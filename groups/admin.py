from django.contrib import admin
from groups.models import Group, Membership

admin.site.register(Group)
admin.site.register(Membership)
