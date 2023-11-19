from django.urls import path
from .views import ApplicationCreateView, ApplicationListAPIView, ApplicationRetrieveUpdateStatusView

urlpatterns = [
    path('pets/<int:pk>/applications/', ApplicationCreateView.as_view(), name='applications-create'),
    path('applications/<int:pk>/', ApplicationRetrieveUpdateStatusView.as_view(), name='applications-retrieve'),
    path('applications/', ApplicationListAPIView.as_view(), name='applications-list'),
]
