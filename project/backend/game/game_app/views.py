from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import Player, Game, Tournament
from django.utils import timezone
import json
from django.views.decorators.http import require_POST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .tournament_logic import create_round_robin_matches

def ping(request):
        """
        for testing, the serveur should reply 'pong' to 'ping'
        """
        return JsonResponse({'received': 'pong'})

class GameCreateView(APIView):
    """
    Create a new Game object
    the request must be POST
    body = {'token': type string,
    '42_access_token': type string,
    'game_custom_name': type string,
    'nickname': type string,
    'match_type': '1v1' or '2v2',
    'game_type': 'pong',
    'score_to_win': type int,
    'tournament_id': type int, 0 if not in a tournament,
    }
    """
    def post(self, request):
        token = request.data.get('token')
        token42 = request.data.get('42_acccess_token')
        if not token and token42:
            return JsonResponse({'error': 'Missing authentification token'}, status=400)
        # get user_id and user_name from authentification app
        #user_info = self.get_info_from_token(token, token42)
        #if not user_info:
        #    return JsonResponse({'error': 'No info from token'}, status=401)
        
        # get player 1 user_id and user_name
        #try:
        #    player1_user_id = int(user_info.get('user_id'))
        #except (ValueError, TypeError):
        #    return JsonResponse({'error': 'Invalid user ID'}, status=400)
        #player1_user_name = user_info.get('user_name')
        player1_user_id = 1
        player1_user_name = 'Toto'

        game_custom_name = request.data.get('game_custom_name')
        nickname = request.data.get('nickname', player1_user_name)
        # Data validation
        if not player1_user_id or not player1_user_name:
            return JsonResponse({'error': 'Player information is required'}, status=400)
        # get or create the player
        player1, created = Player.objects.get_or_create(
            user_id=player1_user_id,
            defaults={'user_id': player1_user_id,
                       'user_name': player1_user_name,
                       'nickname': nickname,
                       'score': 0}
        )
        # if player allready exist and user_name is different, then update
        if not created and player1.user_name != player1_user_name:
            player1.user_name = player1_user_name
            player1.save()
        # if player allready exist and nickname is different, then update
        if not created and player1.nickname != nickname:
            player1.nickname = nickname
            player1.save()
        # get game type (1 vs 1 or 2 vs 2)
        match_type = request.data.get('match_type')
        if not match_type:
            match_type = '1v1'
        elif match_type not in ['1v1', '2v2']:
            return JsonResponse({'error': 'Invalid match type'}, status=400)
        # get game name (pong or snake)
        game_type = request.data.get('game_type')
        if not game_type:
            game_type = 'pong'
        elif game_type not in ['pong', 'snake']:
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
                status='waiting'
            )
            game.players.add(player1)
        except Exception as e:
            return JsonResponse({'error': 'Error creating game: {}'.format(str(e))}, status=500)
        return JsonResponse({'message': 'Game created', 'game_id': game.id}, status=201)

    def get_info_from_token(self, token, token42):
        pass

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
                'players': [
                    {
                        'user_id': player.user_id,
                        'user_name': player.user_name,
                        'score': player.score,
                        'nickname': player.nickname,
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
            'players': [
                {
                    'user_id': player.user_id,
                    'user_name': player.user_name,
                    'score': player.score,
                    'nickname': player.nickname,
                } for player in game.players.all()
            ]
        }
        return JsonResponse(game_details)

class GameJoinView(APIView):
    """
    this allow a player to join a game
    the request must be PUT
    body = {'user_id': type int,
    'user_name': type string,
    'nickname': type string,
    }
    the game_id is in the url
    """
    def put(self, request, game_id):
        # get game from id
        game = get_object_or_404(Game, id=game_id)
        # read the JSON file from the request
        data = request.data
        # get new player user_id and user_name
        try:
            player_user_id = int(data.get('user_id'))
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid user ID'}, status=400)
        player_user_name = data.get('user_name')
        nickname = data.get('nickname', player_user_name)
        # Player info validation
        if not player_user_id or not player_user_name:
            return JsonResponse({'error': 'Player information is required'}, status=400)
        # Check if player allready in game
        if game.players.filter(user_id=player_user_id).exists():
            return JsonResponse({'error': 'Player has already joined the game'}, status=400)
        # Add the player in the game
        player, created = Player.objects.get_or_create(
            user_id=player_user_id,
            defaults={'user_name': player_user_name, 'nickname': nickname, 'score': 0}
        )
        # if player allready exist and user_name is different, then update
        if not created and player.user_name != player_user_name:
            player.user_name = player_user_name
            player.save()
        # if player allready exist and nickname is different, then update
        if not created and player.nickname != nickname:
            player.nickname = nickname
            player.save()
        # check valid match type
        #if game.match_type not in ['1v1', '2v2']:
        #    return JsonResponse({'error': 'Invalid match type'}, status=400)
        # check if game is full
        #if game.match_type == '1v1' and game.players.count() >= 2:
        #    return JsonResponse({'message': 'Game is already full'}, status=400)
        #elif game.match_type == '2v2' and game.players.count() >= 4:
        #    return JsonResponse({'message': 'Game is already full'}, status=400)
        # Assign new player
        game.players.add(player)
        #game.save()
        return JsonResponse({'message': 'Player joined', 'game_id': game.id})

class GameStartView(APIView):
    """
    start a game
    the request must be POST
    body = {}
    the game_id is in the url
    """
    def post(self, request, game_id):
        # get game_id
        game = get_object_or_404(Game, id=game_id)
        # check if game is waiting, then match type
        if game.status != 'waiting':
            return JsonResponse({'message': 'Game cannot be started'}, status=400)
        if game.match_type not in ['1v1', '2v2']:
            return JsonResponse({'error': 'Invalid match type'}, status=400)
        # check if game is full : 2 players in 1v1 and 4 in 2v2
        player_count = game.players.count()
        if game.match_type == '1v1' and player_count != 2:
            return JsonResponse({'error': 'A 1v1 game requires exactly 2 players'}, status=400)
        elif game.match_type == '2v2' and player_count != 4:
            return JsonResponse({'error': 'A 2v2 game requires exactly 4 players'}, status=400)
        # Change status to playing and setup start_time
        game.status = 'playing'
        game.start_time = timezone.now()
        game.save()
        # Send a message to the GameConsumer to start the game loop
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"game_{game.id}",  # group name from the consumer
            {
                "type": "start_game_loop",  # the custom type we'll handle in the consumer
                "message": "start"
            }
        )
        return JsonResponse({'message': 'Game started', 'game_id': game.id})

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
    'match_type': '1v1' or '2v2',
    'game_type': 'pong',
    'player_count': type int,
    'players': [
        {
            'user_id': type int,
            'user_name': type string,
            'score': '0',
            'nickname': type string,
        }
    ]
    }
    """
    def post(self, request):
        tourn_match_type = request.data.get('match_type')
        if tourn_match_type not in ['1v1', '2v2']:
            return JsonResponse({'error': 'Invalid match type'}, status=400)
        try:
            player_count = int(request.data.get('player_count'))
            if player_count <= 1:
                raise ValueError
            if tourn_match_type == '2v2' and (player_count <= 3 or player_count % 2 != 0):
                raise ValueError
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid number of players'}, status=400)
        tourn_game_type = request.data.get('game_type')
        if tourn_game_type not in ['pong', 'snake']:
            return JsonResponse({'error': 'Invalid game type'}, status=400)
        # get the player who create the tournament
        player_data = request.data.get('player')
        if not player_data:
            return JsonResponse({'error': 'Player data is required to create a tournament'}, status=400)
        try:
            user_id = player_data.get('user_id')
            user_name = player_data.get('user_name')
            nickname = player_data.get('nickname', user_name)
        except KeyError:
            return JsonResponse({'error': 'Missing player information'}, status=400)
        # check if the player exist, create or update if needed
        player, created = Player.objects.get_or_create(
            user_id=user_id,
            defaults={
                'user_name': user_name,
                'nickname': nickname,
                'score': 0
            }
        )
        if not created:
            if player.user_name != user_name:
                player.user_name = user_name
            if player.nickname != nickname:
                player.nickname = nickname
            player.save()
        # create tournament
        tournament = Tournament.objects.create(
            match_type=tourn_match_type,
            game_type=tourn_game_type,
            status='waiting',
            player_count=player_count,
            creation_time=timezone.now()
        )
        tournament.players.add(player)

        create_round_robin_matches(tournament)
        return JsonResponse({'message': 'Tournament created', 'tournament_id': tournament.id}, status=201)

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
                    "nickname": player.nickname
                }
                for player in tournament.players.all()
            ]
            games = [
                {
                    "id": game.id,
                    "match_type": game.match_type,
                    "game_type": game.game_type,
                    "status": game.status,
                    "start_time": game.start_time,
                    "end_time": game.end_time
                }
                for game in tournament.games.all()
            ]
            tournament_data = {
                "id": tournament.id,
                "match_type": tournament.match_type,
                "game_type": tournament.game_type,
                "status": tournament.status,
                "creation_time": tournament.creation_time,
                "start_time": tournament.start_time,
                "end_time": tournament.end_time,
                "players": players,
                "games": games
            }
            tournament_list.append(tournament_data)

        return Response(tournament_list)

class TournamentDetailView(APIView):
    """
    return the details of a tournament
    the request must be GET and look like
    body = {}
    the tournament_id is in the url
    """
    def get(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except Tournament.DoesNotExist:
            return Response({"error": "Tournament not found"}, status=404)

        players = [
            {
                "user_id": player.user_id,
                "user_name": player.user_name,
                "score": player.score,
                "nickname": player.nickname
            }
            for player in tournament.players.all()
        ]

        games = [
            {
                "id": game.id,
                "match_type": game.match_type,
                "game_type": game.game_type,
                "status": game.status,
                "start_time": game.start_time,
                "end_time": game.end_time
            }
            for game in tournament.games.all()
        ]

        tournament_data = {
            "id": tournament.id,
            "match_type": tournament.match_type,
            "game_type": tournament.game_type,
            "status": tournament.status,
            "creation_time": tournament.creation_time,
            "start_time": tournament.start_time,
            "end_time": tournament.end_time,
            "players": players,
            "games": games
        }

        return Response(tournament_data, status=200)

class TournamentJoinView(APIView):
    """
    this allow a player to join a tournament
    the request must be PUT
    body = {'user_id': type int,
    'user_name': type string,
    'nickname': type string,
    }
    'tournament_id' is in the url.
    """
    def put(self, request, tournament_id):
        # get tournament
        tournament = get_object_or_404(Tournament, id=tournament_id)
        # tournament must be waiting
        if tournament.status != 'waiting':
            return JsonResponse({'error': 'Tournament has already started or finished'}, status=400)
        # read the JSON file from the request
        data = request.data
        # get player id
        try:
            player_user_id = int(data.get('user_id'))
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid user ID'}, status=400)
        player_user_name = data.get('user_name')
        nickname = data.get('nickname', player_user_name)
        # check the player info
        if not player_user_id or not player_user_name:
            return JsonResponse({'error': 'Player information is required'}, status=400)
        # get or create the player in database
        player, created = Player.objects.get_or_create(
            user_id=player_user_id,
            defaults={'user_name': player_user_name, 'nickname': nickname, 'score': 0}
        )
        # update if needed
        if not created:
            if player.user_name != player_user_name:
                player.user_name = player_user_name
            if player.nickname != nickname:
                player.nickname = nickname
            player.save()
        # check if player allready in the tournament
        if tournament.players.filter(user_id=player_user_id).exists():
            return JsonResponse({'error': 'Player has already joined this tournament'}, status=400)
        # check if tournament is full
        if tournament.players.count() >= tournament.player_count:
            return JsonResponse({'error': 'Tournament is already full'}, status=400)
        # add the player
        tournament.players.add(player)
        return JsonResponse({'message': 'Player joined the tournament', 'tournament_id': tournament.id, 'player_id': player.id}, status=200)

class TournamentStartView(APIView):
    """
    Start a tournament.
    The request must be POST.
    The tournament_id is in the URL.
    """
    def post(self, request, tournament_id):
        # Get tournament
        tournament = get_object_or_404(Tournament, id=tournament_id)
        # Check if tournament is waiting
        if tournament.status != 'waiting':
            return JsonResponse({'message': 'Tournament cannot be started'}, status=400)
        # Check if the number of players matches the required player_count
        player_count = tournament.players.count()
        if player_count != tournament.player_count:
            return JsonResponse({'error': f'Tournament requires exactly {tournament.player_count} players'}, status=400)
        # Change tournament status to playing
        tournament.status = 'playing'
        tournament.start_time = timezone.now()
        tournament.save()
        # Send a message to the TournamentConsumer to start the tournament loop
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"tournament_{tournament.id}",
            {
                "type": "start_tournament_loop", # to do
                "message": "start"
            }
        )
        return JsonResponse({'message': 'Tournament started', 'tournament_id': tournament.id})

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


