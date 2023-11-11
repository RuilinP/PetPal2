# models.py
from django.db import models


class Pet(models.Model):
    name = models.CharField(max_length=255)
    gallery = models.TextField() #separate by comma
    breed = models.CharField(max_length=255)
    age = models.CharField(max_length=10)
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    location = models.TextField() #separate by comma
    health = models.TextField()
    characteristics = models.TextField() #separate by comma
    story = models.TextField()
    status = models.CharField(max_length=20)
    shelter = models.IntegerField()


