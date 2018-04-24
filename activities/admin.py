from django.contrib import admin
from activities.models import Activity, Poke, CreateGroup, CreateEvent, QuickMessage

admin.site.register(Poke)
admin.site.register(QuickMessage)
admin.site.register(CreateGroup)
admin.site.register(CreateEvent)
