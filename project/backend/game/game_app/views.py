from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import Player, Game
from django.utils import timezone
import json
from django.views.decorators.http import require_POST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def ping(request):
        return JsonResponse({'received': 'pong'})

class GameCreateView(APIView):
    def post(self, request):
        # get player 1 user_id and user_name
        try:
            player1_user_id = int(request.POST.get('user_id'))
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid user ID'}, status=400)
        player1_user_name = request.POST.get('user_name')
        # Data validation
        if not player1_user_id or not player1_user_name:
            return JsonResponse({'error': 'Player information is required'}, status=400)

        # Création ou récupération du joueur
        player1, created = Player.objects.get_or_create(
            user_id=player1_user_id,
            defaults={'user_name': player1_user_name,
                       'nickname': player1_user_name,
                       'score': 0}
        )

        # get game type (1 vs 1 or 2 vs 2)
        match_type = request.POST.get('match_type')
        if not match_type:
            match_type = '1v1'
        elif match_type not in ['1v1', '2v2']:
            return JsonResponse({'error': 'Invalid match type'}, status=400)
        # get game name (pong or snake)
        game_type = request.POST.get('game_type')
        if not game_type:
            game_type = 'pong'
        elif game_type not in ['pong', 'snake']:
            return JsonResponse({'error': 'Invalid game type'}, status=400)
        # Game init with palyer 1
        try:
            game = Game.objects.create(
                #player1_user_id=player1_user_id,
                #player1_user_name=player1_user_name,
                status='waiting',
                match_type=match_type,
                game_type=game_type,
            )
            game.players.add(player1)
        except Exception as e:
            return JsonResponse({'error': 'Error creating game: {}'.format(str(e))}, status=500)
        return JsonResponse({'message': 'Game created', 'game_id': game.id}, status=201)

class GameListView(APIView):
    def get(self, request):
        games = Game.objects.all()
        games_data = [
            {
                'id': game.id,
                'status': game.status,
                'game_type': game.game_type,
                'match_type': game.match_type,
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
    def get(self, request, game_id):
        game = get_object_or_404(Game, id=game_id)
        game_details = {
            'game_id': game.id,
            'status': game.status,
            'game_type': game.game_type,
            'match_type': game.match_type,
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
    def put(self, request, game_id):
        # get game from id
        game = get_object_or_404(Game, id=game_id)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        # get new player user_id and user_name
        try:
            player_user_id = int(data.get('user_id'))
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid user ID'}, status=400)
        player_user_name = data.get('user_name')
        # Player info validation
        if not player_user_id or not player_user_name:
            return JsonResponse({'error': 'Player information is required'}, status=400)
        # Check if player allready in game
        if game.players.filter(user_id=player_user_id).exists():
            return JsonResponse({'error': 'Player has already joined the game'}, status=400)
        # Add the player in the game
        player, created = Player.objects.get_or_create(
            user_id=player_user_id,
            defaults={'user_name': player_user_name, 'nickname': player_user_name, 'score': 0}
        )
        # check valid match type
        if game.match_type not in ['1v1', '2v2']:
            return JsonResponse({'error': 'Invalid match type'}, status=400)
        # check if game is full
        if game.match_type == '1v1' and game.players.count() >= 2:
            return JsonResponse({'message': 'Game is already full'}, status=400)
        elif game.match_type == '2v2' and game.players.count() >= 4:
            return JsonResponse({'message': 'Game is already full'}, status=400)
        # Assign new player
        game.players.add(player)
        #game.save()
        return JsonResponse({'message': 'Player joined', 'game_id': game.id})

class GameStartView(APIView):
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
