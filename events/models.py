from django.contrib.auth import get_user_model
from groups.models import Group
from django.db import models
from django.utils import timezone

User = get_user_model()

def default_last():
    return timezone.timedelta(minutes=20)

class EventManager(models.Manager):
    def create_event(self, group, name, description, started, exipred, longitude, latitude):
        event = self.create(group=group, name=name, description=description, started=started, expired=expired, longitude=longitude, latitude=latitude)
        return event

class Event(models.Model):
    group = models.ForeignKey(Group, on_delete = models.CASCADE, related_name='event')
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    tags = models.CharField(max_length=255, blank=True, null=True)

    longitude = models.DecimalField(decimal_places=55, max_digits=60)
    latitude = models.DecimalField(decimal_places=55, max_digits=60)
    notification_radius = models.IntegerField() #for public event only

    created = models.DateField(default = timezone.now)
    started = models.DateField(default = timezone.now)
    last = models.DateField(default = default_last)
    objects = EventManager()

    def __str__(self):
        return self.name

class Participation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participation')

    def __str__(self):
        return ''.join((str(self.event),' ', str(self.user)))
