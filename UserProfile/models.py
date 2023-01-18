from django.db import models

# Create your models here.
from LoginSystem.models import BLUser


class UserProfile(models.Model):
    owner = models.ForeignKey(BLUser, on_delete=models.PROTECT)
    image = models.CharField(max_length=255)
    bio = models.TextField('')
    socialmedia = models.TextField('')
    category = models.CharField(max_length=100)
    config = models.TextField('')

