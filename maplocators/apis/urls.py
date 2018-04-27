from django.conf.urls import url

from .views import postCurrentLocationAPIView, trackCurrentLocationAPIView, getFriendListLocationAPIView
urlpatterns = [
    url(r'^update/$', postCurrentLocationAPIView.as_view(), name='update'),
    url(r'^track/$', trackCurrentLocationAPIView.as_view(), name='track'),
    url(r'^get-friend-locations/$', getFriendListLocationAPIView.as_view(), name='pal-loc'),

]
