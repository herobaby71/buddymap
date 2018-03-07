from rest_framework import serializers
from django.contrib.auth import get_user_model
from buddychat.models import BuddyMessage
from groups.models import Group
from accounts.apis.serializers import UserDetailSerializer
################################################################
# AUTHENTICATION SERIALIZER
################################################################
#user = UserDetaukSerializer(read_only=True)
User = get_user_model()

class MessageUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['buddycode','firstName','lastName']

class MessageGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields = ['id']

class BuddyMessageSerializer(serializers.ModelSerializer):
    user = MessageUserSerializer()
    group = MessageGroupSerializer()
    class Meta:
        model = Group
        fields = ['user','group', 'message', 'message_type']
