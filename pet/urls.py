from django.urls import path
from .views import PetCreateView, PetDetailView

urlpatterns = [
    path('pets/create', PetCreateView.as_view(), name='pet-create'),
    path('pets/<int:pk>/', PetDetailView.as_view(), name='pet-detail'),
]