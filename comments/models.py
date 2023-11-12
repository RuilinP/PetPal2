from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Shelter(models.Model):
    name = models.CharField(max_length=100)
    # other fields...

class Application(models.Model):
    applicant_name = models.CharField(max_length=100)
    # other fields...



class Comment(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    rating = models.IntegerField(choices=RATING_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    # could be a reply from user or shelter, so leave unread options for both
    unread_by_shelter = models.BooleanField(default=False)
    unread_by_author = models.BooleanField(default=False)

    # use ContentType to associate with either a shelter or an application
    # if content_object is set to a shelter instance, the object_id and content_type will be set to that shelter's id and 'Shelter'
    object_id = models.PositiveIntegerField()
    
    # ContentType is a built-in Django model that keeps a record of all models in petpal,i.e. 'Shelter' and 'Application'
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    
    # generic foreign key to the related object, i.e. content_type could be 'Shelter' class and object_id could be a shelter_id
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.author_is_shelter(): # if yes the shelter itself would have read the comment it wrote
                self.unread_by_shelter = True
            
            if not self.author_is_pet_seeker():
                self.unread_by_author = True

        super(Comment, self).save(*args, **kwargs)

    def author_is_shelter(self):
        # Implement logic to determine if the author is the shelter
        pass

    def author_is_pet_seeker(self):
        # Implement logic to determine if the author is the pet seeker
        pass    

    class Meta:
        # sorting comments in descending order based on creation time
        ordering = ['-created_at']


class Reply(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE)
    text = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    unread_by_shelter = models.BooleanField(default=False)
    unread_by_author = models.BooleanField(default=False)

    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.author_is_shelter():
                self.unread_by_shelter = True
            
            if not self.author_is_pet_seeker():
                self.unread_by_author = True

        super(Reply, self).save(*args, **kwargs)

    def author_is_shelter(self):
        # Implement logic to determine if the author is the shelter
        pass

    def author_is_pet_seeker(self):
        # Implement logic to determine if the author is the pet seeker
        pass    

    class Meta:
        # sorting replies in ascending order based on creation time
        ordering = ['created_at']