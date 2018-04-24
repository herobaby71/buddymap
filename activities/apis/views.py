from .serializers import PokeSerializer
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
from activities.models import Activity, Poke
User = get_user_model()


################################################################
#Check all Users participating in the event
################################################################
class PokeAPIView(APIView):
    """
      Post Params:
        user_to (email)
      Process:
        add a poke instance and notify user_to
      Return:
        200 (participations json) or 400
    """
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = request.data
        user_from = request.user
        user_to=data.get('user_to')
        try:
            user_to=list(User.objects.filter(email=user_to))[0]
        except User.DoesNotExist:
            return esponse({"success":False, "message":"User does not exists!"})
        pk_obj = Poke.objects.create(user_from=user_from, user_to=user_to, longitude=user_from.longitude, latitude=user_from.latitude)
        pk_obj.save()
        return Response({"success":True, "message":""})
