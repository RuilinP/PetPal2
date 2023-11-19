from rest_framework import serializers
from .models import Application
from accounts.models import Shelter, Seeker 
from pet.models import Pet

class ApplicationSerializer(serializers.ModelSerializer):
    seeker = serializers.PrimaryKeyRelatedField(queryset=Seeker.objects.all())
    shelter = serializers.PrimaryKeyRelatedField(queryset=Shelter.objects.all())
    pet = serializers.PrimaryKeyRelatedField(queryset=Pet.objects.all())

    class Meta:
        model = Application
        fields = ['id', 'seeker', 'shelter', 'pet', 'status', 'message', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at' ]
