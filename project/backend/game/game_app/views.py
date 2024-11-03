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

        # Retourner une réponse JSON avec le game_id
        return JsonResponse({'message': 'Game created', 'game_id': game.id}, status=201)
