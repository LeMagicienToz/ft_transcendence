from django.db import models
from django.utils import timezone

class Player(models.Model):
    user_id = models.IntegerField(default=0)
    user_name = models.CharField(max_length=30)
    score = models.IntegerField(default=0)
    nickname = models.CharField(max_length=30)
    player_index = models.IntegerField(default=0)
    user_info = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return (f'Player {self.nickname} (ID: {self.user_id}, Username: {self.user_name}, Score: {self.score})')

class Game(models.Model):
    game_custom_name = models.CharField(max_length=30, default="game_custom_name")
    score_to_win = models.IntegerField(default=3)
    players = models.ManyToManyField(Player, related_name="games")
    match_type = models.CharField(
        max_length=10,
        choices=[("1v1", "1 vs 1"), ("2v2", "2 vs 2")],
        default="1v1"
    )
    game_type = models.CharField(
        max_length=20,
        choices=[("pong", "Pong"), ("snake", "Snake")],
        default="pong"
    )
    status = models.CharField(
        max_length=20,
        choices=[("waiting", "Waiting for all the players"),
                  ("playing", "Game in progress"), ("ready_to_play", "Ready to play"), ("finished", "Game finished")],
        default="waiting"
    )
    tournament_id = models.IntegerField(default = 0)
    creation_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def is_full(self):
        indexes = list(self.players.values_list('player_index', flat=True))
        # Count indexes that are not zero
        joined_players_number = sum(1 for index in indexes if index != 0)

        if (self.match_type == '1v1' and joined_players_number == 2):
            return True
        if (self.match_type == '2v2' and joined_players_number == 4):
            return True
        return False

    def update_player_two_score(self, score):
        # Loop through all players in the game
        players = self.players.all()
        for player in players:
            # Check if the player's index is even
            if player.player_index % 2 == 0:
                # Update the score
                player.score = score
                # Save the player object to the database
                player.save()

    def update_player_one_score(self, score):
        # Loop through all players in the game
        players = self.players.all()
        for player in players:
            # Check if the player's index is even
            if player.player_index % 2 == 1:
                # Update the score
                player.score = score
                # Save the player object to the database
                player.save()

    def __str__(self):
        return (f'Game {self.id} (Type: {self.game_type}, Match: {self.match_type}, Status: {self.status})')

class Tournament(models.Model):
    tournament_custom_name = models.CharField(max_length=30, default="tournament_custom_name")
    score_to_win = models.IntegerField(default=3)
    player_count = models.IntegerField(default = 0)
    players = models.ManyToManyField(Player, related_name="tournaments")
    games = models.ManyToManyField(Game, related_name="tournaments")
    match_type = models.CharField(
        max_length=10,
        choices=[("1v1", "1 vs 1"), ("2v2", "2 vs 2")],
        default="1v1"
    )
    game_type = models.CharField(
        max_length=20,
        choices=[("pong", "Pong"), ("snake", "Snake")],
        default="pong"
    )
    status = models.CharField(
        max_length=20,
        choices=[("waiting", "Waiting for all the players"),
                  ("playing", "Game in progress"), ("finished", "Game finished")],
        default="waiting"
    )
    creation_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        num_players = self.players.count()
        return (f'Tournament {self.id} (Game: {self.game_type}, Match: {self.match_type}, Players: {num_players}, Status: {self.status})')
