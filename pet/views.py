from django.shortcuts import render

# views.py
from rest_framework import generics
from .models import Pet
from .serializers import PetSerializer
from .filters import PetFilter
from django_filters.rest_framework import DjangoFilterBackend



class PetCreateView(generics.CreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

class PetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

class PetListView(generics.ListAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    filter_backends = []
    filterset_class = PetFilter

    def get_queryset(self):
        status = self.request.query_params.get('status', 'available')
        sort = self.request.query_params.get('sort', 'name')

        queryset = Pet.objects.filter(status=status).order_by(sort)

        return queryset
