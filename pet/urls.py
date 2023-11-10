from django.urls import path
from .views import PetCreateView, PetRetrieveUpdateDestroyView, PetListView, PetListSearch

urlpatterns = [
    path('pet/', PetCreateView.as_view(), name='pet-create'),
    path('pet/<int:pk>', PetRetrieveUpdateDestroyView.as_view(), name='pet-detail'),
    path('pets/', PetListView.as_view(), name='pet-list'),
    path('pets/search/', PetListSearch.as_view(), name='pet-list'),
]