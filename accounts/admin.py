from django.contrib import admin
from django.contrib.auth import get_user_model
from accounts.models import *

admin.site.register(get_user_model())