from django.shortcuts import render

# views.py
from rest_framework import generics
from .models import Pet
from .serializers import PetSerializer



class PetCreateView(generics.ListCreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

class PetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

# class PetDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Pet.objects.all()
#     serializer_class = PetSerializer
