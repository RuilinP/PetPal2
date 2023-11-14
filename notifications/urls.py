from django.urls import path
from .views import ListNotificationsView, NotificationDetailView
from comments.views import ApplicationCommentDetailView, ShelterCommentDetailView

urlpatterns = [
    path('<int:user_id>/notifications/', ListNotificationsView.as_view(), name='list-notifications'),
    path('<int:user_id>/notifications/<int:notification_id>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('<int:user_id>/applications/<int:application_id>/comments/<int:comment_id>/', ApplicationCommentDetailView.as_view(), name='application-comment-detail'),
    path('<int:user_id>/shelters/<int:shelter_id>/comments/<int:comment_id>/', ShelterCommentDetailView.as_view(), name='shelter-comment-detail'),
    # implement this: add url to application details view


]