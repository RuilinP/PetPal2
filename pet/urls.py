from django.urls import path
from .views import PetCreateView, PetRetrieveUpdateDestroyView

urlpatterns = [
    path('pets/', PetCreateView.as_view(), name='pet-create'),
    path('pets/<int:pk>/', PetRetrieveUpdateDestroyView.as_view(), name='pet-detail'),
]