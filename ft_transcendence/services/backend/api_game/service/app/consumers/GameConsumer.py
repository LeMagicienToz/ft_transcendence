import django
from os import environ
environ.setdefault('DJANGO_SETTINGS_MODULE', 'service.settings')
django.setup()

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
import asyncio
from .consumers_utils import GameLogic
from urllib.parse import parse_qs
from django.utils import timezone


from ..models import GameModel, TournamentModel

import logging
logger = logging.getLogger(__name__)

# Ensure settings are configured


class GameConsumer(AsyncWebsocketConsumer):

    user_info = None
    game_id = None
    game = None
    player = None

    async def connect(self):
        from ..endpoints.endpoints_utils import utils_get_user_info

        cookies = {}
        headers = dict(self.scope["headers"])
        """
        if b"cookie" in headers:
            cookie_header = headers[b"cookie"].decode()
            cookie_list = cookie_header.split(';')
            for cookie in cookie_list:
                key_value_pair = cookie.split('=')
                if len(key_value_pair) != 2:
                    continue
                key = key_value_pair[0]
                value = key_value_pair[1]
                cookies[key] = value
        else :
            #await self.close()
            return self.close()
        """
        cookies = {}
        headers = dict(self.scope["headers"])
        if b"cookie" in headers:
            cookie_header = headers[b"cookie"].decode()
            cookies = {key: value for key, value in [cookie.split('=') for cookie in cookie_header.split('; ')]}
        else :
            await self.close()
            return

        token = cookies.get('token')
        token42 = cookies.get('42_access_token')
        self.user_info = utils_get_user_info(token, token42)

        # check if user_info is caught
        if self.user_info is None or self.user_info.get('error'):
            return
        # import game_id from url, cast into int, and get Game instance
        if await self.get_game() is False:
            return self.close()
        # check if the player is in the game
        if await sync_to_async(self.is_player_in_game)() is False:
            return self.close()
        # pick game_logic
        if (self.pick_game_logic()) is False:
            return self.close()
        await self.game_logic.on_connect()
        #assign the index of player, \game has 2 or 4 players, player 1 is the first one...
        if self.player.player_index == 0:
            # check the status of the game
            await sync_to_async(self.assign_player_index)()
        await self.listen()
        if self.game.status == 'waiting' and await sync_to_async(self.game.is_full)():
            self.game.status = 'ready_to_play'
            await sync_to_async(self.game.save)()
            #tell eveyrone to update their game_data.status
            self.game_logic.game_data['status'] = 'ready_to_play'
            await self.game_logic.send_game_state()

    def assign_player_index(self):
        indexes = list(self.game.players.values_list('player_index', flat=True))
        # Find the maximum value in the indexes list, defaulting to -1 if empty
        for index in range(10):
            player_index = index + 1
            if player_index in indexes:
                continue
            self.player.player_index = player_index
            self.player.save()
            self.game.refresh_from_db()
            break

    def unassign_player_index(self):
        if self.game.status == "finished":
            return
        self.player.player_index = 0
        # Save the updated player instance to the database
        self.player.save()
        self.game.refresh_from_db()

    def is_player_in_game(self):
        user_id = self.user_info.get('user_id')
        # Retrieve the list of user_ids from the players in this game
        player_ids = list(self.game.players.values_list('user_id', flat=True))
        # Check if the given user_id is in the list of player_ids
        if user_id in player_ids:
            # Assign self.player to the Player instance matching the user_id
            self.player = self.game.players.get(user_id=user_id)
            return True
        else:
            # Set self.player to None if the player is not in the game
            self.player = None
            return False

    async def get_game(self):

        # get game_id fron url
        try:
            self.game_id = int(self.scope["url_route"]["kwargs"]["game_id"])
        except ValueError:
            return False
        # get game instance
        try:
            self.game = await sync_to_async(GameModel.objects.get)(id=self.game_id)
        except GameModel.DoesNotExist:
            return False
        return True

    def pick_game_logic(self):
        # pick game_logic, can add any game here
        if self.game.game_type == "pong":
            self.game_logic = GameLogic(self)
        #elif self.game.game_type == "snake":
        #    self.game_logic = MySnakeGameLogic(self)
        else:
            return False
        return True

    # add current channel_name to the group and start accepting message
    async def listen(self):
        self.room_group_name = f"game_{self.game_id}"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):

        if hasattr(self, 'game_logic') and self.game_logic:
            current_player_index = self.player.player_index
            #logger.debug(f"unassigned player {self.player.player_index}")
            # when we have game_logic we know we have player look "connect()"
            # await sync_to_async(self.unassign_player_index)()
            if self.game_logic.game_data['status'] != 'playing' and self.game_logic.game_data['status'] != 'finished':
                logger.debug("change of status")
                self.game.status = 'abandoned'
                self.game_logic.game_data['status'] = 'abandoned'
                await sync_to_async(self.game.save)()
                await self.game_logic.send_game_state()
            elif self.game_logic.game_data['status'] == 'playing':
                if current_player_index == 1:
                    the_other_player_index = '2'
                else:
                    the_other_player_index = '1'
                self.game_logic.game_data["scores"][the_other_player_index] = self.game.score_to_win
                self.game_logic.game_data['status'] = "finished"
                await self.finish_game()
            await self.game_logic.end(close_code)

    # I receive only text because json is only text
    async def receive(self, text_data):
        await self.game_logic.on_receiving_data(text_data)
        #if player start moving, and game is not start, start the game
        if (self.game.status == 'waiting'):
            await sync_to_async(self.game.refresh_from_db)()
        if (self.game.status == "ready_to_play"):
            # if player1 moves, it starts the game
            if (self.player.player_index == 1):
                await self.start_game_loop({})
            # send a msg to everyone but the player who moved to tell game has atrted
            # if it's not the player 1 who moved, he'll start the game when receiving the msg
            await self.channel_layer.group_send(
                f"game_{self.game.id}",  # group name from the consumer
                {
                    "type": "start_game_loop",  # the custom type we'll handle in the consumer
                    "message": "start"
                }
            )

    async def game_onchange(self, event):
        #update self.game_logic.game_data
        data_json = json.loads(event["message"])
        self.game_logic.game_data = data_json.get("game_data")
        if self.game_logic.game_data['status'] == "finished":
            if self.is_player_1():
                await self.finish_game()
        # Send game state by WebSocket
        await self.send(text_data=event["message"])

    async def finish_game(self):
        self.game.status = "finished"
        self.game_logic.game_data["end_time"] = timezone.now().isoformat()
        self.game.end_time = self.game_logic.game_data["end_time"]
        logger.debug(f"score {self.game_logic.game_data['scores']}")
        await sync_to_async(self.game.update_player_one_score)(self.game_logic.game_data["scores"]['1'])
        await sync_to_async(self.game.update_player_two_score)(self.game_logic.game_data["scores"]['2'])
        await sync_to_async(self.game.save)()
        if self.game.tournament_id != 0:
            tournament = await sync_to_async(Tournament.objects.get)(id=self.game.tournament_id)
            finished_games = await sync_to_async(tournament.games.filter)(status='finished')
            tournament_count = await sync_to_async(tournament.games.count)()
            finished_count = await sync_to_async(finished_games.count)()
            if finished_count == tournament_count:
                tournament.status = "finished"
                tournament.end_time = timezone.now().isoformat()
                await sync_to_async(tournament.save)()

    def is_player_1(self):
        return self.player and self.player.player_index == 1

    async def start_game_loop(self, event):
        #game has started
        self.game.status = 'playing'
        self.game.start_time = timezone.now().isoformat()
        #tell eveyrone to update their game_data.status
        self.game_logic.game_data['status'] = 'playing'
        #self.game_logic.game_data['start_time'] = self.game.start_time
        self.game_logic.send_game_state()
        if (self.is_player_1()):
            asyncio.create_task(self.game_logic.start_game_loop())
            await sync_to_async(self.game.save)()
