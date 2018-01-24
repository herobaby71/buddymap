from django.db import models

class UserProfile(models.Model):
    avatar = models.CharField(max_length=100,null=True, blank=True)