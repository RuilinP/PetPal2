from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    password = models.TextField()
    confirm_password = models.TextField()

    USERNAME_FIELD = "email"

class Shelter(CustomUser):
    organization = models.TextField()
    phone_number = models.TextField()
    address = models.TextField()
    country = models.TextField()
    state = models.TextField()
    city = models.TextField()
    zip = models.TextField()
    mission_statement = models.TextField()

class Preference(models.Model):
    DOG = 'dog'
    CAT = 'cat'
    HAMSTER = 'hamster'
    BIRD = 'bird'
    RABBIT = 'rabbit'    
    ANIMAL_CHOICES = (
        (DOG, DOG),
        (CAT, CAT),
        (HAMSTER, HAMSTER),
        (BIRD, BIRD),
        (RABBIT, RABBIT)
    )
    preference = models.TextField(choices=ANIMAL_CHOICES, null=True, blank=True)

class Seeker(CustomUser):
    phone_number = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    country = models.TextField(null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    zip = models.TextField(null=True, blank=True)
    preferences = models.ManyToManyField(Preference)
