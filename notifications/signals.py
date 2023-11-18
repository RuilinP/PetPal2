from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from .models import Notification
from django.contrib.contenttypes.models import ContentType
from accounts.models import Shelter, CustomUser
from comments.models import Comment, Reply
from application.models import Application

def is_shelter(user_id):
    cur_user = get_object_or_404(CustomUser, pk=user_id)
    if hasattr(cur_user, 'seeker'):
        return False
    return True

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        recipient = determine_comment_recipient(instance)
    
        Notification.objects.create(
            recipient=recipient, 
            content_object=instance,
            object_id=instance.id,
            content_type=ContentType.objects.get_for_model(instance)
        )

def determine_comment_recipient(comment):
   
    # for new shelter comments, the recipient is always the shelter
    # for new application comments, the recipient is:
    # - the shelter, when author is seeker
    # - the seeker, when author is shelter

    # determine if it is a shelter or application comment
    application_content_type = ContentType.objects.get_for_model(Application)
    shelter_content_type = ContentType.objects.get_for_model(Shelter)

    if comment.content_type == application_content_type:
        # need to know the author type
        if is_shelter(comment.author):
            recipient = comment.content_object.seeker # get seeker obj from application
        else:
            recipient = comment.content_object.shelter  # get shelter obj from application
    
    else: 
        recipient = comment.content_object # is the shelter
    
    return recipient



@receiver(post_save, sender=Reply)
def create_reply_notification(sender, instance, created, **kwargs):
    if created:
        recipient = determine_reply_recipient(instance)
    
        Notification.objects.create(
            recipient=recipient, 
            content_object=instance,
            object_id=instance.id,
            content_type=ContentType.objects.get_for_model(instance)
        )


def determine_reply_recipient(reply):
    
    # for new shelter replies, the recipient is always the sender of the original comment  
    return reply.comment.author




# implement this: add a signal for applications too
@receiver(post_save, sender=Application)
def create_reply_notification(sender, instance, created, **kwargs):
    if created: # for new application submission, alert the shelter
        recipient = instance.shelter
    
        Notification.objects.create(
            recipient=recipient, 
            content_object=instance,
            object_id=instance.id,
            content_type=ContentType.objects.get_for_model(instance)
        )

    # implement this in application/views.py: alert the shelter and the seeker when application status is updated