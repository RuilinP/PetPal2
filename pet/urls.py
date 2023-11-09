from django.urls import path
from .views import PetListCreateView, PetDetailView

urlpatterns = [
    path('user/', PetListCreateView.as_view(), name='pet-list-create'),
    path('user/<int:pk>/', PetDetailView.as_view(), name='pet-detail'),
]