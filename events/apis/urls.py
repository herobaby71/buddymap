from django.conf.urls import url

from .views import GetParticipantInEventAPIView,
    CreateGroupEventAPIView, RemoveGroupEventAPIView,
    CreatePublicEventAPIView, RemovePublicEventAPIView,
    AddUserToGroupEventAPIView, RemoveUserFromGroupEventAPIView,


urlpatterns = [
    url(r'^create/group/event/$', CreateGroupEventAPIView.as_view(), name='create-group-event'),
    url(r'^remove/group/event/$', RemoveGroupEventAPIView.as_view(), name='info'),
    url(r'^create/public/event/$', CreatePublicEventAPIView.as_view(), name='create-public-event'),
    url(r'^remove/public/event/$', RemovePublicEventAPIView.as_view(), name='info'),
    url(r'^participate/$', AddUserToGroupEventAPIView.as_view(), name='participate'),
    url(r'^bailout/$', RemoveUserFromGroupEventAPIView.as_view(), name='bailout'),
    url(r'^participants/$', GetParticipantInEventAPIView.as_view(), name='participants'),
]
