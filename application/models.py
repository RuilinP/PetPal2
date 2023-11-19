from django.db import models
from accounts.models import Seeker, Shelter
from pet.models import Pet

class Application(models.Model):
    seeker = models.ForeignKey(Seeker, on_delete=models.CASCADE, related_name='applications')
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name='applications')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='applications')
    
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    DENIED = 'denied'
    WITHDRAWN = 'withdrawn'
    STATUS_CHOICES = [ # seeker actions allowed: pending, accepted, withdrawn; shelter actions allowed: pending, accepted, denied
        (PENDING, PENDING),
        (ACCEPTED, ACCEPTED),
        (DENIED, DENIED),
        (WITHDRAWN, WITHDRAWN)
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    message = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', '-updated_at']


 # to minimize redundancy, fields such as the seeker's address, phone number,.etc are not included in the model.
 # These can be accessed through the Seeker object stored in seeker field
 # lmk if you think it is necessary to have those fields in the model