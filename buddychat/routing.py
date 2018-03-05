from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from buddymap.mixins import QueryAuthMiddleware
from channels.sessions import SessionMiddlewareStack

####FIX THE ERROR IN THE CONSUMERS
from buddychat.consumers import EchoConsumer, ChatConsumer

application = ProtocolTypeRouter({
    "websocket":SessionMiddlewareStack(
        QueryAuthMiddleware(
            URLRouter([
                url("^chat/echo/$", EchoConsumer),
                url("^chat/stream/$", ChatConsumer),
            ])
        )
    )
})
