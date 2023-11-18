from django.urls import path
from .views import (ApplicationCommentDetailView, ShelterCommentDetailView, 
                    ShelterCommentListView,
                    ApplicationCommentListView)

urlpatterns = [
    path('applications/<int:application_id>/comments/<int:comment_id>/', ApplicationCommentDetailView.as_view(), name='application-comment-detail'),
    path('shelters/<int:shelter_id>/comments/<int:comment_id>/', ShelterCommentDetailView.as_view(), name='shelter-comment-detail'),
    path('shelters/<int:shelter_id>/comments/', ShelterCommentListView.as_view(), name='list-shelter-comments'),
    path('applications/<int:application_id>/comments/', ApplicationCommentListView.as_view(), name='list-application-comments'),
]
