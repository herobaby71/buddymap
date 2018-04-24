from django.conf.urls import url

from .views import PokeAPIView, MessageAPIView

urlpatterns = [
    url(r'^poke/$', PokeAPIView.as_view(), name='poke'),
    url(r'^message/$', MessageAPIView.as_view(), name='message'),
]
