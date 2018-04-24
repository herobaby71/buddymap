from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from groups.models import Group
from events.models import Event

User = get_user_model()

class Activity(models.Model):
    longitude = models.DecimalField(decimal_places=55, max_digits=60)
    latitude = models.DecimalField(decimal_places=55, max_digits=60)
    created = models.DateTimeField(default = timezone.now)


class Poke(Activity):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='poke')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='poked_by')

    def __str__(self):
        return ''.join((str(self.user_from), ' poke ', str(self.user_to)))

class CreateGroup(Activity):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owns_group')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='created_by')

    def __str__(self):
        return ''.join((str(self.owner), ' Creates Group ', str(self.group)))

class CreateEvent(Activity):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owns_event')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='created_by')

    def __str__(self):
        return ''.join((str(owner), ' Creates ', str(event)))

class QuickMessage(Activity):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messaged_by')
    message = models.CharField(max_length=255, default='Hi! Wassup :)', null=True, blank=True)


    def __str__(self):
        return ''.join((str(self.user_from), ' message ', str(self.user_to)))

# class AddFriend(Activity):
#
# class HideFromGroup(Activity):
#
# class HideFromUser(Activity):
#
# class Block(Activity):
