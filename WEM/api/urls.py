from django.urls import include, path

urlpatterns = [
    path("users/", include("WEM.api.authentication.urls")),
]
