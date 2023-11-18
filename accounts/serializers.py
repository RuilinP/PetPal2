from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Shelter, Preference, Seeker

class ShelterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelter
        fields = '__all__'
    
    def validate_password(self, password):
        return make_password(password)

class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = ['preference']

class SeekerSerializer(serializers.ModelSerializer):
    preferences = serializers.ListSerializer(child=PreferenceSerializer(), required=False)

    class Meta:
        model = Seeker
        fields = '__all__'

    def validate_password(self, password):
        return make_password(password)
