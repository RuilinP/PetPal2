from django.urls import path
from .views import ApplicationCreateView, ApplicationRetrieveView, ApplicationListAPIView

urlpatterns = [
    path('application/', ApplicationCreateView.as_view(), name='applications-create'),
    path('applications/<int:pk>/', ApplicationRetrieveView.as_view(), name='applications-retrieve'),
    path('applications/', ApplicationListAPIView.as_view(), name='applications-list'),
]
