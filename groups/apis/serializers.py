from rest_framework import serializers
from django.contrib.auth import get_user_model
from groups.models import Membership, Group
from accounts.apis.serializers import UserDetailSerializer
################################################################
# AUTHENTICATION SERIALIZER
################################################################
#user = UserDetaukSerializer(read_only=True)
User = get_user_model()

class GroupMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id','name', 'image']

class MembershipSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    group = GroupMembershipSerializer()
    class Meta:
        model = Membership
        fields = ['user', 'group', 'owner', 'date_joined']

class GroupSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    members = UserDetailSerializer(many=True)
    def get_image(self, group):
        request = self.context.get('request')
        image_url = group.avatar.url
        return request.build_absolute_uri(image_url)
    class Meta:
        model = User
        fields = ['name', 'image', 'members']
