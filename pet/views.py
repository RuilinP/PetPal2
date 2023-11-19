from django.shortcuts import render

# views.py
from rest_framework import generics
from .models import Pet
from .serializers import PetSerializer
from .filters import PetFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated,SAFE_METHODS
from .permissions import IsShelterUser
from rest_framework.response import Response



class PetCreateView(generics.CreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    permission_classes = [IsAuthenticated, IsShelterUser]

    def perform_create(self, serializer):
        serializer.save(shelter=self.request.user.id)


class PetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated(), IsShelterUser()]
        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Save the shelter as the authenticated user's ID
        serializer.validated_data['shelter'] = request.user.id
        self.perform_update(serializer)
        return Response(serializer.data)
        
    


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
        age_param = self.request.query_params.get('age')

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
        if age_param:
            ages = age_param.split(',')
            query_filter = Q()
            for age in ages:
                query_filter |= Q(age=age)
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
                query_filter |= Q(breed__icontains=breed)
            queryset = queryset.filter(query_filter)

        if gender_param:
            genders = gender_param.split(',')
            query_filter = Q()
            for gender in genders:
                query_filter |= Q(gender=gender)
            queryset = queryset.filter(query_filter)
            # queryset = queryset.filter(gender__iexact=gender)
        return queryset