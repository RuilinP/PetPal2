from django.urls import path
from .views import (ApplicationCommentDetailView, ShelterCommentDetailView, 
                    ShelterCommentListView,
                    ApplicationCommentListView)

urlpatterns = [
    path('<int:user_id>/applications/<int:application_id>/comments/<int:comment_id>/', ApplicationCommentDetailView.as_view(), name='application-comment-detail'),
    path('<int:user_id>/shelters/<int:shelter_id>/comments/<int:comment_id>/', ShelterCommentDetailView.as_view(), name='shelter-comment-detail'),
    path('<int:user_id>/shelters/<int:shelter_id>/comments/', ShelterCommentListView.as_view(), name='list-shelter-comments'),
    path('<int:user_id>/applications/<int:application_id>/comments/', ApplicationCommentListView.as_view(), name='list-application-comments'),
]
