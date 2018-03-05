from django.db import models
from groups.models import Group
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()
class BuddyMessage(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    group = models.ForeignKey(Group, related_name='messages', on_delete = models.CASCADE, null=True)
    message = models.TextField(max_length = 255)
    message_type = models.IntegerField(choices = settings.MESSAGE_TYPES_CHOICES, default=0)

    message_html = models.TextField(max_length = 255, blank=True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.message
