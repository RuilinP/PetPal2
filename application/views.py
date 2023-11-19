from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from .serializers import ApplicationSerializer
from .models import Application
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination



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
