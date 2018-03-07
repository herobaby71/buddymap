# from .serializers import MembershipSerializer, GroupSerializer, GroupCreateSerializer, GroupWithMembersSerializer
# from rest_framework.views import APIView
# from rest_framework.generics import (
#     CreateAPIView,
#     DestroyAPIView,
#     UpdateAPIView,
#     ListAPIView,
#     RetrieveAPIView,
#     RetrieveUpdateAPIView
# )
# from rest_framework.permissions import (
#     AllowAny,
#     IsAuthenticated,
#     IsAdminUser,
#     IsAuthenticatedOrReadOnly
# )
# from rest_framework.response import Response
# from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
# from django.conf import settings
# from django.contrib.auth import get_user_model
#
# from buddychat.models import BuddyMessage
# User = get_user_model()
# #################################################################
# #BuddyChat APIs Here....
# #################################################################
#
# class GetGroupsFromUserAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request, *args, **kwargs):
#         user = request.user
#         messages = BuddyMessage.objects.filter(group_id=group)
#         # GroupWithMembersSerializer or GroupSerializer
#         serializer_data = GroupSerializer(
#             groups,
#             context={"request": request},
#             many = True
#         ).data
#         return Response({"success":True, "groups":serializer_data}, status=HTTP_200_OK)
