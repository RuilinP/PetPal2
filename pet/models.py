from django.db import models
from django.contrib.postgres.fields import ArrayField

class Pet(models.Model):
    name = models.CharField(max_length=255)
    gallery = ArrayField(models.CharField(max_length=50), size=4)
    breed = models.CharField(max_length=255)
    age = models.IntegerField()
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    location = ArrayField(models.CharField(max_length=20), size=2)
    characteristics = ArrayField(models.CharField(max_length=50), size=5)
    health = models.CharField(max_length=1000)
    story = models.CharField(max_length=3000)
    status = models.CharField(max_length=20, default="available")
    shelter_id = models.CharField(max_length=10)
