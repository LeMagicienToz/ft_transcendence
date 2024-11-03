"""
from django.urls import re_path
from .gameConsumer import GameConsumer

websocket_urlpatterns = [
    re_path(r"ws/games/(?P<game_id>\d+)/$", GameConsumer.as_asgi()),
]
"""
