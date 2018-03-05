from rest_framework import serializers
from django.contrib.auth import get_user_model
from activities.models import Poke
from accounts.apis.serializers import UserDetailSerializer
import json

class PokeSerializer(serializers.ModelSerializer):
    user_from = UserDetailSerializer()
    user_to = UserDetailSerializer()
    class Meta:
        model = Poke
        fields = ('user_from', 'user_to')
