from .models import Tournament, Game, Player
from django.utils import timezone

def create_round_robin_matches(tournament):
    # Récupère les informations nécessaires du tournoi
    players = list(tournament.players.all())
    game_custom_name = "Game in " + tournament.tournament_custom_name
    tournament_id = tournament.id
    score_to_win = tournament.score_to_win
    match_type = tournament.match_type
    game_type = tournament.game_type
    games = []

    # Création des matchs en fonction du type de match
    if match_type == '1v1':
        # Mode 1v1 : chaque joueur affronte chaque autre joueur une fois
        for i in range(len(players)):
            for j in range(i + 1, len(players)):
                game = Game(
                    game_custom_name=game_custom_name,
                    match_type=match_type,
                    game_type=game_type,
                    score_to_win=score_to_win,
                    tournament_id=tournament_id,
                    status='waiting'
                )
                game.save()
                # Clone les joueurs pour le jeu
                player1 = Player(
                    user_id=players[i].user_id,
                    user_name=players[i].user_name,
                    score=0,
                    nickname=players[i].nickname,
                    player_index=players[i].player_index
                )
                player2 = Player(
                    user_id=players[j].user_id,
                    user_name=players[j].user_name,
                    score=0,
                    nickname=players[j].nickname,
                    player_index=players[j].player_index
                )
                player1.save()
                player2.save()
                game.players.add(player1, player2)
                #game.players.add(players[i], players[j])  # Ajoute les joueurs au match
                games.append(game)

    elif match_type == '2v2':
        # Mode 2v2 : création d'équipes et affrontements entre équipes
        if len(players) % 2 != 0:
            raise ValueError("The number of players must be even for 2v2 matches.")

        # Création des équipes par paires successives
        teams = [(players[i], players[i + 1]) for i in range(0, len(players), 2)]

        # Chaque équipe affronte chaque autre équipe une fois
        for i in range(len(teams)):
            for j in range(i + 1, len(teams)):
                game = Game(
                    game_custom_name=game_custom_name,
                    match_type=match_type,
                    game_type=game_type,
                    score_to_win=score_to_win,
                    tournament_id=tournament_id,
                    status='waiting'
                )
                game.save()
                # Clone les joueurs pour le jeu
                team1_player1 = Player.objects.create(
                    user_id=teams[i][0].user_id,
                    user_name=teams[i][0].user_name,
                    score=0,
                    nickname=teams[i][0].nickname,
                    player_index=teams[i][0].player_index
                )
                team1_player2 = Player.objects.create(
                    user_id=teams[i][1].user_id,
                    user_name=teams[i][1].user_name,
                    score=0,
                    nickname=teams[i][1].nickname,
                    player_index=teams[i][1].player_index
                )
                team2_player1 = Player.objects.create(
                    user_id=teams[j][0].user_id,
                    user_name=teams[j][0].user_name,
                    score=0,
                    nickname=teams[j][0].nickname,
                    player_index=teams[j][0].player_index
                )
                team2_player2 = Player.objects.create(
                    user_id=teams[j][1].user_id,
                    user_name=teams[j][1].user_name,
                    score=0,
                    nickname=teams[j][1].nickname,
                    player_index=teams[j][1].player_index
                )
                game.players.add(team1_player1, team1_player2, team2_player1, team2_player2)
                # Ajoute les joueurs des deux équipes au match
                #game.players.add(teams[i][0], teams[i][1], teams[j][0], teams[j][1])
                games.append(game)

    # Ajoute tous les jeux au tournoi
    tournament.games.set(games)
    tournament.status = 'playing'
    tournament.start_time = timezone.now()
    tournament.save()

def update_tournament_status(tournament):
    """
    Met à jour le statut d'un tournoi en fonction de l'état de ses matchs.
    """
    ongoing_games = tournament.games.filter(status='playing').count()
    finished_games = tournament.games.filter(status='finished').count()
    total_games = tournament.games.count()

    if finished_games == total_games:
        tournament.status = 'finished'
        tournament.end_time = timezone.now()
    elif ongoing_games > 0:
        tournament.status = 'playing'
    else:
        tournament.status = 'waiting'
    tournament.save()

def record_match_result(game_id, player1_score, player2_score):
    """
    Enregistre le résultat d'un match, met à jour les scores des joueurs
    et vérifie si le tournoi est terminé.
    """
    game = Game.objects.get(id=game_id)
    if game.status != 'playing':
        return {'error': 'Game is not active'}

    # Met à jour les scores des joueurs
    players = game.players.all()
    player1, player2 = players[0], players[1]

    game.status = 'finished'
    game.end_time = timezone.now()
    game.save()

    # Mettre à jour les scores
    player1.score += player1_score
    player2.score += player2_score
    player1.save()
    player2.save()

    # Vérifie si le tournoi est terminé
    tournament = game.tournaments.first()  # On prend le tournoi associé
    update_tournament_status(tournament)

    return {'message': 'Match result recorded', 'tournament_status': tournament.status}
