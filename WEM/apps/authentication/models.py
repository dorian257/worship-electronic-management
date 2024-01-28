import logging
from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from WEM.apps.core.models import TimestampedModel

TOKEN_EXPIRATION_IN_SECONDS = getattr(settings, "TOKEN_EXPIRATION_IN_SECONDS", 24 * 60 * 60)

logger = logging.getLogger(__name__)

# Create your models here.


class MYUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):

        if not email:
            raise ValueError("Users must have an Email")

        if not username:
            raise ValueError("Users must have a username")

        if email:
            email = self.normalize_email(email)

        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password=None):

        if not email:
            raise ValueError("Superusers must have an Email")

        if not username:
            raise ValueError("Superusers must have a username")

        user = self.create_user(email, username, password)
        user.is_admin = True
        user.save(using=self._db)

        return user


class MyUser(AbstractBaseUser, PermissionsMixin):

    email = models.CharField(max_length=50, verbose_name="Email adresse", unique=True)
    username = models.CharField(max_length=27, verbose_name="Username", unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MYUserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ("email",)

    def __str__(self):
        """
        Returns a string representation of this 'User'.

        This string is used when a 'User' is printed in the console.
        """
        return getattr(self, self.USERNAME_FIELD)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_full_name(self):
        if hasattr(self, "profile"):
            return self.profile.get_full_name()
        return getattr(self, self.USERNAME_FIELD)

    def get_short_name(self):
        return getattr(self, self.USERNAME_FIELD)

    @property
    def token(self):
        """
        Allows us to get a user's token by calling 'user.token' instead of
        'user.generate_jwt_token().

        The '@property' decorator above makes this possible. 'token' is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def _get_jwt_payload(self):
        # dt = datetime.utcnow() + timedelta(days=1)
        dt = datetime.utcnow() + timedelta(seconds=TOKEN_EXPIRATION_IN_SECONDS)

        # payload = {"id": self.pk, "exp": int(dt.strftime("%s"))},
        payload = {"id": self.pk, "exp": dt, "iat": datetime.utcnow()}

        return payload

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 1 days(s) into the future.

        https://pyjwt.readthedocs.io/en/latest/usage.html
        """

        token = jwt.encode(self._get_jwt_payload(), settings.SECRET_KEY, algorithm="HS256")

        return token.decode("utf-8")