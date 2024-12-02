from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
import json
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import requests
import os

from .endpoints_utils import *
from ..models import GameModel, PlayerModel, TournamentModel

### STATUS #####################################################

@require_GET
def status(request):
    return JsonResponse({'success': 'OK'})

################################################################



class GameCreateView(APIView):
    """
    Create a new Game object
    the request must be POST
    body = {
    'custom_name': type string,
    'nickname': type string,
    'match_type': '1v1' or '2v2',
    'game_type': 'pong',
    'score_to_win': type int,
    'tournament_id': type int, 0 if not in a tournament,
    'ball_speed': type float, (optional)
    'color_board': type string, (optional)
    'color_ball': type string, (optional)
    'color_wall': type string, (optional)
    'color_paddle': type string, (optional)
    }
    cookie = {
    'token': type string,
    '42_access_token': type string,
    } one token must be valid
    """
    def post(self, request):
        # get user_id and user_name from authentification app
        token = request.COOKIES.get('token')
        refresh_token = request.COOKIES.get('refresh_token')
        token42 = request.COOKIES.get('42_access_token')
        user_info = utils_get_user_info(token, token42, refresh_token)
        player1_user_id = ""
        player1_user_name = ""
        if not user_info:
            return JsonResponse({'success': False,'message': 'Failed to get user info'}, status=400)
        try:
            player1_user_id = user_info.get('user_id')
            player1_user_name = user_info.get('username')
        except KeyError as e:
            return JsonResponse({'success': False,'message': f'Missing key in user_info: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False,'message': f'An unexpected error occurred: {str(e)}'}, status=500)

        custom_name = request.data.get('custom_name')
        nickname = request.data.get('nickname', player1_user_name)
        # Data validation
        if not player1_user_id or not player1_user_name:
            return JsonResponse({'success': False,'message': 'Player information is required'}, status=400)
        # create Player
        player1 = PlayerModel.objects.create(
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
            return JsonResponse({'success': False,'message': 'Invalid match type'}, status=400)
        if match_type == '1v1':
            player_count = 2
        elif match_type == '2v2':
            player_count = 4
        # get game name (pong or snake)
        game_type = request.data.get('game_type')
        if game_type not in ['pong']:
            return JsonResponse({'success': False,'message': 'Invalid game type'}, status=400)
        # Get score to win
        try:
            score_to_win = int(request.data.get('score_to_win', 3))
        except (ValueError, TypeError):
            score_to_win = 3
        # get tournament id and check if it's valid
        try:
            tourn_id = int(request.data.get('tournament_id', 0))
            tourn = TournamentModel.objects.get(id=tourn_id) if tourn_id > 0 else None
            tourn_id = tourn.id if tourn else 0
        except (ValueError, TypeError, TournamentModel.DoesNotExist):
            tourn_id = 0
        # Get game customization parameters
        try:
            ball_speed = float(request.data.get('ball_speed', 1.0))
            color_board = request.data.get('color_board', '#000000')
            color_ball = request.data.get('color_ball', '#e48d2d')
            color_wall = request.data.get('color_wall', '#e48d2d')
            color_paddle = request.data.get('color_paddle', '#ffffff')
        except ValueError as e:
            return JsonResponse({'error': f'Invalid value for customization parameter: {str(e)}'}, status=400)
        # Validate customization parameters
        if not (0.5 <= ball_speed <= 2.5):
            return JsonResponse({'error': 'Ball speed must be between 0.5 and 2.5'}, status=400)
        # Game init with pLayer 1
        try:
            game = GameModel.objects.create(
                custom_name=custom_name,
                match_type=match_type,
                game_type=game_type,
                score_to_win=score_to_win,
                player_count=player_count,
                tournament_id=tourn_id,
                ball_speed=ball_speed,
                color_board=color_board,
                color_ball=color_ball,
                color_wall=color_wall,
                color_paddle=color_paddle,
                creation_time=timezone.now(),
                status='waiting',
            )
            game.players.add(player1)
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Error creating game: {}'.format(str(e))}, status=500)
        return JsonResponse({'success': True, 'message': 'Game created', 'game_id': game.id, 'list_id': [game.id]}, status=200)

class ListView(APIView):
    """
    Return a single 'games' array containing both games and tournaments in a single response.
    The request must be GET.
    """
    def get(self, request):
        # Récupération des données des jeux
        games = GameModel.objects.filter(tournament_id=0, status='waiting')
        games_data = [
            game.to_array() for game in games
        ]

        tournaments = TournamentModel.objects.filter(status='waiting')
        tournaments_data = [
            tournament.to_array()
            for tournament in tournaments
        ]

        combined_data = games_data + tournaments_data

        response_data = {
            'success': True,
            'games': combined_data
        }

        return JsonResponse(response_data, safe=False)

# TODO remove before push
class ListAllView(APIView):
    """
    Return a single 'games' array containing both games and tournaments in a single response.
    The request must be GET.
    """
    def get(self, request):
        # Récupération des données des jeux
        games = GameModel.objects.filter(tournament_id=0)
        games_data = [
            game.to_array()
            for game in games
        ]
        tournaments = TournamentModel.objects.all()
        tournaments_data = [
            tournament.to_array()
            for tournament in tournaments
        ]
        combined_data = games_data + tournaments_data
        response_data = {
            'success': True,
            'games': combined_data
        }
        return JsonResponse(response_data, safe=False)

class GameDetailView(APIView):
    """
    return the details of a game
    the request must be GET and look like
    body = {}
    the game_id is in the url
    """
    def get(self, request, game_id):
        game = get_object_or_404(GameModel, id=game_id)
        game_details = game.to_array()
        return JsonResponse({'success': True, 'game': game_details})

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
        refresh_token = request.COOKIES.get('refresh_token')
        token42 = request.COOKIES.get('42_access_token')
        user_info = utils_get_user_info(token, token42, refresh_token)
        if not user_info:
            return JsonResponse({'success': False, 'message': 'Failed to get user info'}, status=400)
        player_user_id = user_info['user_id']
        player_user_name = user_info['username']
        # read the JSON file from the request
        data = request.data
        nickname = data.get('nickname', player_user_name)
        # Player info validation
        if not player_user_id or not player_user_name:
            return JsonResponse({'success': False, 'message': 'Player information is required'}, status=400)
        # get game from id
        game = get_object_or_404(GameModel, id=game_id)
        # Check if player allready in game
        if game.players.filter(user_id=player_user_id).exists():
            return JsonResponse({'success': False, 'message': 'Player has already joined the game'}, status=400)
        # check if game is full
        if game.match_type == '1v1' and game.players.count() >= 2:
            return JsonResponse({'success': False, 'message': 'Game is already full'}, status=400)
        elif game.match_type == '2v2' and game.players.count() >= 4:
            return JsonResponse({'success': False, 'message': 'Game is already full'}, status=400)
        # Game must be waiting
        if game.status != 'waiting':
            return JsonResponse({'success': False, 'message': 'Game has already started or finished or is full'}, status=400)
        # create Player
        player = PlayerModel.objects.create(
            user_id=player_user_id,
            user_name=player_user_name,
            score=0,
            nickname=nickname,
            player_index=0,
            user_info=user_info,
        )
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        game_list = None
        if game.tournament_id > 0:
            tournament = TournamentModel.objects.filter(id=game.tournament_id)
            if tournament:
                game_list = tournament.games.filter(players__user_id=player_user_id, status='waiting').exclude(id=game.id)
        # Assign new player
        game.players.add(player)
        game.save()
        return JsonResponse({'success': True, 'message': 'Player joined', 'game_id': game.id, 'list_id': list(game_list.values_list('id', flat=True)) if game_list else [game_id]}, status=200)

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
            return JsonResponse({'success': False, 'message': 'Invalid user_id. Must be an integer.'}, status=400)
        # Filter games where used_id is in
        games = GameModel.objects.filter(players__user_id=user_id, status='finished').order_by('-end_time')
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
                'custom_name': game.custom_name,
                'status': game.status,
                'game_type': game.game_type,
                'match_type': game.match_type,
                'score_to_win': game.score_to_win,
                'tournament_id': game.tournament_id,
                'ball_speed': game.ball_speed,
                'color_board': game.color_board,
                'color_ball': game.color_ball,
                'color_wall': game.color_wall,
                'color_paddle': game.color_paddle,
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
        return JsonResponse({'success': True, 'games': game_details_list}, safe=False)

class GameDeleteView(APIView):
    """
    Delete a game
    the request must be DELETE
    body = {}
    cookie = {
    'token': type string,
    '42_access_token': type string,
    } one token must be valid
    the game_id is in the url
    """
    def delete(self, request, game_id):
        # get user_id from authentification app
        token = request.COOKIES.get('token')
        refresh_token = request.COOKIES.get('refresh_token')
        token42 = request.COOKIES.get('42_access_token')
        user_info = utils_get_user_info(token, token42, refresh_token)
        if not user_info or not user_info.get('user_id'):
            return JsonResponse({'success': False, 'message': 'Failed to get user info'}, status=400)
        player_user_id = user_info['user_id']
        # Player info validation
        if not player_user_id:
            return JsonResponse({'success': False, 'message': 'Player information is required'}, status=400)
        # get game from id
        game = get_object_or_404(GameModel, id=game_id)
        # check if the request comes from the creator
        player_is_creator = (game.players.all()[0].user_id == player_user_id)
        if player_is_creator == False:
            return JsonResponse({'success': False, 'message': 'Only creator can delete the game'}, status=400)
        game.delete()
        return JsonResponse({'success': True, 'message': 'Game deleted successfully'}, status=200)

class GameDeleteAllView(APIView):
    """
    Delete all games
    the request must be DELETE
    body = {}
    """
    def delete(self, request):
        GameModel.objects.all().delete()
        return JsonResponse({'success': True, 'message': 'All games deleted successfully'}, status=200)

class TournamentCreateView(APIView):
    """
    Create a tourament
    the request must be POST
    body = {
        'custom_name': type string,
        'nickname': type string,
        'match_type': '1v1' or '2v2',
        'game_type': 'pong',
        'score_to_win': type int,
        'player_count': type int,
        'ball_speed': type float,
        'color_board': type string,
        'color_ball': type string,
        'color_wall': type string,
        'color_paddle': type string,
    }
    cookie = {
        'token': type string,
        '42_access_token': type string,
    } One of the token must be valid

    return {
        "success": true,
        "message": "Tournament created",
        "game_id": 3 #first game to be played
    }
    """
    def post(self, request):
        # get user_id and user_name from authentification app
        token = request.COOKIES.get('token')
        refresh_token = request.COOKIES.get('refresh_token')
        token42 = request.COOKIES.get('42_access_token')
        user_info = utils_get_user_info(token, token42, refresh_token)
        player1_user_id = ""
        player1_user_name = ""
        if not user_info:
            return JsonResponse({'success': False, 'message': 'Failed to get user info'}, status=400)
        try:
            player1_user_id = user_info.get('user_id')
            player1_user_name = user_info.get('username')
        except KeyError as e:
            return JsonResponse({'success': False, 'message': f'Missing key in user_info: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'An unexpected error occurred: {str(e)}'}, status=500)
        custom_name = request.data.get('custom_name')
        nickname = request.data.get('nickname', player1_user_name)
        # Data validation
        if not player1_user_id or not player1_user_name:
            return JsonResponse({'success': False, 'message': 'Player information is required'}, status=400)
        # get game type (1 vs 1 or 2 vs 2)
        tourn_match_type = request.data.get('match_type')
        if tourn_match_type not in ['1v1', '2v2']:
            return JsonResponse({'success': False, 'message': 'Invalid match type'}, status=400)
        # get game type (pong or snake)
        tourn_game_type = request.data.get('game_type')
        if not tourn_game_type:
            tourn_game_type = 'pong'
        elif tourn_game_type not in ['pong', 'snake']:
            return JsonResponse({'success': False, 'message': 'Invalid game type'}, status=400)
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
            return JsonResponse({'success': False, 'message': 'Invalid number of players'}, status=400)
        try:
            ball_speed = float(request.data.get('ball_speed', 1.0))
            color_board = request.data.get('color_board', '#000000')
            color_ball = request.data.get('color_ball', '#e48d2d')
            color_wall = request.data.get('color_wall', '#e48d2d')
            color_paddle = request.data.get('color_paddle', '#ffffff')
        except ValueError as e:
            return JsonResponse({'success': False, 'message': f'Invalid value for customization parameter: {str(e)}'}, status=400)
        # Validate customization parameters
        if not (0.5 <= ball_speed <= 2.5):
            return JsonResponse({'success': False, 'message': 'Ball speed must be between 0.5 and 2.5'}, status=400)
        # create tournament
        tournament = TournamentModel.objects.create(
            custom_name=custom_name,
            match_type=tourn_match_type,
            game_type=tourn_game_type,
            score_to_win=score_to_win,
            player_count=player_count,
            ball_speed=ball_speed,
            color_board=color_board,
            color_ball=color_ball,
            color_wall=color_wall,
            color_paddle=color_paddle,
            creation_time=timezone.now(),
            status='waiting',
        )
        # create Player 1
        for idx in range(player_count):
            placeholder = tournament.get_placeholder_user_name(idx)
            placeholder_user_id = tournament.get_placeholder_user_id(idx)
            if (idx == 0):
                player = PlayerModel.objects.create(
                    user_id=player1_user_id,
                    user_name=player1_user_name,
                    score=0,
                    nickname=nickname,
                    player_index=0,
                    user_info=user_info,
                )
            else:
                player = PlayerModel.objects.create(
                    user_id=placeholder_user_id,
                    user_name=placeholder,
                    score=0,
                    nickname='...',
                    player_index=0,
                )
            tournament.players.add(player)
        create_round_robin_matches(tournament)
        tournament_data = tournament.to_array()
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        game_list = None
        if tournament:
            game_list = tournament.games.filter(players__user_id=player1_user_id, status='waiting')
        game_id = tournament_data.get('games')[0].get('id')
        return JsonResponse({
            'success': True,
            'message': 'Tournament created',
            'game_id': game_id,
            'list_id': list(game_list.order_by('id').values_list('id', flat=True)) if game_list else [game.id],
            'tournament': tournament_data,
        }, status=200)

# TODO remove fefore push
class TournamentListView(APIView):
    """
    Return the list of the tournaments
    the request must be GET and look like
    body = {}
    """
    def get(self, request):
        tournaments = TournamentModel.objects.all()
        tournament_list = []
        for tournament in tournaments:
            tournament_data = tournament.to_array()
            tournament_list.append(tournament_data)
        return JsonResponse({'success': True, 'data': tournament_list}, status=200)

class TournamentDetailView(APIView):
    """
    return the details of a tournament
    the request must be GET and look like
    body = {}
    the tournament_id is in the url
    """
    def get(self, request, tournament_id):
        tournament = get_object_or_404(TournamentModel, id=tournament_id)
        return JsonResponse({
            'success': True,
            'data': tournament.to_array()
        }, status=200)

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
        tournament = get_object_or_404(TournamentModel, id=tournament_id)
        # check if tournament is full
        joined_players_count = tournament.get_joined_players_count() # need to find the number of players that are not iwth placeholders
        if joined_players_count >= tournament.player_count:
            return JsonResponse({'success': False, 'message': 'Tournament is already full'}, status=400)
        # tournament must be waiting
        if tournament.status != 'waiting':
            return JsonResponse({'success': False, 'message': 'Tournament has already started or finished'}, status=400)
        # get user_id and user_name from authentification app
        token = request.COOKIES.get('token')
        refresh_token = request.COOKIES.get('refresh_token')
        token42 = request.COOKIES.get('42_access_token')
        user_info = utils_get_user_info(token, token42, refresh_token)
        if not user_info:
            return JsonResponse({'success': False, 'message': 'Failed to get user info'}, status=400)
        player_user_id = user_info['user_id']
        player_user_name = user_info['username']
        # read the JSON file from the request
        data = request.data
        nickname = data.get('nickname', player_user_name)
        # check the player info
        if not player_user_id or not player_user_name:
            return JsonResponse({'success': False, 'message': 'Player information is required'}, status=400)
        # Check if player allready in tournament
        if tournament.players.filter(user_id=player_user_id).exists():
            return JsonResponse({'success': False, 'message': 'Player has already joined the tournament'}, status=400)
        placeholder_player_user_id = tournament.get_placeholder_user_id(joined_players_count)
        players_with_placeholder_user_id = PlayerModel.objects.filter(user_id=placeholder_player_user_id)
        for player in players_with_placeholder_user_id:
            player.user_id = player_user_id
            player.user_name = player_user_name
            player.nickname = nickname
            player.user_info = user_info
            player.save()
        joined_players_count += 1
        # Check if the number of players matches the required player_count
        if joined_players_count == tournament.player_count:
            # Change tournament status to playing
            tournament.status = 'Tournament_full'
            tournament.start_time = timezone.now()
            tournament.save()
        game = tournament.games.filter(status='waiting', players__user_id=player_user_id).first()
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        game_list = None
        if tournament:
            game_list = tournament.games.filter(players__user_id=player_user_id, status='waiting')
        tournament_data = tournament.to_array()
        return JsonResponse({
            'success': True,
            'message': 'Player joined the tournament',
            'game_id': game.id,
            'list_id': list(game_list.order_by('id').values_list('id', flat=True)) if game_list else [game.id],
            'tournament_id': tournament.id,
            'game_id': tournament_data.get('games')[0].get('id'),
            'player_id': player.user_id,
            'tournament': tournament_data
        }, status=200)
        #return JsonResponse({'success': True, 'message': 'Player joined', 'game_id': game.id}, status=200)

class TournamentDeleteView(APIView):
    """
    Delete a tournament
    the request must be DELETE
    body = {}
    cookie = {
    'token': type string,
    '42_access_token': type string,
    } one token must be valid
    the tournament_id is in the url
    """
    def delete(self, request, tournament_id):
        # get user_id from authentification app
        token = request.COOKIES.get('token')
        refresh_token = request.COOKIES.get('refresh_token')
        token42 = request.COOKIES.get('42_access_token')
        user_info = utils_get_user_info(token, token42, refresh_token)
        if not user_info or not user_info.get('user_id'):
            return JsonResponse({'success': False, 'message': 'Failed to get user info'}, status=400)
        player_user_id = user_info['user_id']
        # Player info validation
        if not player_user_id:
            return JsonResponse({'success': False, 'message': 'Player information is required'}, status=400)
        # get tournament from id
        tournament = get_object_or_404(TournamentModel, id=tournament_id)
        # check if the request comes from the creator
        player_is_creator = (tournament.players.all()[0].user_id == player_user_id)
        if player_is_creator == False:
            return JsonResponse({'success': False, 'message': 'Only creator can delete the game'}, status=400)
        tournament.delete()
        return JsonResponse({'success': True, 'message': 'Tournament deleted successfully'}, status=200)

class TournamentDeleteAllView(APIView):
    """
    Delete all tournaments
    the request must be DELETE
    body = {}
    """
    def delete(self, request):
        TournamentModel.objects.all().delete()
        return JsonResponse({'success': True, 'message': 'All tournaments deleted successfully'}, status=200)

