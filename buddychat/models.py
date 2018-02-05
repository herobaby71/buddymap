from django.db import models
from groups.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()
class BuddyRoom(models.Model):
    group = models,OneToOneField(Group, on_delete=models.CASCADE, primary_key=True)
    label = models.SlugField(unique=True)

class BuddyMessage(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    room = models.ForeignKey(BuddyRoom, related_name='messages')
    message = models.TextField(max_length = 3000)
    message_html = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.message
