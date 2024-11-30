from django.db import models

class PlayerModel(models.Model):

    user_id = models.IntegerField(default=0)
    user_name = models.CharField(max_length=30)
    score = models.IntegerField(default=0)
    nickname = models.CharField(max_length=30)
    player_index = models.IntegerField(default=0)
    user_info = models.JSONField(default=dict, blank=True)

    def to_array(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'score': self.score,
            'nickname': self.nickname,
            'player_index': self.player_index,
            'user_info': self.user_info,
        }

class GameModel(models.Model):

    custom_name = models.CharField(max_length=30, default="custom_name")
    score_to_win = models.IntegerField(default=3)
    players = models.ManyToManyField(PlayerModel, related_name="games")
    player_count = models.IntegerField(default = 0)
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

    def to_array(self):
        return {
            'id': self.id,
            'custom_name': self.custom_name,
            'status': self.status,
            'game_type': self.game_type,
            'match_type': self.match_type,
            "player_count": self.player_count,
            'score_to_win': self.score_to_win,
            'tournament_id': self.tournament_id,
            'ball_speed': self.ball_speed,
            'color_board': self.color_board,
            'color_ball': self.color_ball,
            'color_wall': self.color_wall,
            'color_paddle': self.color_paddle,
            'creation_time': self.creation_time,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'type': 'game',
            'joined_players_count': self.get_joined_players_count(),
            'players': [
                player.to_array()
                for player in self.players.all()
            ]
        }

    def get_joined_players_count(self):
        players_that_not_with_placeholder_username = [
            player for player in self.players.all()
            if not player.user_name.startswith("__placeholder")
        ]
        return len(players_that_not_with_placeholder_username)

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

    def is_full(self):
        return (self.get_joined_players_count() == self.player_count)

    def to_array(self):
        players = [
            player.to_array()
            for player in self.players.all()
        ]
        games = [
            game.to_array()
            for game in self.games.all().order_by('id')
        ]
        tournament_data = {
            "id": self.id,
            "custom_name": self.custom_name,
            "match_type": self.match_type,
            "game_type": self.game_type,
            "player_count": self.player_count,
            "score_to_win": self.score_to_win,
            "status": self.status,
            'ball_speed': self.ball_speed,
            'color_board': self.color_board,
            'color_ball': self.color_ball,
            'color_wall': self.color_wall,
            'color_paddle': self.color_paddle,
            "creation_time": self.creation_time,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "players": players,
            "games": games,
            "joined_players_count": self.get_joined_players_count(),
        }
        return tournament_data

    def get_joined_players_count(self):
        players_that_not_with_placeholder_username = [
            player for player in self.players.all()
            if not player.user_name.startswith("__placeholder")
        ]
        return len(players_that_not_with_placeholder_username)

    def get_placeholder_user_id(self, idx):
        return self.id * 10000000 + idx

    def get_placeholder_user_name(self, idx):
        return f"__placeholder_{idx}"

    def __str__(self):
        num_players = self.players.count()
        return (f'Tournament {self.id} (Game: {self.game_type}, Match: {self.match_type}, Players: {num_players}, Status: {self.status})')
