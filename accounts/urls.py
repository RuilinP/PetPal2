from django.urls import path
from .views import ShelterListCreateView, ShelterRetrieveUpdateView, ShelterDestroyPetsView, \
    SeekerCreateView, SeekerRetrieveUpdateView, SeekerDestroyApplicationsView

urlpatterns = [
    path('shelters/', ShelterListCreateView.as_view(), name='shelter-list-create'),
    path('shelters/<int:pk>/pets/', ShelterDestroyPetsView.as_view(), name='shelter-destroy-pets'),
    path('shelters/<int:pk>/', ShelterRetrieveUpdateView.as_view(), name='shelter-update'),
    path('seekers/', SeekerCreateView.as_view(), name='seeker-create'),
    path('seekers/<int:pk>/applications/', SeekerDestroyApplicationsView.as_view(), name='seeker-destroy-applications'),
    path('seekers/<int:pk>/', SeekerRetrieveUpdateView.as_view(), name='seeker-update'),
]
