from django.urls import path
from . import views
from .views import (
    GameCreateView, GameListView, GameDetailView, #GameJoinView, , GameStartView,
)

urlpatterns = [
    path('ping/', views.ping, name='ping'),
    path("create/", GameCreateView.as_view(), name="game-create"),     # Créer un nouveau jeu
    path("list/", GameListView.as_view(), name="game-list"),                # Liste de tous les jeux
    path("game-details/<int:game_id>/", GameDetailView.as_view(), name="game-detail"),   # Détaille un jeu
]
    #path("join/<int:game_id>/", GameJoinView.as_view(), name="game-join"),  # Joindre un jeu
    #path("start/<int:game_id>/", GameStartView.as_view(), name="game-start"), # Démarrer un jeu
# use {% url 'game-join' id=12 %} in html
