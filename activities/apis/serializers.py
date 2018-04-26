from rest_framework import serializers
from django.contrib.auth import get_user_model
from activities.models import Poke, QuickMessage
from accounts.apis.serializers import UserDetailSerializer
import json

class PokeSerializer(serializers.ModelSerializer):
    user_from = UserDetailSerializer()
    user_to = UserDetailSerializer()
    class Meta:
        model = Poke
        fields = ('user_from', 'user_to')

class QuickMessageSerializer(serializers.ModelSerializer):
    user_from = UserDetailSerializer()
    user_to = UserDetailSerializer()
    class Meta:
        model = QuickMessage
        fields = ('user_from', 'user_to', 'message')
