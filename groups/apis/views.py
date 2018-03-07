from .serializers import MembershipSerializer, GroupSerializer, GroupCreateSerializer, GroupWithMembersSerializer
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.conf import settings
from django.contrib.auth import get_user_model

from groups.models import Group, Membership
from activities.models import CreateGroup
from buddychat.models import BuddyMessage
User = get_user_model()
#################################################################
#Group APIs Here....                                             #
#################################################################
class CreateGroupAPIView(APIView):
    """
        Post Params:
            name: name of the group
            description: description of the group
            image: group image (dun have for now)
            members: list of emails of the people in the group, default empty except for the owner
    """
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data= request.data
        #create a new group given the name, description, and image
        serializer = GroupSerializer(data=data)
        if(serializer.is_valid(raise_exception=True)):
            group_obj = Group(name = data.get('name'), description = data.get('description'), image= data.get('image'))
            group_obj.save()

        #associate the group with the owner and members through Membership
        owner = request.user
        if(not Membership.objects.filter(user = owner, group=group_obj).exists()):
            own_mem_obj = Membership(user = owner, group = group_obj, owner=True)
            own_mem_obj.save()

        members = data.get('members','')
        members = [item.strip() for item in members.strip().split(',')]
        for member in members:
            try:
                user_obj = User.objects.get(email = member)
            except User.DoesNotExists:
                pass
            if(not Membership.objects.filter(user = user_obj, group=group_obj).exists()):
                mem_obj = Membership(user = user_obj, group=group_obj, owner=False)
                mem_obj.save()

                #notify the group
                msg_obj = BuddyMessage(user=user_obj, group=group_obj, message=''.join((user_obj.buddycode,' joined the group')), message_type=settings.MSG_TYPE_JOIN)
                msg_obj.save()

        #create an activity for the owner
        if(not CreateGroup.objects.filter(user = owner, group = group_obj).exists()):
            activity_obj = CreateGroup(owner = owner, group = group_obj, longitude = owner.longitude, latitude = owner.latitude)
            activity_obj.save()

        return Response({"success":True}, status=HTTP_200_OK)

class RemoveGroupAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class AddUserToGroupAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = request.data
        user_to_email = data.get('user_email')
        group_id = data.get('group_id')
        user_from = request.user

        #check if the user is part of the group
        group_obj = Group.objects.get(id=group_id)
        if( not Membership.objects.filter(user=user_from, group=group_obj).exists()):
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        #add user to group if the request user exists
        try:
            user_to_obj = User.objects.get(email=user_to_email)
            mem_obj = Membership(user = user_to_obj, group=group_obj, owner=False)
            mem_obj.save()

            msg_obj = BuddyMessage(user=user_to_obj, group=group_obj, message=''.join((user_to_obj.buddycode,' joined the group')), message_type=settings.MSG_TYPE_JOIN)
            msg_obj.save()

        except User.DoesNotExists:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        #notify the group

        return Response({"success":True}, status=HTTP_200_OK)

class RemoveUserFromGroupAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = request.data
        user_to_email = data.get('user_email')
        group_id = data.get('group_id')
        user_from = request.user

        #check if the user is part of the group
        group_obj = Group.objects.get(id=group_id)
        if( not Membership.objects.filter(user=user_from, group=group_obj).exists()):
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        #add user to group if the request user exists
        try:
            user_to_obj = User.objects.get(email=user_to_email)
            mem_obj = Membership.objects.get(user = user_to_obj, group=group_obj)
            mem_obj.delete()

        except User.DoesNotExists:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        #notify the group

        return Response({"success":True}, status=HTTP_200_OK)

class GetGroupsFromUserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user
        groups = list(Group.objects.filter(members=user))
        # GroupWithMembersSerializer or GroupSerializer
        serializer_data = GroupSerializer(
            groups,
            context={"request": request},
            many = True
        ).data
        return Response({"success":True, "groups":serializer_data}, status=HTTP_200_OK)

class GetUsersInGroup(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        # data = request.GET
        # query_result = list(Friend.objects.friends(request.user))
        # friendList = UserDetailSerializer(
        #     query_result,
        #     context={"request": request},
        #     many=True,
        # ).data
        # for i in range(len(friendList)):
        #     try:
        #         locator = Locator.objects.filter(user__email=friendList[i].get('email')).latest('inited')
        #         friendList[i]['longitude'] = locator.longitude
        #         friendList[i]['latitude'] = locator.latitude
        #     except:
        #         pass
        # return Response({"success": True, "friends": friendList}, status = HTTP_200_OK)
