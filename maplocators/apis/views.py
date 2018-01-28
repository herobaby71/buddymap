from django.contrib.auth import get_user_model
from friendship.models import Friend, FriendshipRequest, getFriendRequestSerializer
from friendship.apis.serializers import getFriendListSerializer

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated
)

User = get_user_model()

class postCurrentLocationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = request.data

        print("Query Result Get Friend:", query_result)
        friendList = getFriendListSerializer(
            query_result,
            many=True,
        ).data
        return Response({"success": True}, status = HTTP_200_OK)
