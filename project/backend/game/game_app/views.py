from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import Game
from django.utils import timezone
import json
from django.views.decorators.http import require_POST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def ping(request):
        return JsonResponse({'received': 'ok'})

class GameCreateView(View):
    def post(self, request):
        # Vérification du type de requête
        if request.method != 'POST':
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        # Récupérer les données du joueur 1
        try:
            player1_user_id = int(request.POST.get('user_id'))
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid user ID'}, status=400)
        player1_user_name = request.POST.get('user_name')
        # Récupérer le type de jeu (1 vs 1 ou 2 vs 2)
        match_type = request.POST.get('match_type')
        if not match_type:
            match_type = '1v1'
        elif match_type not in ['1v1', '2v2']:
            return JsonResponse({'error': 'Invalid match type'}, status=400)
        # Récupérer le type de jeu (pong ou snake)
        game_type = request.POST.get('game_type')
        if not game_type:
            game_type = 'pong'
        elif game_type not in ['pong', 'snake']:
            return JsonResponse({'error': 'Invalid game type'}, status=400)
        # Validation data
        if not player1_user_id or not player1_user_name:
            return JsonResponse({'error': 'Player information is required'}, status=400)
        # Initialiser le jeu avec les informations du joueur 1
        try:
            game = Game.objects.create(
                player1_user_id=player1_user_id,
                player1_user_name=player1_user_name,
                status='waiting',
                match_type=match_type,
                game_type=game_type,
            )
        except Exception as e:
            return JsonResponse({'error': 'Error creating game: {}'.format(str(e))}, status=500)
        return JsonResponse({'message': 'Game created', 'game_id': game.id}, status=201)

class GameListView(View):
    def get(self, request):
        if request.method != 'GET':
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        games = Game.objects.all().values(
            'id',
            'status',
            'game_type',
            'match_type',
            'player1_user_id',   # eventuellement supprimer id et name si GPRD
            'player1_user_name',
            'player1_score',
            'player1_nickname',
            'player2_user_id',
            'player2_user_name',
            'player2_score',
            'player2_nickname',
            'player3_user_id',
            'player3_user_name',
            'player3_score',
            'player3_nickname',
            'player4_user_id',
            'player4_user_name',
            'player4_score',
            'player4_nickname'
        )
        return JsonResponse(list(games), safe=False)

class GameDetailView(View):
    def get(self, request, game_id):
        if request.method != 'GET':
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        game = get_object_or_404(Game, id=game_id)
        game_details = {
            'game_id': game.id,
            'status': game.status,
            'game_type': game.game_type,
            'match_type': game.match_type,
            'player1_user_id': game.player1_user_id,
            'player1_user_name': game.player1_user_name,
            'player1_score': game.player1_score,
            'player1_nickname': game.player1_nickname,
            'player2_user_id': game.player2_user_id,
            'player2_user_name': game.player2_user_name,
            'player2_score': game.player2_score,
            'player2_nickname': game.player2_nickname,
            'player3_user_id': game.player3_user_id,
            'player3_user_name': game.player3_user_name,
            'player3_score': game.player3_score,
            'player3_nickname': game.player3_nickname,
            'player4_user_id': game.player4_user_id,
            'player4_user_name': game.player4_user_name,
            'player4_score': game.player4_score,
            'player4_nickname': game.player4_nickname,
        }
        return JsonResponse(game_details)

class GameJoinView(View):
    def put(self, request, game_id):
        if request.method != 'PUT':
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        # Récupérer la partie en cours
        game = get_object_or_404(Game, id=game_id)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        player2_user_id = data.get('user_id')
        player2_user_name = data.get('user_name')
        # Validation des informations du joueur 2
        if not player2_user_id or not player2_user_name:
            return JsonResponse({'error': 'Player information is required'}, status=400)
        # Validation ID du joueur 2
        try:
            player2_user_id = int(player2_user_id)
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid user ID'}, status=400)
        # Vérifier que ce joueur n'est pas déjà dans la partie
        if player2_user_id in [game.player1_user_id, game.player2_user_id, game.player3_user_id, game.player4_user_id]:
            return JsonResponse({'error': 'Player has already joined the game'}, status=400)
        # Vérifier si le type de match est valide
        if game.match_type not in ['1v1', '2v2']:
            return JsonResponse({'error': 'Invalid match type'}, status=400)
        if game.match_type == '1v1':
            # Vérifier si player2 est déjà assigné
            if game.player2_user_id != 0:
                return JsonResponse({'message': 'Game is already full'}, status=400)
            # Assignation des données au joueur 2
            game.player2_user_id = player2_user_id
            game.player2_user_name = player2_user_name
        elif game.match_type == '2v2':
            # Vérifier si les joueurs 2, 3 et 4 sont assignés
            if game.player2_user_id != 0 and game.player3_user_id != 0 and game.player4_user_id != 0:
                return JsonResponse({'message': 'Game is already full'}, status=400)
            # Assignation des données au joueur 2 ou 3 ou 4
            if game.player2_user_id == 0:
                game.player2_user_id = player2_user_id
                game.player2_user_name = player2_user_name
            elif game.player3_user_id == 0:
                game.player3_user_id = player2_user_id
                game.player3_user_name = player2_user_name
            elif game.player4_user_id == 0:
                game.player4_user_id = player2_user_id
                game.player4_user_name = player2_user_name
        game.save()
        return JsonResponse({'message': 'Player joined', 'game_id': game.id})

"""
class GameStartView(View):
    def post(self, request, game_id):
        if request.method != 'POST':
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        # Récupérer la partie à démarrer
        game = get_object_or_404(Game, id=game_id)
        # Vérifier si le jeu est en attente et a le bon type de match
        #if game.status != 'waiting':
        #    return JsonResponse({'message': 'Game cannot be started'}, status=400)
        if game.match_type not in ['1v1', '2v2']:
            return JsonResponse({'error': 'Invalid match type'}, status=400)
        active_players = (game.player1_user_id != 0) + (game.player2_user_id != 0) + (game.player3_user_id != 0) + (game.player4_user_id != 0)
        if game.match_type == '1v1' and active_players != 2:
            return JsonResponse({'error': 'A 1v1 game requires exactly 2 players'}, status=400)
        elif game.match_type == '2v2' and active_players != 4:
            return JsonResponse({'error': 'A 2v2 game requires exactly 4 players'}, status=400)
        # Changer le statut du jeu et enregistrer l'heure de début
        game.status = 'playing'
        game.start_time = timezone.now()
        game.save()
        # ask the async game consumer to start a loop
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
"""
