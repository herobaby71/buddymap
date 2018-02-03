from .serializers import MembershipSerializer, GroupSerializer, GroupMembershipSerializer
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

from django.contrib.auth import get_user_model
User = get_user_model()
#################################################################
#Group APIs Here....                                             #
#################################################################
class CreateGroupAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class RemoveGroupAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class AddUserToGroupAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class RemoveUserFromGroupAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class GetGroupsFromUserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class GetUsersInGroup(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
