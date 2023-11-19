from django.urls import path
from .views import PetCreateView, PetRetrieveUpdateDestroyView, PetListSearch

urlpatterns = [
    path('pet/', PetCreateView.as_view(), name='pet-create'),
    path('pets/<int:pk>', PetRetrieveUpdateDestroyView.as_view(), name='pet-detail'),
    path('pets/', PetListSearch.as_view(), name='pet-list'),
]