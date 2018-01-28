from django.conf.urls import url

from .views import getFriendListAPIView, getFriendRequestsAPIView, makeFriendRequestAPIView, removeFriendAPIView, acceptFriendRequestAPIView, rejectFriendRequestAPIView
urlpatterns = [
    url(r'^get-friend-list/$', getFriendListAPIView.as_view(), name='get-friend-list'),
    url(r'^get-friend-requests/$', getFriendRequestsAPIView.as_view(), name='get-friend-requests'),
    url(r'^add/$', makeFriendRequestAPIView.as_view(), name='add'),
    url(r'^remove/$', removeFriendAPIView.as_view(), name='remove'),
    url(r'^accept/$', acceptFriendRequestAPIView.as_view(), name='accept'),
    url(r'^reject/$', rejectFriendRequestAPIView.as_view(), name='reject'),
]
