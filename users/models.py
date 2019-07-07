from django.db import models

# Create your models here.


class Users(models.Model):

    name = models.CharField(max_length=255, null=False, blank=False)
    username = models.CharField(max_length=255, null=False, blank=False,unique=True)
    email = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=10)
    password = models.CharField(max_length=255, null=False, blank=False)
    short_bio = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class AccessToken(models.Model):

    user = models.ForeignKey(Users)
    access_token = models.CharField(max_length=255)
    last_request_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

