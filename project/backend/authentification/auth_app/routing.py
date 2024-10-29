from django.urls import path
from . import consumers

websocket_urlpatterns = [
        path('ws/user_connection/', consumers.User_connection.as_asgi()),
        ]