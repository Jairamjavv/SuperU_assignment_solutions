from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=50)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class UserProfiles(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    bio = models.CharField(max_length=100)
    profile_picture_url = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.fname} user'