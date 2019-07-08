from django.db import models
import uuid

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

    def create_token(self):
        self.access_token = uuid.uuid4()


class Movie(models.Model):

    name = models.CharField(max_length=255)
    duration_in_minutes = models.IntegerField(default=120)
    release_date = models.DateTimeField(null=True)
    overall_rating = models.DecimalField(decimal_places=2,max_digits=4)
    censor_board_rating = models.CharField(max_length=5)
    poster_picture = models.CharField(max_length=255)
    user = models.ForeignKey(Users)


class Genre(models.Model):

    name = models.CharField(max_length=255)


class MovieGenre(models.Model):

    movie = models.ForeignKey(Movie)
    genre = models.ForeignKey(Genre)



