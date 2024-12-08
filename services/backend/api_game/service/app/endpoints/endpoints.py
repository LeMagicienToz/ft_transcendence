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
import re

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
        'refresh_token': type string,
        '42_access_token': type string,
    } one token must be valid
    """
    def post(self, request):
        token = request.COOKIES.get('token')
        refresh_token = request.COOKIES.get('refresh_token')
        token42 = request.COOKIES.get('42_access_token')
        refresh_token42 = request.COOKIES.get('42_refresh_token')
        user_info = utils_get_user_info(token, token42, refresh_token, refresh_token42)

        if not user_info:
            return JsonResponse({'success': False,'message': 'Failed to fetch user info.'}, status=400)
        try:
            player1_user_id = user_info.get('user_id')
            player1_user_name = user_info.get('username')
        except:
            return JsonResponse({'success': False, 'message': 'An error has occurred.'}, status=400)

        if not player1_user_id or not player1_user_name:
            return JsonResponse({'success': False,'message': 'Player information is required'}, status=400)

        custom_name = request.data.get('custom_name')
        nickname = request.data.get('nickname', player1_user_name)

        if not re.search(r"^[A-Za-z0-9 _.+'\"$#@)(\][)-]{4,24}$", custom_name):
            return JsonResponse({'success': False, 'message': 'Room name can only contain alphanumeric characters and "_-.+\'()[]"" symbols, and be between 5 and 24 characters long.'}, status=400)
        if not re.search(r"^[A-Za-z0-9_#-]{5,16}$", nickname):
            return JsonResponse({'success': False, 'message': 'Nickname can only contain alphanumeric characters and "_-" symbols, and be between 5 and 16 characters long.'}, status=400)
   
        player1 = PlayerModel.objects.create(
            user_id=player1_user_id,
            user_name=player1_user_name,
            score=0,
            nickname=nickname,
            player_index=0,
            user_info=user_info,
        )

        match_type = request.data.get('match_type')
        if not match_type or match_type not in ['1v1']:
            return JsonResponse({'success': False, 'message': 'An error has occurred.'}, status=400)

        game_type = request.data.get('game_type')
        if not game_type or game_type not in ['pong']:
            return JsonResponse({'success': False, 'message': 'An error has occurred.'}, status=400)

        def clamp(value, min_value, max_value):
            return max(min_value, min(value, max_value))

        try:
            score_to_win = clamp(int(request.data.get('score_to_win', 3)), 3, 15)
        except:
            score_to_win = 3
        try:
            tourn_id = int(request.data.get('tournament_id', 0))
            tourn = TournamentModel.objects.get(id=tourn_id) if tourn_id > 0 else None
            tourn_id = tourn.id if tourn else 0
        except (ValueError, TypeError, TournamentModel.DoesNotExist):
            tourn_id = 0

        color_board = request.data.get('color_board', '#000000')
        color_ball = request.data.get('color_ball', '#e48d2d')
        color_wall = request.data.get('color_wall', '#e48d2d')
        color_paddle = request.data.get('color_paddle', '#ffffff')

        for color in color_board, color_ball, color_wall, color_paddle:
            if not re.search(r"^#[A-Fa-f0-9]{6}$", color):
                return JsonResponse({'success': False, 'message': 'An error has occurred.'}, status=400)

        try:
            ball_speed = clamp(float(request.data.get('ball_speed', 1.0)), 0.5, 2.5)
        except:
            return JsonResponse({'success': False, 'message': 'An error has occurred.'}, status=400)

        try:
            game = GameModel.objects.create(
                custom_name=custom_name,
                creator=nickname,
                match_type=match_type,
                game_type=game_type,
                score_to_win=score_to_win,
                player_count=2,
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
        except Exception:
            return JsonResponse({'success': False, 'message': 'Failed to create game.'}, status=400)
        return JsonResponse({'success': True, 'message': 'Game created', 'game_id': game.id, 'list_id': [game.id]}, status=200)

class ListView(APIView):
    """
    Return a single 'games' array containing both games and tournaments in a single response that are 'waiting'.
    The request must be GET.
    """
    def get(self, request):
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
# class ListAllView(APIView):
#     """
#     Return a single 'games' array containing both games and tournaments in a single response.
#     The request must be GET.
#     """
#     def get(self, request):
#         games = GameModel.objects.filter(tournament_id=0)
#         games_data = [
#             game.to_array()
#             for game in games
#         ]
#         tournaments = TournamentModel.objects.all()
#         tournaments_data = [
#             tournament.to_array()
#             for tournament in tournaments
#         ]
#         combined_data = games_data + tournaments_data
#         response_data = {
#             'success': True,
#             'games': combined_data
#         }
#         return JsonResponse(response_data, safe=False)

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
        'refresh_token': type string,
        '42_access_token': type string,
    }
    the game_id is in the url
    """
    def put(self, request, game_id):
        token = request.COOKIES.get('token')
        refresh_token = request.COOKIES.get('refresh_token')
        token42 = request.COOKIES.get('42_access_token')
        refresh_token42 = request.COOKIES.get('42_refresh_token')
        user_info = utils_get_user_info(token, token42, refresh_token, refresh_token42)

        if not user_info:
            return JsonResponse({'success': False, 'message': 'Failed to fetch user info.'}, status=400)

        player_user_id = user_info['user_id']
        player_user_name = user_info['username']

        if not player_user_id or not player_user_name:
            return JsonResponse({'success': False, 'message': 'An error has occurred.'}, status=400)

        data = request.data
        nickname = data.get('nickname', player_user_name)

        if not re.search(r"^[A-Za-z0-9_#-]{5,16}$", nickname):
            return JsonResponse({'success': False, 'message': 'An error has occurred.'}, status=400)
        
        game = get_object_or_404(GameModel, id=game_id)

        if game.players.filter(user_id=player_user_id).exists():
            return JsonResponse({'success': False, 'message': 'You can\'t join the game twice.'}, status=400)
        if game.players.count() >= 2:
            return JsonResponse({'success': False, 'message': 'Game is full.'}, status=400)

        if game.status != 'waiting':
            return JsonResponse({'success': False, 'message': 'Game has already started.'}, status=400)

        player = PlayerModel.objects.create(
            user_id=player_user_id,
            user_name=player_user_name,
            score=0,
            nickname=nickname,
            player_index=0,
            user_info=user_info,
        )
        game_list = None
        if game.tournament_id > 0:
            tournament = TournamentModel.objects.filter(id=game.tournament_id)
            if tournament:
                game_list = tournament.games.filter(players__user_id=player_user_id, status='waiting').exclude(id=game.id)
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
            return JsonResponse({'success': False, 'message': 'Invalid user id.'}, status=400)

        games = GameModel.objects.filter(players__user_id=user_id, status='finished').order_by('-end_time')
        game_details_list = []
        for game in games:
            players = game.players.all()
            has_won = False
            user_score = None
            opponent_score = None
            for player in players:
                if player.user_id == user_id:
                    user_score = player.score
                else:
                    opponent_score = player.score
            if user_score is not None and opponent_score is not None:
                has_won = user_score >= opponent_score
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

# TODO remove before push
# class GameDeleteView(APIView):
#     """
#     Delete a game
#     the request must be DELETE
#     body = {}
#     cookie = {
#         'token': type string,
#         'refresh_token': type string,
#         '42_access_token': type string,
#     } one token must be valid
#     the game_id is in the url
#     """
#     def delete(self, request, game_id):
#         # get user_id from authentification app
#         token = request.COOKIES.get('token')
#         refresh_token = request.COOKIES.get('refresh_token')
#         token42 = request.COOKIES.get('42_access_token')
#         user_info = utils_get_user_info(token, token42, refresh_token)
#         if not user_info or not user_info.get('user_id'):
#             return JsonResponse({'success': False, 'message': 'Failed to get user info'}, status=400)
#         player_user_id = user_info['user_id']
#         # Player info validation
#         if not player_user_id:
#             return JsonResponse({'success': False, 'message': 'Player information is required'}, status=400)
#         # get game from id
#         game = get_object_or_404(GameModel, id=game_id)
#         # check if the request comes from the creator
#         player_is_creator = (game.players.all()[0].user_id == player_user_id)
#         if player_is_creator == False:
#             return JsonResponse({'success': False, 'message': 'Only creator can delete the game'}, status=400)
#         game.delete()
#         return JsonResponse({'success': True, 'message': 'Game deleted successfully'}, status=200)

# TODO remove before push
# class GameDeleteAllView(APIView):
#     """
#     Delete all games
#     the request must be DELETE
#     body = {}
#     """
#     def delete(self, request):
#         GameModel.objects.all().delete()
#         return JsonResponse({'success': True, 'message': 'All games deleted successfully'}, status=200)

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
        'refresh_token': type string,
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
        refresh_token42 = request.COOKIES.get('42_refresh_token')
        user_info = utils_get_user_info(token, token42, refresh_token, refresh_token42)

        if not user_info:
            return JsonResponse({'success': False, 'message': 'Failed to fetch user info.'}, status=400)
        try:
            player1_user_id = user_info.get('user_id')
            player1_user_name = user_info.get('username')
        except:
            return JsonResponse({'success': False, 'message': 'An error has occurred.'}, status=400)

        if not player1_user_id or not player1_user_name:
            return JsonResponse({'success': False, 'message': 'Player information is required'}, status=400)

        custom_name = request.data.get('custom_name')
        nickname = request.data.get('nickname', player1_user_name)

        if not re.search(r"^[A-Za-z0-9 _.+'\"$#@)(\][)-]{4,24}$", custom_name):
            return JsonResponse({'success': False, 'message': 'Room name can only contain alphanumeric characters and "_-.+\'()[]"" symbols, and be between 5 and 24 characters long.'}, status=400)
        if not re.search(r"^[A-Za-z0-9_#-]{5,16}$", nickname):
            return JsonResponse({'success': False, 'message': 'Nickname can only contain alphanumeric characters and "_-" symbols, and be between 5 and 16 characters long.'}, status=400)
   
        tourn_match_type = request.data.get('match_type')
        if tourn_match_type not in ['1v1']:
            return JsonResponse({'success': False, 'message': 'An error has occurred.'}, status=400)
        tourn_game_type = request.data.get('game_type')
        if not tourn_game_type or tourn_game_type not in ['pong']:
            return JsonResponse({'success': False, 'message': 'An error has occurred.'}, status=400)

        def clamp(value, min_value, max_value):
            return max(min_value, min(value, max_value))

        try:
            score_to_win = clamp(int(request.data.get('score_to_win', 3)), 3, 15)
        except:
            score_to_win = 3

        try:
            player_count = clamp(int(request.data.get('player_count')), 3, 10)
        except (ValueError, TypeError):
            return JsonResponse({'success': False, 'message': 'An error has occurred.'}, status=400)

        color_board = request.data.get('color_board', '#000000')
        color_ball = request.data.get('color_ball', '#e48d2d')
        color_wall = request.data.get('color_wall', '#e48d2d')
        color_paddle = request.data.get('color_paddle', '#ffffff')

        for color in color_board, color_ball, color_wall, color_paddle:
            if not re.search(r"^#[A-Fa-f0-9]{6}$", color):
                return JsonResponse({'success': False, 'message': 'An error has occurred.'}, status=400)

        try:
            ball_speed = clamp(float(request.data.get('ball_speed', 1.0)), 0.5, 2.5)
        except:
            return JsonResponse({'success': False, 'message': 'An error has occurred.'}, status=400)

        tournament = TournamentModel.objects.create(
            custom_name=custom_name,
            creator=nickname,
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
        game_list = None
        if tournament:
            game_list = tournament.games.filter(players__user_id=player1_user_id, status='waiting')
        game_id = tournament_data.get('games')[0].get('id')
        return JsonResponse({
            'success': True,
            'message': 'Tournament created',
            'game_id': game_id,
            'list_id': list(game_list.order_by('id').values_list('id', flat=True)) if game_list else [game_id],
            'tournament': tournament_data,
        }, status=200)

# TODO remove before push
# class TournamentListView(APIView):
#     """
#     Return the list of the tournaments
#     the request must be GET and look like
#     body = {}
#     """
#     def get(self, request):
#         tournaments = TournamentModel.objects.all()
#         tournament_list = []
#         for tournament in tournaments:
#             tournament_data = tournament.to_array()
#             tournament_list.append(tournament_data)
#         return JsonResponse({'success': True, 'data': tournament_list}, status=200)

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
        tournament = get_object_or_404(TournamentModel, id=tournament_id)
        joined_players_count = tournament.get_joined_players_count() # need to find the number of players that are not iwth placeholders

        if joined_players_count >= tournament.player_count:
            return JsonResponse({'success': False, 'message': 'Tournament is full.'}, status=400)

        if tournament.status != 'waiting':
            return JsonResponse({'success': False, 'message': 'Tournament has already started.'}, status=400)

        token = request.COOKIES.get('token')
        refresh_token = request.COOKIES.get('refresh_token')
        token42 = request.COOKIES.get('42_access_token')
        refresh_token42 = request.COOKIES.get('42_refresh_token')
        user_info = utils_get_user_info(token, token42, refresh_token, refresh_token42)

        if not user_info:
            return JsonResponse({'success': False, 'message': 'Failed to fetch user info.'}, status=400)
    
        player_user_id = user_info['user_id']
        player_user_name = user_info['username']

        if not player_user_id or not player_user_name:
            return JsonResponse({'success': False, 'message': 'An error has occurred.'}, status=400)

        data = request.data
        nickname = data.get('nickname', player_user_name)

        if not re.search(r"^[A-Za-z0-9_#-]{5,16}$", nickname):
            return JsonResponse({'success': False, 'message': 'Nickname can only contain alphanumeric characters and "_-" symbols, and be between 5 and 16 characters long.'}, status=400)

        if tournament.players.filter(user_id=player_user_id).exists():
            return JsonResponse({'success': False, 'message': 'You can\'t join the tournament twice.'}, status=400)
        placeholder_player_user_id = tournament.get_placeholder_user_id(joined_players_count)
        players_with_placeholder_user_id = PlayerModel.objects.filter(user_id=placeholder_player_user_id)
        for player in players_with_placeholder_user_id:
            player.user_id = player_user_id
            player.user_name = player_user_name
            player.nickname = nickname
            player.user_info = user_info
            player.save()
        joined_players_count += 1
        if joined_players_count == tournament.player_count:
            tournament.status = 'tournament_full'
            tournament.start_time = timezone.now()
            tournament.save()
        game = tournament.games.filter(status='waiting', players__user_id=player_user_id).first()
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

# TODO remove before push
# class TournamentDeleteView(APIView):
#     """
#     Delete a tournament
#     the request must be DELETE
#     body = {}
#     cookie = {
#         'token': type string,
#         'refresh_token': type string,
#         '42_access_token': type string,
#     } one token must be valid
#     the tournament_id is in the url
#     """
#     def delete(self, request, tournament_id):
#         # get user_id from authentification app
#         token = request.COOKIES.get('token')
#         refresh_token = request.COOKIES.get('refresh_token')
#         token42 = request.COOKIES.get('42_access_token')
#         user_info = utils_get_user_info(token, token42, refresh_token)
#         if not user_info or not user_info.get('user_id'):
#             return JsonResponse({'success': False, 'message': 'Failed to get user info'}, status=400)
#         player_user_id = user_info['user_id']
#         # Player info validation
#         if not player_user_id:
#             return JsonResponse({'success': False, 'message': 'Player information is required'}, status=400)
#         # get tournament from id
#         tournament = get_object_or_404(TournamentModel, id=tournament_id)
#         # check if the request comes from the creator
#         player_is_creator = (tournament.players.all()[0].user_id == player_user_id)
#         if player_is_creator == False:
#             return JsonResponse({'success': False, 'message': 'Only creator can delete the game'}, status=400)
#         tournament.delete()
#         return JsonResponse({'success': True, 'message': 'Tournament deleted successfully'}, status=200)

# # TODO remove before push
# class TournamentDeleteAllView(APIView):
#     """
#     Delete all tournaments
#     the request must be DELETE
#     body = {}
#     """
#     def delete(self, request):
#         TournamentModel.objects.all().delete()
#         return JsonResponse({'success': True, 'message': 'All tournaments deleted successfully'}, status=200)
