from django.db import models
from django.contrib.auth import get_user_model
from members.models import Member

class Group(models.Model):
    name = models.CharField(max_length=128)
    image = models.CharField(max_length = 500)
    members = models.ManyToManyField(Member, through= 'Membership')

    def __str__(self):
        return self.name

class Membership(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField(default = timezone.now)
