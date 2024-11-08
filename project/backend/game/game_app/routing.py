from django.urls import re_path
from .consumers import Consumer

# all the ws/game/number/ will redirect to the class Consumer in consumers.py with game_id=number
websocket_urlpatterns = [
    re_path(r"ws/game/(?P<game_id>\d+)/$", Consumer.as_asgi()),
]
