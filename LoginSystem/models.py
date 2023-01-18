from django.db import models
from LoginSystem.Authentication import Authentication

# Create your models here.

class BLUser(models.Model):
    email = models.CharField(max_length=255, unique=True)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    password = models.CharField(max_length=200)
    PublicAdress = models.CharField(max_length=255)
    config = models.TextField('')
    logintype = models.IntegerField(Authentication.Email_password)

class RestAPIKeys(models.Model):
    APISecret =  models.CharField(max_length=255, unique=True)