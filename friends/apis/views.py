from django.contrib.auth import get_user_model
from friendship.models import Friend, FriendshipRequest
from friends.apis.serializers import getFriendListSerializer, getFriendRequestSerializer
from accounts.apis.serializers import UserDetailSerializer

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated
)
from maplocators.models import Locator
from maplocators.apis.serializers import LocatorsSerializer
User = get_user_model()

class getFriendListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        data = request.GET
        query_result = list(Friend.objects.friends(request.user))
        print("debug loc 1")

        friend_locs = []
        for friend in query_result:
            try:
                friend_locs.append(list(Locator.objects.filter(user=friend).order_by('-created'))[0])
            except:
                pass
        print("debug loc 2:", friend_locs)
        friendList = UserDetailSerializer(
            query_result,
            context={"request": request},
            many=True,
        ).data
        friends_loc = LocatorsSerializer(
            friend_locs,
            many=True,
            context={"request": request}
        ).data
        print("friend list:", friendList)

        for i,friend in enumerate(friends):
            try:
                friends[i]['longitude'] = friends_loc[i]['longitude']
                friends[i]['latitude'] = friends_loc[i]['latitude']
            except:
                friends[i]['longitude'] = -77.8579206738819635802428820170
                friends[i]['latitude'] = 40.799171908870782488065742654

        return Response({"success": True, "friends": friendList}, status = HTTP_200_OK)

class getFriendRequestsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        data = request.GET

        query_result = list(Friend.objects.unread_requests(user=request.user))
        # print("Query Result Get Friend Request:", query_result)
        requestList = getFriendRequestSerializer(
            query_result,
            many=True,
            context={"request": request}
        ).data

        return Response({"success": True, "requests":requestList}, status = HTTP_200_OK)

class makeFriendRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        user_to = None
        #verify user is valid
        try:
            user_email = data.get("user_email")
            user_to = User.objects.get(email=user_email)
            print("user_email:",user_email)
            print("user_to:",user_to)
        except User.DoesNotExist:
            return Response({"success": False, "error_message": "user does not exist"}, status = HTTP_400_BAD_REQUEST)

        #add friend
        try:
            Friend.objects.add_friend(
                request.user,
                user_to,
                message= 'Hi! Eat me'
            )
        except:
            return Response({"success": False, "error_message": "cannot add this user as friend"}, status = HTTP_400_BAD_REQUEST)
        return Response({"success": True}, status=HTTP_200_OK)

class removeFriendAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = request.data
        user_to = None
        #verify user is valid
        try:
            user_email = data.get("user_email")
            user_to = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return Response({"success": False, "error_message": "user does not exist"}, status = HTTP_400_BAD_REQUEST)

        #add friend
        try:
            Friend.objects.remove_friend(
                request.user,
                user_to
            )
        except:
            return Response({"success": False, "error_message": "cannot remove this user from friendlist"}, status = HTTP_400_BAD_REQUEST)
        return Response({"success": True}, status=HTTP_200_OK)

class acceptFriendRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = request.data
        friend_request = None
        #verigy FriendshipRequest is valid
        try:
            print("1st", data)
            friend_req_id = data.get("id")
            friend_request = FriendshipRequest.objects.get(id = friend_req_id)
            print("friend req:",friend_request)
        except:
            return Response({"success": False, "error_message": "friend request is no longer valid"}, status = HTTP_400_BAD_REQUEST)

        #accept friend request
        try:
            print("2nd")
            friend_request.accept()
        except:
            return Response({"success": False, "error_message": "failed to accept friend request"}, status = HTTP_400_BAD_REQUEST)
        return Response({"success": True}, status = HTTP_200_OK)

class rejectFriendRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = request.data
        friend_request = None
        #verigy FriendshipRequest is valid
        try:
            friend_req_id = data.get("id")
            friend_request = FriendshipRequest.objects.get(id = friend_req_id)
        except:
            return Response({"success": False, "error_message": "friend request is no longer valid"}, status = HTTP_400_BAD_REQUEST)

        #accept friend request
        try:
            friend_request.reject()
        except:
            return Response({"success": False, "error_message": "failed to reject friend request"}, status = HTTP_400_BAD_REQUEST)
        return Response({"success": True}, status = HTTP_200_OK)
