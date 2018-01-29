from django.conf.urls import url

from .views import postCurrentLocationAPIView
urlpatterns = [
    url(r'^update/$', postCurrentLocationAPIView.as_view(), name='update'),
]
