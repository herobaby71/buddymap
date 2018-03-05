from django.contrib import admin
from activities.models import Activity, Poke, CreateGroup, CreateEvent

admin.site.register(Activity)
admin.site.register(Poke)
admin.site.register(CreateGroup)
admin.site.register(CreateEvent)
