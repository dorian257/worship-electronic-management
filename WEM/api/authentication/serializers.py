# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # The 'validate' method is where we make sure that the current
        # instance of 'LoginSerializer' has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        username = data.get("username", None)
        password = data.get("password", None)

        # Raise an exception if an
        # username is not provided.
        if username is None:
            raise serializers.ValidationError(
                "An username address is required to log in."
            )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError("A password is required to log in.")

        # The 'authenticate' method is provided by Django and handles checking
        # for a user that matches this username/password combination. Notice how
        # we pass 'username' as the 'username' value since in our User
        # model we set 'USERNAME_FIELD' as 'username'.
        user = authenticate(username=username, password=password)

        # If no user was found matching this username/password combination then
        # 'authenticate' will return 'None'. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                "A user with this email and password was not found."
            )

        # Django provides a flag on our 'User' model called 'is_active'. The
        # purpose of this flag is to tell us whether the user has been banned
        # or deactivated. This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError("This user has been deactivated.")

        # The 'validate' method should return a dictionary of validated data.
        # This is the data that is passed to the 'create' and 'update' methods
        # that we will see later on.
        return {"username": user.username, "token": user.token}
