from django.contrib import admin
from .models import Comment, Reply, Shelter, Application

admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Shelter)
admin.site.register(Application)