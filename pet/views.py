from django.shortcuts import render

# views.py
from rest_framework import generics
from .models import Pet
from .serializers import PetSerializer
from .filters import PetFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q



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
        shelter_param = self.request.query_params.get('shelter')
        status_param = self.request.query_params.get('status')
        gender_param = self.request.query_params.get('gender')
        specie_param = self.request.query_params.get('specie')
        breed_param = self.request.query_params.get('breed')

        queryset = Pet.objects.all().order_by(sort)
        if not status_param:
            status_param = 'Available'  
            queryset = queryset.filter(status=status_param)
        else:
            statuses = status_param.split(',')
            query_filter = Q()
            for status in statuses:
                query_filter |= Q(status=status)
            queryset = queryset.filter(query_filter)
            

        

        if name:
            queryset = queryset.filter(name__icontains=name)
        if shelter_param:
            shelters = shelter_param.split(',')
            query_filter = Q()
            for shelter in shelters:
                query_filter |= Q(shelter=shelter)
            queryset = queryset.filter(query_filter)
        if specie_param:
            species = specie_param.split(',')
            query_filter = Q()
            for specie in species:
                query_filter |= Q(specie=specie)
            queryset = queryset.filter(query_filter)
        if breed_param:
            breeds = breed_param.split(',')
            query_filter = Q()
            for breed in breeds:
                query_filter |= Q(breed=breed)
            queryset = queryset.filter(query_filter)

        if gender_param:
            genders = gender_param.split(',')
            query_filter = Q()
            for gender in genders:
                query_filter |= Q(gender=gender)
            queryset = queryset.filter(query_filter)
            # queryset = queryset.filter(gender__iexact=gender)
        return queryset