from django.urls import path
from .views import ApplicationCreateView, ApplicationRetrieveView

urlpatterns = [
    path('applications/', ApplicationCreateView.as_view(), name='applications-create'),
    path('applications/<int:pk>/', ApplicationRetrieveView.as_view(), name='applications-retrieve'),
]
