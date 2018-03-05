from django.conf.urls import url

from .views import PokeAPIView

urlpatterns = [
    url(r'^poke/$', PokeAPIView.as_view(), name='poke'),
]
