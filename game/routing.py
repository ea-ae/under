from django.urls import path
from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from game.consumers import WarfareConsumer
from game.consumers import NotFoundConsumer


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/warfare', WarfareConsumer),
            url(r'^', NotFoundConsumer),
        ])
    )
})
