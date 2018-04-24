from .serializers import UserCreateSerializer, UserLoginSerializer, UserDetailSerializer
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



#################################################################
#User APIs Here....                                             #
#################################################################
class verifyCredentialsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return Response({"success": True}, status = HTTP_200_OK)

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = get_user_model().objects.all()

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if(serializer.is_valid(raise_exception=True)):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class getUserInfoAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer_data = UserDetailSerializer(
            user,
            context={"request": request}
        ).data
        return Response({"success": True, "user":serializer_data}, status = HTTP_200_OK)

class ChangeUserStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        try:
            user.status = data.get("status")
            user.save()
        except:
            return Response({"success": False, 'error_message': "status not valid"}, status = HTTP_400_BAD_REQUEST)
        return Response({"success": True}, status = HTTP_200_OK)
