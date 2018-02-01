from django.conf.urls import url

from .views import postCurrentLocationAPIView, trackCurrentLocationAPIView
urlpatterns = [
    url(r'^update/$', postCurrentLocationAPIView.as_view(), name='update'),
    url(r'^track/$', trackCurrentLocationAPIView.as_view(), name='track')
]
