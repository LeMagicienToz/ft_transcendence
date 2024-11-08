from django.urls import re_path
from .consumers import Consumer

websocket_urlpatterns = [
    re_path(r"ws/game/(?P<game_id>\d+)/$", Consumer.as_asgi()),
]
