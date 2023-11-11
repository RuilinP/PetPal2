from django.urls import path
from .views import ShelterCreateRetrieveView, ShelterRetrieveUpdateView, SeekerCreateView, SeekerRetrieveUpdateView

urlpatterns = [
    path('shelters/', ShelterCreateRetrieveView.as_view(), name='shelter-create'),
    path('shelters/<int:pk>/', ShelterRetrieveUpdateView.as_view(), name='shelter-update'),
    path('seekers/', SeekerCreateView.as_view(), name='seeker-create'),
    path('seekers/<int:pk>/', SeekerRetrieveUpdateView.as_view(), name='seeker-update'),
]
