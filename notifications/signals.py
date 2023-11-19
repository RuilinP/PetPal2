from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from .models import Notification
from django.contrib.contenttypes.models import ContentType
from accounts.models import CustomUser
from comments.models import Comment, Reply
from application.models import Application



def is_shelter(user_id):
    cur_user = get_object_or_404(CustomUser, pk=user_id)
    if hasattr(cur_user, 'seeker'):
        return False
    return True



def create_notification_for_user(user, instance):
    """ helper function to create notification for a user. """
    Notification.objects.create(
        recipient=user, 
        content_object=instance,
        object_id=instance.id,
        content_type=ContentType.objects.get_for_model(instance)
    )



@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        create_notification_for_user(determine_comment_recipient(instance), instance)



def determine_comment_recipient(comment):
   
    # for new shelter comments, the recipient is always the shelter
    # for new application comments, the recipient is:
    # - the shelter, when author is seeker
    # - the seeker, when author is shelter

    # determine if it is a shelter or application comment
    application_content_type = ContentType.objects.get_for_model(Application)

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
        # create notif for comment author
        create_notification_for_user(instance.comment.author, instance)

        # create notif for unique users who replies to the comment
        replied_users = set()
        for reply in instance.comment.replies.all():
            # don't create for comment author or user themselves
            if reply.author != instance.comment.author and reply.author != instance.author:
                replied_users.add(reply.author)

        for user in replied_users:
            create_notification_for_user(user, instance)



@receiver(post_save, sender=Application)
def create_reply_notification(sender, instance, created, **kwargs):

    if created: # for new application submission, alert the shelter
        create_notification_for_user(instance.shelter, instance)

    # implement this in application/views.py: alert the shelter and the seeker when application status is updated