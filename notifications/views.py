from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404



# get, update read status, delete
class NotificationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, notification_id):
        notification = get_object_or_404(Notification, pk=notification_id, recipient=request.user)
        notification.is_read = True
        notification.save()

        serializer = NotificationSerializer(notification)
        return Response(serializer.data)
    
    def delete(self, request, notification_id):
        notification = get_object_or_404(Notification, pk=notification_id, recipient=request.user)
        
        # check if the user is allowed to delete this notification
        if notification.recipient != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# list
class ListNotificationsView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user
        queryset = Notification.objects.filter(recipient=user)

        read_status = self.request.query_params.get('is_read')
        if read_status is not None:
            queryset = queryset.filter(is_read=read_status == 'true')

        return queryset.order_by('-created_at')  # Ordering by creation time
    