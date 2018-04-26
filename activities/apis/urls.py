from django.conf.urls import url

from .views import PokeAPIView, MessageAPIView, GetActivitiesAPIView

urlpatterns = [
    url(r'^poke/$', PokeAPIView.as_view(), name='poke'),
    url(r'^message/$', MessageAPIView.as_view(), name='message'),
    url(r'^get/activities/$', MessageAPIView.as_view(), name='get-activities'),
]
