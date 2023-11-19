from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView,RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from .serializers import ApplicationSerializer
from .models import Application
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from pet.models import Pet


class ApplicationCreateView(CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

class ApplicationRetrievePermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        application = get_object_or_404(Application, id=view.kwargs['pk'])
        # Check that user requesting is the application's seeker or shelter
        return request.user.id == application.seeker.id or request.user.id == application.shelter.id

class ApplicationEditPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        print(request.user.id)
        print(view)
        application = Application.objects.filter(shelter=request.user)
        if not application:
            return False
        return True


class ApplicationRetrieveView(RetrieveAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [ApplicationRetrievePermission]

    def get_object(self):
        return get_object_or_404(Application, id=self.kwargs['pk'])

class ApplicationUpdateStatusAPIView(UpdateAPIView):
    serializer_class = ApplicationSerializer
    queryset = Application.objects.all()
    permission_classes = [IsAuthenticated]
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        # pet_id = data['pet']
        # pet = get_object_or_404(Application, id=pet_id)
        if 'status' in data:
            user = request.user
            if (user.id == instance.shelter.id
                and instance.status == 'pending' 
                and data['status'] in ['accepted', 'denied']) or \
            (user.id ==  instance.seeker.id
             and instance.status in ['pending', 'accepted'] 
             and data['status'] == 'withdrawn'):
                serializer = self.get_serializer(instance, data=data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                pet_id = instance.pet.id
                pet = get_object_or_404(Pet, id=pet_id)
                pet.status = data['status']
                pet.save()
                return Response(serializer.data)
        return Response({'error': 'You are not allowed to update this field.'}, status=status.HTTP_403_FORBIDDEN)

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
                and instance.status == 'pending' 
                and data['status'] in ['accepted', 'denied']) or \
               (user.id == instance.seeker.id
                and instance.status in ['pending', 'accepted'] 
                and data['status'] == 'withdrawn'):
                
                serializer = self.get_serializer(instance, data=data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                
                # Update the related pet's status
                pet_id = instance.pet.id
                pet = get_object_or_404(Pet, id=pet_id)
                pet.status = data['status']
                pet.save()
                
                return Response(serializer.data)
     

class ApplicationListAPIView(ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [ApplicationEditPermission]
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
