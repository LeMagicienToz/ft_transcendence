from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import Player, Game, Tournament
from django.utils import timezone
import json
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .tournament_logic import create_round_robin_matches
import requests
import os

# decorator.py line 38 to increase cookies life
# auth/views.py 185 187

import logging
logger = logging.getLogger('myapp')

def utils_get_user_info(token, token42):
    headers = {'Content-Type': 'application/json'}
    cookies = {}
    # Use the appropriate token as a cookie
    if not token and not token42:
        return JsonResponse({'error': 'No authentication token received'}, status=401)
    if token42:
        cookies['42_access_token'] = token42
    else:
        cookies['token'] = token
    try:
        response = requests.get(
            f"{os.getenv('AUTH_SERVICE_HOST', 'http://auth-service:8000')}/get_user/",
            headers=headers,
            cookies=cookies
        )
        result = response.json()
        if (result.get('success') != True):
            return None
        return result
    except requests.exceptions.RequestException as e:
        # Log the detailed error
        return {
            'error': 'An error occurred while connecting to the authentication service.',
            'details': str(e)
        }

# keep this endpoint just for testing
@api_view(['POST'])
def get_user_info(request):
    # Retrieve tokens from request data
    token = request.COOKIES.get('token')
    token42 = request.COOKIES.get('42_access_token')
    # Check if either token is present
    if not token and not token42:
        return JsonResponse({'error': 'Missing authentication token'}, status=400)
    user_info = utils_get_user_info(token, token42)
    return JsonResponse(user_info)


def ping(request):
        """
        for testing, the serveur should reply 'pong' to 'ping'
        """
        return JsonResponse({'received': 'pong'})

class GameCreateView(APIView):
    """
    Create a new Game object
    the request must be POST
    body = {
    'game_custom_name': type string,
    'nickname': type string,
    'match_type': '1v1' or '2v2',
    'game_type': 'pong',
    'score_to_win': type int,
    'tournament_id': type int, 0 if not in a tournament,
    }
    cookie = {
    'token': type string,
    '42_access_token': type string,
    }
    """
    def post(self, request):
        # get user_id and user_name from authentification app
        token = request.COOKIES.get('token')
        token42 = request.COOKIES.get('42_access_token')
        user_info = utils_get_user_info(token, token42)
        player1_user_id = ""
        player1_user_name = ""
        if not user_info:
            return JsonResponse({'error': 'Failed to get user info'}, status=400)
        try:
            player1_user_id = user_info.get('user_id')
            player1_user_name = user_info.get('username')
        except KeyError as e:
            return JsonResponse({'error': f'Missing key in user_info: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)

        game_custom_name = request.data.get('game_custom_name')
        nickname = request.data.get('nickname', player1_user_name)
        # Data validation
        if not player1_user_id or not player1_user_name:
            return JsonResponse({'error': 'Player information is required'}, status=400)
        # create Player
        player1 = Player.objects.create(
            user_id=player1_user_id,
            user_name=player1_user_name,
            score=0,
            nickname=nickname,
            player_index=0,
            user_info=user_info,
        )
        # get game type (1 vs 1 or 2 vs 2)
        match_type = request.data.get('match_type')
        if match_type not in ['1v1', '2v2']:
            return JsonResponse({'error': 'Invalid match type'}, status=400)
        # get game name (pong or snake)
        game_type = request.data.get('game_type')
        if game_type not in ['pong']:
            return JsonResponse({'error': 'Invalid game type'}, status=400)
        # Get score to win
        try:
            score_to_win = int(request.data.get('score_to_win', 3))
        except (ValueError, TypeError):
            score_to_win = 3
        # get tournament id and check if it's valid
        try:
            tourn_id = int(request.data.get('tournament_id', 0))
            tourn = Tournament.objects.get(id=tourn_id) if tourn_id > 0 else None
            tourn_id = tourn.id if tourn else 0
        except (ValueError, TypeError, Tournament.DoesNotExist):
            tourn_id = 0
        # Game init with pLayer 1
        try:
            game = Game.objects.create(
                game_custom_name=game_custom_name,
                match_type=match_type,
                game_type=game_type,
                score_to_win=score_to_win,
                tournament_id=tourn_id,
                creation_time=timezone.now(),
                status='waiting',
            )
            game.players.add(player1)
        except Exception as e:
            return JsonResponse({'error': 'Error creating game: {}'.format(str(e))}, status=500)
        if token:
            return JsonResponse({'message': 'Game created', 'game_id': game.id, 'token': token}, status=201)
        elif token42:
            return JsonResponse({'message': 'Game created', 'game_id': game.id, 'token42': token42}, status=201)

class GameListView(APIView):
    """
    Return the list of the games
    the request must be GET and look like
    body = {}
    """
    def get(self, request):
        games = Game.objects.all()
        games_data = [
            {
                'id': game.id,
                'game_custom_name': game.game_custom_name,
                'status': game.status,
                'game_type': game.game_type,
                'match_type': game.match_type,
                'score_to_win': game.score_to_win,
                'tournament_id': game.tournament_id,
                'creation_time': game.creation_time,
                'start_time': game.start_time,
                'end_time': game.end_time,
                'players': [
                    {
                        'user_id': player.user_id,
                        'user_name': player.user_name,
                        'score': player.score,
                        'nickname': player.nickname,
                        'player_index': player.player_index,
                        'user_info': player.user_info,
                    } for player in game.players.all()
                ]
            } for game in games
        ]
        return JsonResponse(games_data, safe=False)

class GameDetailView(APIView):
    """
    return the details of a game
    the request must be GET and look like
    body = {}
    the game_id is in the url
    """
    def get(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)
        game_details = {
            'game_id': game.id,
            'game_custom_name': game.game_custom_name,
            'status': game.status,
            'game_type': game.game_type,
            'match_type': game.match_type,
            'score_to_win': game.score_to_win,
            'tournament_id': game.tournament_id,
            'creation_time': game.creation_time,
            'start_time': game.start_time,
            'end_time': game.end_time,
            'players': [
                {
                    'user_id': player.user_id,
                    'user_name': player.user_name,
                    'score': player.score,
                    'nickname': player.nickname,
                    'player_index': player.player_index,
                    'user_info': player.user_info,
                } for player in game.players.all()
            ]
        }
        return JsonResponse(game_details)

class GameJoinView(APIView):
    """
    this allow a player to join a game
    the request must be PUT
    body = {
    'nickname': type string,
    }
    cookie = {
    'token': type string,
    '42_access_token': type string,
    }
    the game_id is in the url
    """
    def put(self, request, game_id):
        # get user_id and user_name from authentification app
        token = request.COOKIES.get('token')
        token42 = request.COOKIES.get('42_access_token')
        user_info = utils_get_user_info(token, token42)
        if not user_info or not user_info.get('user_id'):
            return JsonResponse({'error': 'Failed to get user info'}, status=400)
        player_user_id = user_info['user_id']
        player_user_name = user_info['username']
        # read the JSON file from the request
        data = request.data
        nickname = data.get('nickname', player_user_name)
        # Player info validation
        if not player_user_id or not player_user_name:
            return JsonResponse({'error': 'Player information is required'}, status=400)

        # get game from id
        game = get_object_or_404(Game, id=game_id)
        # check if game is full
        player_is_in_the_game = game.players.filter(user_id=player_user_id).exists()
        if game.match_type == '1v1' and game.players.count() >= 2 and player_is_in_the_game == False:
            return JsonResponse({'message': 'Game is already full'}, status=400)
        elif game.match_type == '2v2' and game.players.count() >= 4 and player_is_in_the_game == False:
            return JsonResponse({'message': 'Game is already full'}, status=400)
        # Game must be waiting
        if game.status != 'waiting':
            return JsonResponse({'error': 'Game has already started or finished or is full'}, status=400)
        # Check if player allready in game
        if player_is_in_the_game == False:
            # create Player
            player = Player.objects.create(
                user_id=player_user_id,
                user_name=player_user_name,
                score=0,
                nickname=nickname,
                player_index=0,
                user_info=user_info,
            )
            # Assign new player
            game.players.add(player)
            game.save()
        if token:
            return JsonResponse({'message': 'Player joined', 'game_id': game.id, 'token': token}, status=201)
        elif token42:
            return JsonResponse({'message': 'Player joined', 'game_id': game.id, 'token42': token42}, status=201)

class GameUserHistoryView(APIView):
    """
    Return the list of games for a specific user, with status = finished
    the request must be GET and look like
    body = {}
    The user_id is in the URL.
    """
    def get(self, request, user_id):
        try:
            user_id = int(user_id)
        except ValueError:
            return JsonResponse({'error': 'Invalid user_id. Must be an integer.'}, status=400)
        # Filter games where used_id is in
        games = Game.objects.filter(players__user_id=user_id, status='finished')
        game_details_list = []
        for game in games:
            players = game.players.all()
            has_won = False
            # Determine if the user won based on the match type
            if game.match_type == '1v1':
                user_score = None
                opponent_score = None
                for player in players:
                    if player.user_id == user_id:
                        user_score = player.score
                    else:
                        opponent_score = player.score
                if user_score is not None and opponent_score is not None:
                    has_won = user_score >= opponent_score
            elif game.match_type == '2v2':
                user_score = None
                highest_opponent_score = None
                for player in players:
                    if player.user_id == user_id:
                        user_score = player.score
                    else:
                        if highest_opponent_score is None or player.score > highest_opponent_score:
                            highest_opponent_score = player.score
                if user_score is not None and highest_opponent_score is not None:
                    has_won = user_score >= (highest_opponent_score or 0)
            # Build the game details
            game_details = {
                'id': game.id,
                'game_custom_name': game.game_custom_name,
                'status': game.status,
                'game_type': game.game_type,
                'match_type': game.match_type,
                'score_to_win': game.score_to_win,
                'tournament_id': game.tournament_id,
                'creation_time': game.creation_time,
                'start_time': game.start_time,
                'end_time': game.end_time,
                'has_won': has_won,
                'players': [
                    {
                        'user_id': player.user_id,
                        'user_name': player.user_name,
                        'score': player.score,
                        'nickname': player.nickname,
                        'player_index': player.player_index,
                    } for player in players
                ]
            }
            game_details_list.append(game_details)
        return JsonResponse(game_details_list, safe=False)

class GameDeleteView(APIView):
    """
    Delete a game
    the request must be DELETE
    body = {}
    the game_id is in the url
    """
    def delete(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)
        game.delete()
        return JsonResponse({'message': 'Game deleted successfully'}, status=200)

class TournamentCreateView(APIView):
    """
    Create a tourament
    the request must be DELETE
    body = {
    'tournament_custom_name': type string,
    'nickname': type string,
    'match_type': '1v1' or '2v2',
    'game_type': 'pong',
    'score_to_win': type int,
    'player_count': type int,
    }
    cookie = {
    'token': type string,
    '42_access_token': type string,
    }
    """
    def post(self, request):
        # get user_id and user_name from authentification app
        token = request.COOKIES.get('token')
        token42 = request.COOKIES.get('42_access_token')
        user_info = utils_get_user_info(token, token42)
        player1_user_id = ""
        player1_user_name = ""
        if not user_info:
            return JsonResponse({'error': 'Failed to get user info'}, status=400)
        try:
            player1_user_id = user_info.get('user_id')
            player1_user_name = user_info.get('username')
        except KeyError as e:
            return JsonResponse({'error': f'Missing key in user_info: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)
        tournament_custom_name = request.data.get('tournament_custom_name')
        nickname = request.data.get('nickname', player1_user_name)
        # Data validation
        if not player1_user_id or not player1_user_name:
            return JsonResponse({'error': 'Player information is required'}, status=400)
        # create Player
        player1 = Player.objects.create(
            user_id=player1_user_id,
            user_name=player1_user_name,
            score=0,
            nickname=nickname,
            player_index=0,
            user_info=user_info,
        )
        # get game type (1 vs 1 or 2 vs 2)
        tourn_match_type = request.data.get('match_type')
        if tourn_match_type not in ['1v1', '2v2']:
            return JsonResponse({'error': 'Invalid match type'}, status=400)
        # get game type (pong or snake)
        tourn_game_type = request.data.get('game_type')
        if not tourn_game_type:
            tourn_game_type = 'pong'
        elif tourn_game_type not in ['pong', 'snake']:
            return JsonResponse({'error': 'Invalid game type'}, status=400)
        # Get score to win
        try:
            score_to_win = int(request.data.get('score_to_win', 3))
        except (ValueError, TypeError):
            score_to_win = 3
        # Get the number of players
        try:
            player_count = int(request.data.get('player_count'))
            if player_count <= 1:
                raise ValueError
            if tourn_match_type == '2v2' and (player_count <= 3 or player_count % 2 != 0):
                raise ValueError
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid number of players'}, status=400)
        # create tournament
        tournament = Tournament.objects.create(
            tournament_custom_name=tournament_custom_name,
            match_type=tourn_match_type,
            game_type=tourn_game_type,
            score_to_win=score_to_win,
            player_count=player_count,
            creation_time=timezone.now(),
            status='waiting',
        )
        tournament.players.add(player1)
        if token:
            return JsonResponse({'message': 'Tournament created', 'tournament_id': tournament.id, 'token': token}, status=201)
        elif token42:
            return JsonResponse({'message': 'Tournament created', 'tournament_id': tournament.id, 'token42': token42}, status=201)

class TournamentListView(APIView):
    """
    Return the list of the tournaments
    the request must be GET and look like
    body = {}
    """
    def get(self, request):
        tournaments = Tournament.objects.all()
        tournament_list = []
        for tournament in tournaments:
            players = [
                {
                    "user_id": player.user_id,
                    "user_name": player.user_name,
                    "score": player.score,
                    "nickname": player.nickname,
                    "player_index": player.player_index,
                    'user_info': player.user_info,
                }
                for player in tournament.players.all()
            ]
            games = [
                {
                    "id": game.id,
                    "game_custom_name": game.game_custom_name,
                    "match_type": game.match_type,
                    "game_type": game.game_type,
                    "score_to_win": game.score_to_win,
                    "tournament_id": game.tournament_id,
                    "status": game.status,
                    "creation_time": game.creation_time,
                    "start_time": game.start_time,
                    "end_time": game.end_time,
                    "players": [
                        {
                            "user_id": player.user_id,
                            "user_name": player.user_name,
                            "score": player.score,
                            "nickname": player.nickname,
                            "player_index": player.player_index,
                            'user_info': player.user_info,
                        }
                        for player in game.players.all()
                    ]
                }
                for game in tournament.games.all()
            ]
            tournament_data = {
                "id": tournament.id,
                "tournament_custom_name": tournament.tournament_custom_name,
                "match_type": tournament.match_type,
                "game_type": tournament.game_type,
                "player_count": tournament.player_count,
                "score_to_win": tournament.score_to_win,
                "status": tournament.status,
                "creation_time": tournament.creation_time,
                "start_time": tournament.start_time,
                "end_time": tournament.end_time,
                "players": players,
                "games": games
            }
            tournament_list.append(tournament_data)
        return Response(tournament_list, status=200)

class TournamentDetailView(APIView):
    """
    return the details of a tournament
    the request must be GET and look like
    body = {}
    the tournament_id is in the url
    """
    def get(self, request, tournament_id):
        tournament = get_object_or_404(Tournament, id=tournament_id)
        players = [
            {
                "user_id": player.user_id,
                "user_name": player.user_name,
                "score": player.score,
                "nickname": player.nickname,
                "player_index": player.player_index,
                'user_info': player.user_info,
            }
            for player in tournament.players.all()
        ]
        games = [
            {
                "id": game.id,
                "game_custom_name": game.game_custom_name,
                "match_type": game.match_type,
                "game_type": game.game_type,
                "score_to_win": game.score_to_win,
                "tournament_id": game.tournament_id,
                "status": game.status,
                "creation_time": game.creation_time,
                "start_time": game.start_time,
                "end_time": game.end_time,
                "players": [
                    {
                        "user_id": player.user_id,
                        "user_name": player.user_name,
                        "score": player.score,
                        "nickname": player.nickname,
                        "player_index": player.player_index,
                        'user_info': player.user_info,
                    }
                    for player in game.players.all()
                ]
            }
            for game in tournament.games.all()
        ]
        tournament_data = {
            "id": tournament.id,
            "tournament_custom_name": tournament.tournament_custom_name,
            "match_type": tournament.match_type,
            "game_type": tournament.game_type,
            "player_count": tournament.player_count,
            "score_to_win": tournament.score_to_win,
            "status": tournament.status,
            "creation_time": tournament.creation_time,
            "start_time": tournament.start_time,
            "end_time": tournament.end_time,
            "players": players,
            "games": games,
        }
        return Response(tournament_data, status=200)

class TournamentJoinView(APIView):
    """
    this allow a player to join a tournament
    the request must be PUT
    body = {
    'nickname': type string,
    }
    cookie = {
    'token': type string,
    '42_access_token': type string,
    }
    'tournament_id' is in the url.
    """
    def put(self, request, tournament_id):
        # get tournament
        tournament = get_object_or_404(Tournament, id=tournament_id)
        # check if tournament is full
        if tournament.players.count() >= tournament.player_count:
            return JsonResponse({'error': 'Tournament is already full'}, status=400)
        # tournament must be waiting
        if tournament.status != 'waiting':
            return JsonResponse({'error': 'Tournament has already started or finished'}, status=400)
        # get user_id and user_name from authentification app
        token = request.COOKIES.get('token')
        token42 = request.COOKIES.get('42_access_token')
        user_info = utils_get_user_info(token, token42)
        if not user_info:
            return JsonResponse({'error': 'Failed to get user info'}, status=400)
        player_user_id = user_info['user_id']
        player_user_name = user_info['username']
        # read the JSON file from the request
        data = request.data
        nickname = data.get('nickname', player_user_name)
        # check the player info
        if not player_user_id or not player_user_name:
            return JsonResponse({'error': 'Player information is required'}, status=400)
        # Check if player allready in tournament
        if tournament.players.filter(user_id=player_user_id).exists():
            return JsonResponse({'error': 'Player has already joined the tournament'}, status=400)
        # create Player
        player = Player.objects.create(
            user_id=player_user_id,
            user_name=player_user_name,
            score=0,
            nickname=nickname,
            player_index=0,
            user_info=user_info,
        )
        # add the player
        tournament.players.add(player)
        tournament.save()
        # Check if the number of players matches the required player_count
        player_count = tournament.players.count()
        if player_count == tournament.player_count:
            # Change tournament status to playing
            tournament.status = 'Tournament_full'
            tournament.start_time = timezone.now()
            tournament.save()
            # create the list of games
            create_round_robin_matches(tournament)
        if token:
            return JsonResponse({'message': 'Player joined the tournament', 'tournament_id': tournament.id, 'player_id': player.id, 'token': token}, status=201)
        elif token42:
            return JsonResponse({'message': 'Player joined the tournament', 'tournament_id': tournament.id, 'player_id': player.id, 'token42': token42}, status=201)

class TournamentDeleteView(APIView):
    """
    Delete a tournament
    the request must be DELETE
    body = {}
    the tournament_id is in the url
    """
    def delete(self, request, tournament_id):
        tournament = get_object_or_404(Tournament, id=tournament_id)
        tournament.delete()
        return JsonResponse({'message': 'Tournament deleted successfully'}, status=200)
