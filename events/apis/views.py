
from .serializers import ParticipantSerializer, EventSerializer
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
from events.models import Event, Participation
User = get_user_model()


################################################################
#Check all Users participating in the event
################################################################
class GetParticipantInEventAPIView(APIView):
    """
      Post Params:
        event_id
      Process:
        check if the user is in the group that hosted the event (ignore if public)
        get all Participation object
      Return:
        200 (participations json) or 400
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class AddUserToEventAPIView(APIView):
    """
      Post Params:
        event_id, user_email
      Process:
        create an Participation object
      Return:
        200 or 400
    """
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class RemoveUserFromEventAPIView(APIView):
    """
      Post Params:
        event_id, user_email
      Process:
        remove an Event object
      Return:
        200 or 400
    """
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class ReportEventAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

#################################################################
#Group Event APIs Here....                                             #
#################################################################
class CreateGroupEventAPIView(APIView):
    """
      Post Params:
        user_email, group_id, name, description, started, exipred, longitude, latitude
      Process:
        create an Activity that keep track of the user who create the group event
        create an Event object and notify group members
      Return:
        200 or 400
    """
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class RemoveGroupEventAPIView(APIView):
    """
      Post Params:
        event_id, user_email, group_id
      Process:
        make sure that the user created the event
        create an Activity that keep track of the user who remove it
        remove an Event object and notify group members
      Return:
        200 or 400
    """
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


##################################################################
#Public Event APIs Here...
##################################################################
class CreatePublicEventAPIView(APIView):
    """
      Post Params:
        user_email, name, description, started, exipred, longitude, latitude, notification_radius
      Process:
        create an Activity that keep track of the user who created it
        create an Event object and notify everyone within radius
      Return:
        200 or 400
    """
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class RemovePublicEventAPIView(APIView):
    """
      Post Params:
        event_id, user_email
      Process:
        check if the user is the creator of the event
        create an activity indicate that the user remove the event
        set the event to expire and notify everyone in the radius
      Return:
        200 or 400
    """
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
