from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    telega_id = models.BigIntegerField(unique=True, null=True, blank=True)
