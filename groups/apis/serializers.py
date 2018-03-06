from rest_framework import serializers
from django.contrib.auth import get_user_model
from groups.models import Membership, Group
from accounts.apis.serializers import UserDetailSerializer
################################################################
# AUTHENTICATION SERIALIZER
################################################################
#user = UserDetaukSerializer(read_only=True)
User = get_user_model()

class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name','description', 'image']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id','name','description', 'image']

class MembershipSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    group = GroupSerializer()
    class Meta:
        model = Membership
        fields = ['user', 'group', 'owner', 'date_joined']

class GroupWithMembersSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    members = UserDetailSerializer(many=True)
    def get_image(self, group):
        request = self.context.get('request')
        image = group.image
        if(image):
            return request.build_absolute_uri(image.url)
        return None
    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'image', 'members']
