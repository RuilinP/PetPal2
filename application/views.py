from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.serializers import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from .serializers import ApplicationSerializer
from .models import Application
from accounts.models import Seeker, Shelter
from pet.models import Pet
from notifications.signals import create_notification_for_user

class ApplicationCreatePermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Check that user making request is a seeker
        if not hasattr(request.user, 'seeker'):
            return False
        
        pet = get_object_or_404(Pet, id=view.kwargs['pk'])

        # Check that pet is available
        return pet.status == 'Available'

class ApplicationCreateView(CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [ApplicationCreatePermission]

    def perform_create(self, serializer):
        serializer.validated_data['seeker'] = get_object_or_404(Seeker, id=self.request.user.id)
        pet = get_object_or_404(Pet, id=self.kwargs['pk'])
        serializer.validated_data['pet'] = pet
        serializer.validated_data['shelter'] = get_object_or_404(Shelter, id=pet.shelter)

        # Check if application already exists
        applications = Application.objects.filter(pet=pet, seeker=serializer.validated_data['seeker'])
        if len(applications) > 0:
            raise ValidationError("Duplicate application.")

        Application.objects.create(**serializer.validated_data)

class ApplicationRetrievePermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        application = get_object_or_404(Application, id=view.kwargs['pk'])
        # Check that user requesting is the application's seeker or shelter
        return request.user.id == application.seeker.id or request.user.id == application.shelter.id

class ApplicationListPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        application = Application.objects.filter(shelter=request.user)
        if not application:
            return False
        return True



class ApplicationRetrieveUpdateStatusView(RetrieveUpdateAPIView):
    serializer_class = ApplicationSerializer
    queryset = Application.objects.all()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        
        if 'status' in data:
            user = request.user
            if (user.id == instance.shelter.id
                and instance.status == Application.PENDING
                and data['status'] in [Application.ACCEPTED, Application.DENIED]) or \
               (user.id == instance.seeker.id
                and instance.status in [Application.PENDING, Application.ACCEPTED] 
                and data['status'] == Application.WITHDRAWN):
                
                serializer = self.get_serializer(instance, data=data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                
                # Update the related pet's status
                pet_id = instance.pet.id
                pet = get_object_or_404(Pet, id=pet_id)
                if data['status'] in ['withdrawn', 'denied']:
                    pet.status = "Available"
                else:
                    pet.status = "Adopted"
                pet.save()

                # Create a notification for:
                # shelter if seeker updated the notification
                # seeker if shelter updated the notification
                if user.id == instance.seeker.id:
                    create_notification_for_user(instance.shelter, instance)
                else:
                    create_notification_for_user(instance.seeker, instance)

                
                return Response(serializer.data)
        return Response({'error': 'You are not allowed to update this field.'}, status=status.HTTP_403_FORBIDDEN)


class ApplicationListAPIView(ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [ApplicationListPermission]
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        status = self.request.query_params.get('status') 
        queryset = Application.objects.filter(shelter=self.request.user)
        if status:
            queryset = queryset.filter(status=status)
        queryset = queryset.order_by('-created_at', '-updated_at')

        return queryset
