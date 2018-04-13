from django.conf.urls import url
from buddymap.mixins import QueryAuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack

from buddychat.consumers import EchoConsumer, ChatConsumer
from buddylocator.consumers import LocatorConsumer

application = ProtocolTypeRouter({
    "websocket":SessionMiddlewareStack(
        QueryAuthMiddleware(
            URLRouter([
                url("^chat/echo/$", EchoConsumer),
                url("^chat/stream/$", ChatConsumer),
                url("^locator/stream/$", LocatorConsumer)
            ])
        )
    )
})
