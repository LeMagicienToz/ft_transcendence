from django.urls import path
from . import views
from .views import (
    GameCreateView, GameListView, GameDetailView, GameJoinView, GameUserHistoryView, GameDeleteView,
	TournamentCreateView, TournamentListView, TournamentDetailView, TournamentJoinView,
	TournamentDeleteView, GameDeleteAllView
)

urlpatterns = [
    path('ping/', views.ping, name='ping'),
	path('test-get-user-info/', views.get_user_info, name='test'),
    path("create/", GameCreateView.as_view(), name="game-create"),     # Create game
    path("list/", GameListView.as_view(), name="game-list"),                # List all games
    path("game-details/<int:game_id>/", GameDetailView.as_view(), name="game-detail"),   # Detail one game
    path("join/<int:game_id>/", GameJoinView.as_view(), name="game-join"),  # Join a game
    path("user-history/<int:user_id>/", GameUserHistoryView.as_view(), name="user-histoty"),   # list of games played by user_id
    path("delete/<int:game_id>/", GameDeleteView.as_view(), name="game-delete"),   # Delete one game
    path("tournament/create/", TournamentCreateView.as_view(), name="tournament-create"),   # Create tournament
    path("tournament/details/<int:tournament_id>/", TournamentDetailView.as_view(), name="tournament-detail"),   # List all tournaments
    path("tournament/list/", TournamentListView.as_view(), name="tournament-list"),   # List all tournaments
    path("tournament/join/<int:tournament_id>/", TournamentJoinView.as_view(), name="tournament-join"),  # Join a tournament
    path("tournament/delete/<int:tournament_id>/", TournamentDeleteView.as_view(), name="tournament-delete"),   # Delete a tournament

    # TODO remove this
    path("delete-all/", GameDeleteAllView.as_view(), name="game-delete-all"),   # Delete all games
]
# use {% url 'game-join' id=12 %} in html
