from django.db import models
from django.contrib.auth.models import AbstractUser

from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    phone = models.CharField(max_length=15, unique=True)
    username = models.CharField(max_length=255, unique=True)

    USERNAME_FIELD = "phone"

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            "refresh_token": str(refresh)
        }
    