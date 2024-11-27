from django.http import JsonResponse
import os
import requests
from ..models import PlayerModel, GameModel, TournamentModel
from django.utils import timezone

def utils_get_user_info(token, token42):
    headers = {'Content-Type': 'application/json'}
    cookies = {}
    # Use the appropriate token as a cookie
    if not token and not token42:
        return JsonResponse({'message': 'No authentication token received'}, status=401)
    if token42:
        cookies['42_access_token'] = token42
    else:
        cookies['token'] = token
    try:
        response = requests.get(
            'http://auth:' + os.environ.get('T_PORT_INTERN_BACKEND') + '/api/auth/me',
            headers=headers,
            cookies=cookies
        )
        result = response.json()
        if (result.get('success') != True):
            return None
        result.pop('email', None)
        return result
    except requests.exceptions.RequestException as e:
        # Log the detailed error
        return {
            'message': 'An error occurred while connecting to the authentication service.',
            'details': str(e)
        }

def create_round_robin_matches(tournament):
    # Récupère les informations nécessaires du tournoi
    players = list(tournament.players.all())
    game_custom_name = "Game in " + tournament.tournament_custom_name
    tournament_id = tournament.id
    score_to_win = tournament.score_to_win
    match_type = tournament.match_type
    game_type = tournament.game_type
    ball_speed = tournament.ball_speed
    color_board = tournament.color_board
    color_ball = tournament.color_ball
    color_wall = tournament.color_wall
    color_paddle = tournament.color_paddle
    games = []

    def organize_matches(matches):
        """
        Organise les matchs pour minimiser les conflits de disponibilité des joueurs.
        """
        scheduled_matches = []
        while matches:
            block = []
            used_players = set()
            remaining_matches = []
            for match in matches:
                # Si aucun joueur du match n'est déjà utilisé, on peut le programmer dans ce bloc
                if not used_players.intersection(match):
                    block.append(match)
                    used_players.update(match)
                else:
                    remaining_matches.append(match)
            scheduled_matches.append(block)
            matches = remaining_matches
        return scheduled_matches

    if match_type == '1v1':
        # Mode 1v1 : chaque joueur affronte chaque autre joueur une fois
        matches = [(players[i], players[j]) for i in range(len(players)) for j in range(i + 1, len(players))]
        # Organise les matchs en blocs indépendants
        organized_matches = organize_matches(matches)

        for block in organized_matches:
            for player1, player2 in block:
                game = GameModel(
                    game_custom_name=game_custom_name,
                    match_type=match_type,
                    game_type=game_type,
                    score_to_win=score_to_win,
                    tournament_id=tournament_id,
                    ball_speed=ball_speed,
                    color_board=color_board,
                    color_ball=color_ball,
                    color_wall=color_wall,
                    color_paddle=color_paddle,
                    status='waiting'
                )
                game.save()
                # Clone les joueurs pour le jeu
                player1_clone = PlayerModel.objects.create(
                    user_id=player1.user_id,
                    user_name=player1.user_name,
                    score=0,
                    nickname=player1.nickname,
                    player_index=player1.player_index
                )
                player2_clone = PlayerModel.objects.create(
                    user_id=player2.user_id,
                    user_name=player2.user_name,
                    score=0,
                    nickname=player2.nickname,
                    player_index=player2.player_index
                )
                game.players.add(player1_clone, player2_clone)
                games.append(game)
    elif match_type == '2v2':
        # Mode 2v2 : création d'équipes et affrontements entre équipes
        if len(players) % 2 != 0:
            raise ValueError("The number of players must be even for 2v2 matches.")
        teams = [(players[i], players[i + 1]) for i in range(0, len(players), 2)]
        matches = [(teams[i], teams[j]) for i in range(len(teams)) for j in range(i + 1, len(teams))]
        # Organise les matchs en blocs indépendants
        organized_matches = organize_matches(matches)

        for block in organized_matches:
            for (team1_player1, team1_player2), (team2_player1, team2_player2) in block:
                game = GameModel(
                    game_custom_name=game_custom_name,
                    match_type=match_type,
                    game_type=game_type,
                    score_to_win=score_to_win,
                    tournament_id=tournament_id,
                    status='waiting'
                )
                game.save()
                # Clone les joueurs pour le jeu
                t1p1_clone = PlayerModel.objects.create(
                    user_id=team1_player1.user_id,
                    user_name=team1_player1.user_name,
                    score=0,
                    nickname=team1_player1.nickname,
                    player_index=team1_player1.player_index
                )
                t1p2_clone = PlayerModel.objects.create(
                    user_id=team1_player2.user_id,
                    user_name=team1_player2.user_name,
                    score=0,
                    nickname=team1_player2.nickname,
                    player_index=team1_player2.player_index
                )
                t2p1_clone = PlayerModel.objects.create(
                    user_id=team2_player1.user_id,
                    user_name=team2_player1.user_name,
                    score=0,
                    nickname=team2_player1.nickname,
                    player_index=team2_player1.player_index
                )
                t2p2_clone = PlayerModel.objects.create(
                    user_id=team2_player2.user_id,
                    user_name=team2_player2.user_name,
                    score=0,
                    nickname=team2_player2.nickname,
                    player_index=team2_player2.player_index
                )
                game.players.add(t1p1_clone, t1p2_clone, t2p1_clone, t2p2_clone)
                games.append(game)

    # Ajoute tous les jeux au tournoi
    tournament.games.set(games)
    tournament.status = 'playing'
    tournament.start_time = timezone.now()
    tournament.save()
