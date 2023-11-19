# models.py
from django.db import models


class Pet(models.Model):
    name = models.CharField(max_length=255)
    gallery = models.TextField() #separate by comma
    specie = models.CharField(max_length=10)
    breed = models.CharField(max_length=255)
    age = models.CharField(max_length=10)
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    location = models.TextField() #separate by comma
    health = models.TextField()
    characteristics = models.TextField() #separate by comma
    story = models.TextField()
    PET_CHOICES = [
        ("Available", "Available"),
        ("Adopted", "Adopted"),
    ]
    status = models.CharField(max_length=20, choices=PET_CHOICES)
    shelter = models.IntegerField()


