from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.common.models import TimeStampedModel


class User(AbstractUser, TimeStampedModel):
    image = models.ImageField(upload_to="profile-image", null=True, blank=True)
