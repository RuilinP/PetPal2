from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password):
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(make_password(password))
        user.save()
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    password = models.TextField()
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}"

class Shelter(CustomUser):
    organization = models.TextField()
    phone_number = models.TextField(validators=[
        RegexValidator(
            regex='^\d{3}-\d{3}-\d{4}$',
            message='Enter a valid phone number.',
            code='invalid_phone_number'
        ),
    ])
    address = models.TextField()
    country = models.TextField()
    state = models.TextField()
    city = models.TextField()
    zip = models.TextField()
    mission_statement = models.TextField()

    def __str__(self):
        return f"Shelter: {self.email}"

class Seeker(CustomUser):
    first_name = models.TextField(null=True, blank=True)
    last_name = models.TextField(null=True, blank=True)
    phone_number = models.TextField(null=True, blank=True, validators=[
        RegexValidator(
            regex='^\d{3}-\d{3}-\d{4}$',
            message='Enter a valid phone number.',
            code='invalid_phone_number'
        ),
    ])
    address = models.TextField(null=True, blank=True)
    country = models.TextField(null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    zip = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Seeker: {self.email}"

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
    preference = models.TextField(choices=ANIMAL_CHOICES)
    owner = models.ForeignKey(Seeker, related_name="preferences", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.preference}"