from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, BasePermission
from .serializers import ShelterSerializer, SeekerSerializer
from .models import Shelter, Seeker, Preference
from pet.models import Pet
from application.models import Application
from notifications.models import Notification

class ShelterListCreatePermission(BasePermission):
    def has_permission(self, request, view):
        # POST method by any user is allowed
        if request.method in ["POST"]:
            return True

        return request.user.is_authenticated

class ShelterListCreateView(ListCreateAPIView):
    serializer_class = ShelterSerializer
    permission_classes = [ShelterListCreatePermission]
    queryset = Shelter.objects.all()

class ShelterRetrieveUpdatePermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # GET method by any authenticated user is allowed
        if request.method in ["GET"]:
            return True

        return request.user.id == view.kwargs['pk']

class ShelterRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = ShelterSerializer
    permission_classes = [ShelterRetrieveUpdatePermission]

    def get_object(self):
        return get_object_or_404(Shelter, id=self.kwargs['pk'])

class DestroyPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.id == view.kwargs['pk']

class ShelterDestroyPetsView(DestroyAPIView):
    serializer_class = ShelterSerializer
    permission_classes = [DestroyPermission]

    def get_queryset(self):
        return Pet.objects.filter(shelter=self.kwargs['pk'])

class ShelterDestroyNotificationsView(DestroyAPIView):
    serializer_class = ShelterSerializer
    permission_classes = [DestroyPermission]

    def get_queryset(self):
        recipient = get_object_or_404(Shelter, id=self.kwargs['pk'])
        return Notification.objects.filter(recipient=recipient)

class SeekerCreateView(CreateAPIView):
    serializer_class = SeekerSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # Remove preferences from the form data
        preferences = serializer.validated_data.pop('preferences', tuple())

        # Save the seeker first (otherwise preferences won't have a seeker to refer to)
        seeker = Seeker.objects.create(**serializer.validated_data)

        # Create a new preference object for each preference
        for preference in preferences:
            Preference.objects.create(**preference, owner=seeker)

class SeekerRetrieveUpdatePermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # Check if this is shelter retrieving seeker account with active application
        if request.method in ["GET"] and request.user.id != view.kwargs['pk']:
            # Check if shelter has an active application from this seeker
            return Application.objects.all().filter(shelter=request.user.id, seeker=view.kwargs['pk'], status='pending').exists()

        return request.user.id == view.kwargs['pk']

class SeekerRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = SeekerSerializer
    permission_classes = [SeekerRetrieveUpdatePermission]

    def get_object(self):
        return get_object_or_404(Seeker, id=self.kwargs['pk'])
    
    def perform_update(self, serializer):
        # Remove preferences from the form data
        preferences = serializer.validated_data.pop('preferences', None)

        # Update the seeker
        super().perform_update(serializer)

        if preferences != None:
            # Delete existing preferences
            Preference.objects.filter(owner=self.kwargs['pk']).delete()

            seeker = Seeker.objects.get(id=self.kwargs['pk'])

            # Create new preferences
            for preference in preferences:
                Preference.objects.create(**preference, owner=seeker)

class SeekerDestroyApplicationsView(DestroyAPIView):
    serializer_class = SeekerSerializer
    permission_classes = [DestroyPermission]

    def get_queryset(self):
        seeker = get_object_or_404(Seeker, id=self.kwargs['pk'])
        return Application.objects.filter(seeker=seeker)

class SeekerDestroyNotificationsView(DestroyAPIView):
    serializer_class = SeekerSerializer
    permission_classes = [DestroyPermission]

    def get_queryset(self):
        recipient = get_object_or_404(Seeker, id=self.kwargs['pk'])
        return Notification.objects.filter(recipient=recipient)
