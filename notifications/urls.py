from django.urls import path
from .views import ListNotificationsView, NotificationDetailView
from comments.views import ApplicationCommentDetailView, ShelterCommentDetailView
from application.views import ApplicationRetrieveUpdateStatusView

urlpatterns = [
    path('notifications/', ListNotificationsView.as_view(), name='list-notifications'),
    path('notifications/<int:notification_id>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('applications/<int:application_id>/comments/<int:comment_id>/', ApplicationCommentDetailView.as_view(), name='application-comment-detail'),
    path('shelters/<int:shelter_id>/comments/<int:comment_id>/', ShelterCommentDetailView.as_view(), name='shelter-comment-detail'),
    path('applications/<int:pk>/', ApplicationRetrieveUpdateStatusView.as_view(), name='applications-retrieve'),


]
