from django.db import models
from accounts.models import CustomUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



class Comment(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    rating = models.IntegerField(choices=RATING_CHOICES)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    # use ContentType to associate with either a shelter or an application
    # if content_object is set to a shelter instance, the object_id and content_type will be set to that shelter's id and 'Shelter'
    object_id = models.PositiveIntegerField()
    
    # ContentType is a built-in Django model that keeps a record of all models in petpal,i.e. 'Shelter' and 'Application'
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    
    # generic foreign key to the related object, i.e. content_type could be 'Shelter' class and object_id could be a shelter_id
    content_object = GenericForeignKey('content_type', 'object_id')   

    class Meta:
        # sorting comments in descending order based on creation time
        ordering = ['-created_at']


class Reply(models.Model):

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE)
    text = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id') 

    class Meta:
        # sorting replies in ascending order based on creation time
        ordering = ['created_at']