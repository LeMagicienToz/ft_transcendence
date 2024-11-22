from django.urls import path
from .consumers import User_connection

websocket_urlpatterns = [
        path('ws/user_connection/', User_connection.as_asgi()),
]