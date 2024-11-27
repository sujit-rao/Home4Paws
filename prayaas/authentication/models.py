from django.db import models
import datetime
import os


# Create your models here.
class user_data(models.Model):
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    phone=models.CharField(max_length=200)
    city=models.CharField(max_length=200, blank=True)
    address=models.CharField(max_length=200)
    country=models.CharField(max_length=200)
