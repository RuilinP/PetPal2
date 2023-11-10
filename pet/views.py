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
        #status = self.request.query_params.get('status', 'available')
        sort = self.request.query_params.get('sort', 'name')

        #queryset = Pet.objects.filter(status=status).order_by(sort)
        queryset = Pet.objects.all().order_by(sort)

        # name = self.request.query_params.get('name')
        # shelter = self.request.query_params.get('shelter')
        # status = self.request.query_params.get('status')
        # gender = self.request.query_params.get('gender')

        # if name:
        #     queryset = queryset.filter(name__icontains=name)
        # if shelter:
        #     queryset = queryset.filter(breed__iexact=shelter)
        # if status:
        #     queryset = queryset.filter(color__iexact=status)
        # if gender:
        #     queryset = queryset.filter(gender__iexact=gender)
        return queryset

class PetListSearch(generics.ListAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    filter_backends = []
    filterset_class = PetFilter

    def get_queryset(self):
        # status = self.request.query_params.get('status', 'available')
        sort = self.request.query_params.get('sort', 'id')

        name = self.request.query_params.get('name')
        shelter = self.request.query_params.get('shelter')
        status = self.request.query_params.get('status')
        gender = self.request.query_params.get('gender')

        queryset = Pet.objects.all().order_by(sort)
        if not status:
            status = 'available'  
            queryset = queryset.filter(status=status)
        else:
            queryset = queryset.filter(status=status)

        

        if name:
            queryset = queryset.filter(name__icontains=name)
        if shelter:
            queryset = queryset.filter(breed__iexact=shelter)
        # if status:
        #     queryset = queryset.filter(color__iexact=status)
        if gender:
            queryset = queryset.filter(gender__iexact=gender)
        return queryset