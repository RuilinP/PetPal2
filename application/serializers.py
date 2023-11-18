from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'seeker', 'shelter', 'pet', 'status', 'message', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at' ]
