from django.contrib.auth import get_user_model
from maplocators.models import Locator
from maplocators.apis.serializers import LocatorsSerializer

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated
)

User = get_user_model()

class postCurrentLocationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LocatorsSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        try:
            locator = Locator.objects.create_locator(request.user, data.get("longitude"), data.get("latitude"))
            locator.save()
            user.longitude = data.get("longitude")
            user.latitude = data.get("latitude")
            user.save()
        except:
            return Response({"success": False, 'error_message': "unidentified coordinate"}, status = HTTP_400_BAD_REQUEST)
        return Response({"success": True}, status = HTTP_200_OK)

class getFriendListLocationAPIView(APIView):
    pass
class getGroupLocationAPIView(APIView):
    pass
