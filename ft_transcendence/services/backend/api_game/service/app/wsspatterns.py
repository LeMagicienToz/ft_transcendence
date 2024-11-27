from channels.routing import URLRouter
from django.urls import path
from os import environ
from .consumers import GameConsumer

wsspatterns = [
    path('wss/' + environ.get('T_SELF_NAME') + '/', URLRouter([
        path('<int:game_id>/', GameConsumer.GameConsumer.as_asgi()),
    ])),
]

