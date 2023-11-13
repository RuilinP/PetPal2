from rest_framework import serializers
from .models import Notification
from django.urls import reverse
from comments.models import Comment, Application, Reply
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from accounts.models import Shelter

class NotificationSerializer(serializers.ModelSerializer):
    content_object_url = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'object_id', 'content_type', 'created_at', 'is_read', 'content_object_url']
        read_only_fields = ['id', 'recipient', 'object_id', 'content_type', 'created_at', 'is_read']

    def get_content_object_url(self, obj):
        # obj.object_id is the id for either application or comment/reply associated with the notification

        if obj.content_object:

            if obj.content_type == ContentType.objects.get_for_model(Application):
                # implement this: the related name for urls to the application details page may change
                return reverse('application-detail', args=[obj.recipient.id, obj.object_id])
            
            else : # comment or reply
                if obj.content_type == ContentType.objects.get_for_model(Comment):
                    comment = get_object_or_404(Comment, pk=obj.object_id)
                    comment_id = obj.object_id
                elif obj.content_type == ContentType.objects.get_for_model(Reply):
                    # if is reply, get the reply's associated comments
                    comment = get_object_or_404(Reply, pk=obj.object_id).comment
                    comment_id = comment.id
                else:
                    return None

                # comment/reply's associated comment's associated application or shelter id
                related = comment.object_id

                # check if the comment is for application or shelter
                if obj.content_type == ContentType.objects.get_for_model(Application):
                    return reverse('application-comment-detail', args=[obj.recipient.id, related, comment_id])
                elif obj.content_type == ContentType.objects.get_for_model(Shelter):
                    return reverse('shelter-comment-detail', args=[obj.recipient.id, related, comment_id])

                
        return None
