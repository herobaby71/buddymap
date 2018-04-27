from django.contrib.auth import get_user_model
from maplocators.models import Locator
from maplocators.apis.serializers import LocatorsSerializer
from friends.apis.serializers import getFriendListSerializer, getFriendRequestSerializer

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated
)
import datetime
User = get_user_model()

class trackCurrentLocationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LocatorsSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        try:
            locator = Locator.objects.create_locator(request.user, data.get("longitude"), data.get("latitude"))
            locator.save()
        except:
            return Response({"success": False, 'error_message': "unidentified coordinate"}, status = HTTP_400_BAD_REQUEST)
        return Response({"success": True}, status = HTTP_200_OK)

class postCurrentLocationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = request.data

        user = request.user
        user.longitude = data.get("longitude")
        user.latitude = data.get("latitude")
        user.last_updated = datetime.now()
        user.save()
        return Response({"success": True}, status = HTTP_200_OK)

class getFriendListLocationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user
        friends = list(Friend.objects.friends(request.user))
        friend_locs = []
        for friend in friends:
            friend_locs.append(list(Locators.objects.filter(user=friend).order_by('-created'))[0])

        friends = UserDetailSerializer(
            query_result,
            context={"request": request},
            many=True,
        ).data
        friends_loc = LocatorsSerializer(
            friend_locs,
            many=True,
            context={"request": request}
        ).data

        for i,friend in enumerate(friends):
            friends[i]['longitude'] = friends_loc[i]['longitude']
            friends[i]['latitude'] = friends_loc[i]['latitude']

        return Response({"success": True, "friends":friends}, status = HTTP_200_OK)

class getGroupLocationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user
        friends = list(Friend.objects.friends(request.user))
        friend_locs = []
        for friend in friends:
            friend_locs.append(list(Locators.objects.filter(user=friend).order_by('-created'))[0])

        friends = UserDetailSerializer(
            query_result,
            context={"request": request},
            many=True,
        ).data
        friends_loc = LocatorsSerializer(
            friend_locs,
            many=True,
            context={"request": request}
        ).data

        for i,friend in enumerate(friends):
            friends[i]['longitude'] = friends_loc[i]['longitude']
            friends[i]['latitude'] = friends_loc[i]['latitude']

        return Response({"success": True, "friends":friends}, status = HTTP_200_OK)
