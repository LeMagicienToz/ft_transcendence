from django.db import models

class PlayerModel(models.Model):

    user_id = models.IntegerField(default=0)
    user_name = models.CharField(max_length=30)
    score = models.IntegerField(default=0)
    nickname = models.CharField(max_length=30)
    player_index = models.IntegerField(default=0)
    user_info = models.JSONField(default=dict, blank=True)

class GameModel(models.Model):

    custom_name = models.CharField(max_length=30, default="custom_name")
    score_to_win = models.IntegerField(default=3)
    players = models.ManyToManyField(PlayerModel, related_name="games")
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
                  ("playing", "Game in progress"), ("ready_to_play", "Ready to play"), ("abandoned", "Game abandoned"), ("finished", "Game finished")],
        default="waiting"
    )
    tournament_id = models.IntegerField(default=0)
    ball_speed = models.FloatField(default=1.0)
    color_board = models.CharField(max_length=7, default="#ffffff")
    color_ball = models.CharField(max_length=7, default="#e48d2d")
    color_wall = models.CharField(max_length=7, default="#e48d2d")
    color_paddle = models.CharField(max_length=7, default="#ffffff")
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

    def make_the_other_player_win(self, player_who_quit):
        # Loop through all players in the game
        players = self.players.all()
        the_other_players = [
                    player for player in players
                    if player.user_id != player_who_quit.user_id
                ]
        the_other_player = the_other_players[0]
        the_other_player.score = self.score_to_win
        the_other_player.save()

class TournamentModel(models.Model):

    custom_name = models.CharField(max_length=30, default="custom_name")
    score_to_win = models.IntegerField(default=3)
    player_count = models.IntegerField(default = 0)
    players = models.ManyToManyField(PlayerModel, related_name="tournaments")
    games = models.ManyToManyField(GameModel, related_name="tournaments")
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
    ball_speed = models.FloatField(default=1.0)
    color_board = models.CharField(max_length=7, default="#FFFFFF")
    color_ball = models.CharField(max_length=7, default="#E48D2D")
    color_wall = models.CharField(max_length=7, default="#E48D2D")
    color_paddle = models.CharField(max_length=7, default="#FFFFFF")
    creation_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        num_players = self.players.count()
        return (f'Tournament {self.id} (Game: {self.game_type}, Match: {self.match_type}, Players: {num_players}, Status: {self.status})')
