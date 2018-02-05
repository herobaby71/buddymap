from channels.routing import ProtocolTypeRouter

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url("^front(end)/$", consumers.AsyncChatConsumer),
        ])
    ),
})
