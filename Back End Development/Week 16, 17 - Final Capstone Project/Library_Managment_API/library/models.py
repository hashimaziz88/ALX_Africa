from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_membership = models.DateField(auto_now=False, auto_now_add=False)
