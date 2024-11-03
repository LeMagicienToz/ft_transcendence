from django.db import models
from django.utils import timezone

class Game(models.Model):
    player1_user_id = models.IntegerField(default=0)
    player1_user_name = models.CharField(default="Player1", max_length=30)
    player1_score = models.IntegerField(default=0)
    player1_nickname = models.CharField(default="Player1", max_length=30)

    player2_user_id = models.IntegerField(default=0)
    player2_user_name = models.CharField(default="Player2", max_length=30)
    player2_score = models.IntegerField(default=0)
    player2_nickname = models.CharField(default="Player2", max_length=30)

    player3_user_id = models.IntegerField(default=0)
    player3_user_name = models.CharField(default="Player3", max_length=30)
    player3_score = models.IntegerField(default=0)
    player3_nickname = models.CharField(default="Player3", max_length=30)

    player4_user_id = models.IntegerField(default=0)
    player4_user_name = models.CharField(default="Player4", max_length=30)
    player4_score = models.IntegerField(default=0)
    player4_nickname = models.CharField(default="Player4", max_length=30)

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
        return f'Game (Type: {self.game_type}, Status: {self.status})'
