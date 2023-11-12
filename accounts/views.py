from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from .serializers import ShelterSerializer, SeekerSerializer
from .models import Shelter, Seeker

class ShelterListCreateView(ListCreateAPIView):
    serializer_class = ShelterSerializer
    permission_classes = [AllowAny]

class ShelterRetrieveUpdatePermission(BasePermission):
    def has_permission(self, request, view):
        # GET method without authentication is allowed
        if request.method in ["GET"]:
            return True

        return request.user.id == self.kwargs['pk']

class ShelterRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = ShelterSerializer
    permission_classes = [ShelterRetrieveUpdatePermission]
    
    def get_object(self):
        return get_object_or_404(Shelter, id=self.kwargs['pk'])

class DestroyPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.id == self.kwargs['pk']

class ShelterDestroyPetsView(DestroyAPIView):
    serializer_class = ShelterSerializer
    permission_classes = [DestroyPermission]

    def perform_destroy(self, instance):
        # TODO: Remove return
        return
        instance.pets.delete()
        instance.save()

class ShelterDestroyNotificationsView(DestroyAPIView):
    serializer_class = ShelterSerializer
    permission_classes = [DestroyPermission]

    def perform_destroy(self, instance):
        # TODO: Remove return
        return
        instance.notifications.delete()
        instance.save()

class SeekerCreateView(CreateAPIView):
    serializer_class = SeekerSerializer
    permission_classes = [AllowAny]

class SeekerRetrieveUpdatePermission(BasePermission):
    def has_permission(self, request, view):
        # Check if this is shelter retrieving seeker account with active application
        if request.method in ["GET"] and request.user.id != self.kwargs['pk']:
            # Check if this is a shelter requesting
            try:
                shelter = Shelter.objects.get(id=request.user.id)
            except Shelter.DoesNotExist:
                return False

            # TODO: Uncomment when application model is done
            # Check if shelter has an active application from this seeker
            # application = Seeker.applications.get(owner=self.kwargs['pk'])
            # return application.is_active
            return True

        return request.user.id == self.kwargs['pk']

class SeekerRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = SeekerSerializer
    permission_classes = [SeekerRetrieveUpdatePermission]

    def get_object(self):
        return get_object_or_404(Seeker, id=self.kwargs['pk'])

class SeekerDestroyApplicationsView(DestroyAPIView):
    serializer_class = SeekerSerializer
    permission_classes = [DestroyPermission]

    def perform_destroy(self, instance):
        # TODO: Remove return
        return
        instance.applications.delete()
        instance.save()

class SeekerDestroyNotificationsView(DestroyAPIView):
    serializer_class = SeekerSerializer
    permission_classes = [DestroyPermission]

    def perform_destroy(self, instance):
        # TODO: Remove return
        return
        instance.notifications.delete()
        instance.save()
