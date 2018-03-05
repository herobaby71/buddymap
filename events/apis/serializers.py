from rest_framework import serializers
from groups.apis.serializers import GroupSerializer
from accounts.apis.serializers import UserDetailSerializer
from django.contrib.auth import get_user_model

from events.models import Event, Participation
import json

User = get_user_model()

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['email', 'firstName', 'lastName', 'longitude', 'latitude']

class ParticipantSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    class Meta:
        model = Participation
        fields = ('user')

class EventSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    class Meta:
        model = Event
        fields = ('group', 'name', 'description', 'started', 'exipred', 'longitude', 'latitude')
