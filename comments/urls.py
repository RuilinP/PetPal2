from django.urls import path
from .views import (ApplicationCommentDetailView, ShelterCommentDetailView, 
                    ShelterCommentListView,
                    ShelterDashboardCommentsView)

urlpatterns = [
    path('applications/<int:application_id>/comments/<int:comment_id>/', ApplicationCommentDetailView.as_view(), name='application-comment-detail'),
    path('shelters/<int:shelter_id>/comments/<int:comment_id>/', ShelterCommentDetailView.as_view(), name='shelter-comment-detail'),
    path('shelters/<int:shelter_id>/comments/', ShelterCommentListView.as_view(), name='list-shelter-comments'),
    path('shelter/<int:shelter_id>/dashboard/comments/', ShelterDashboardCommentsView.as_view(), name='shelter-dashboard-comments'),
]
