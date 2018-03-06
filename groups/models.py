from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()
class Group(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=255, default="awesome group")
    image = models.ImageField(upload_to=settings.GROUP_IMAGES_DIR, null = True, blank = True)
    members = models.ManyToManyField(User, through= 'Membership', through_fields= ('group', 'user'))

    def __str__(self):
        return self.name

    @property
    def group_name(self):
        """
          Returns the Channels Group name that sockets should subscribe to to get sent
          messages as they are generated.
        """
        return "group-%s" % self.id
class Membership(models.Model):
    group   = models.ForeignKey(Group, on_delete = models.CASCADE)
    user    = models.ForeignKey(User, on_delete = models.CASCADE)
    owner   = models.BooleanField(default = True)
    date_joined = models.DateField(default = timezone.now)
