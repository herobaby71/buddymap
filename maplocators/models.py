from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()
class LocatorManager(models.Manager):
    def create_locator(self, user, longitude, latitude):
        locator = self.create(user= user, longitude=longitude, latitude=latitude)
        return locator
class Locator(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='locators')
    longitude = models.DecimalField(decimal_places=55, max_digits=60, null = True, blank = True)
    latitude = models.DecimalField(decimal_places=55, max_digits=60, null=True, blank = True)
    created = models.DateField(default = timezone.now)
    inited = models.DateTimeField(default = timezone.now)
    objects = LocatorManager()
