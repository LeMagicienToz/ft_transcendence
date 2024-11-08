from django.db import models
from django.utils import timezone

class Player(models.Model):
    user_id = models.IntegerField(default=0)
    user_name = models.CharField(max_length=30)
    score = models.IntegerField(default=0)
    nickname = models.CharField(max_length=30)

    def __str__(self):
        return (f'Player {self.nickname} (ID: {self.user_id}, Username: {self.user_name}, Score: {self.score})')

class Game(models.Model):
    game_custom_name = models.CharField(max_length=30)
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
                  ("playing", "Game in progress"), ("finished", "Game finished")],
        default="waiting"
    )
    tournament_id = models.IntegerField(default = 0)
    creation_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return (f'Game {self.id} (Type: {self.game_type}, Match: {self.match_type}, Status: {self.status})')

class Tournament(models.Model):
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
