from django.urls import path
from .endpoints import endpoints

from .endpoints.endpoints import (
    GameCreateView, ListView, GameDetailView, GameJoinView, GameUserHistoryView,
	TournamentCreateView, TournamentDetailView, TournamentJoinView
)

# TODO remove this
from .endpoints.endpoints import (
    GameDeleteAllView, TournamentDeleteAllView, ListAllView
)

urlpatterns = [
    path('status/',                         endpoints.status, name='status'),

    path("create/", GameCreateView.as_view(), name="game-create"),     # Create game
    path("list/", ListView.as_view(), name="list"),                # List all 'waiting' games and tournament
    path("game-details/<int:game_id>/", GameDetailView.as_view(), name="game-detail"),   # Detail one game
    path("join/<int:game_id>/", GameJoinView.as_view(), name="game-join"),  # Join a game
    path("user-history/<int:user_id>/", GameUserHistoryView.as_view(), name="user-histoty"),   # list of games played by user_id
    path("tournament/create/", TournamentCreateView.as_view(), name="tournament-create"),   # Create tournament
    path("tournament/details/<int:tournament_id>/", TournamentDetailView.as_view(), name="tournament-detail"),   # List all tournaments
    path("tournament/join/<int:tournament_id>/", TournamentJoinView.as_view(), name="tournament-join"),  # Join a tournament

    # TODO remove this
    # path("delete/<int:game_id>/", GameDeleteView.as_view(), name="game-delete"),   # Delete one game
    # path("tournament/delete/<int:tournament_id>/", TournamentDeleteView.as_view(), name="tournament-delete"),   # Delete a tournament
    # path("delete-all/", GameDeleteAllView.as_view(), name="game-delete-all"),   # Delete all games
    # path("tournament/delete-all/", TournamentDeleteAllView.as_view(), name="tournament-delete-all"),   # Delete all tournaments
    # path("list-all/", ListAllView.as_view(), name="list-all"),                # List all games
    # path("tournament/list/", TournamentListView.as_view(), name="tournament-list"),   # List all tournaments
]
