from django.urls import path
from . import views
from .views import (
    GameCreateView, GameListView, GameDetailView, GameJoinView, GameStartView,
)

urlpatterns = [
    path('ping/', views.ping, name='ping'),
    path("create/", GameCreateView.as_view(), name="game-create"),     # Create game
    path("list/", GameListView.as_view(), name="game-list"),                # List all games
    path("game-details/<int:game_id>/", GameDetailView.as_view(), name="game-detail"),   # Detail one game
    path("join/<int:game_id>/", GameJoinView.as_view(), name="game-join"),  # Join a game
    path("start/<int:game_id>/", GameStartView.as_view(), name="game-start"), # Start a game
]
# use {% url 'game-join' id=12 %} in html
