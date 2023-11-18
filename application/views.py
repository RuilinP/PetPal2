from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from .serializers import ApplicationSerializer
from .models import Application

class ApplicationCreateView(CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

class ApplicationRetrievePermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        application = get_object_or_404(Application, id=view.kwargs['pk'])
        # Check that user requesting is the application's seeker or shelter
        return request.user.id == application.seeker or request.user.id == application.shelter

class ApplicationRetrieveView(RetrieveAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [ApplicationRetrievePermission]

    def get_object(self):
        return get_object_or_404(Application, id=self.kwargs['pk'])
