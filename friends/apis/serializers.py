from rest_framework import serializers
import json
from friendship.models import Friend, FriendshipRequest
from accounts.apis.serializers import UserDetailSerializer
################################################################################
#Friend Serialziers :)
################################################################################

class getFriendListSerializer(serializers.ModelSerializer):
    to_user = UserDetailSerializer()
    class Meta:
        model = Friend
        fields = ('to_user', 'created')

class getFriendRequestSerializer(serializers.ModelSerializer):
    to_user = UserDetailSerializer()
    from_user = UserDetailSerializer()
    class Meta:
        model = FriendshipRequest
        fields = ('id','from_user','to_user', 'created', 'message')
