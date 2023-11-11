from rest_framework import serializers
from .models import Shelter, Preference, Seeker

class ShelterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelter
        fields = '__all__'

class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = '__all__'

class SeekerSerializer(serializers.ModelSerializer):
    preferences = PreferenceSerializer(many=True)

    class Meta:
        model = Seeker
        fields = '__all__'
