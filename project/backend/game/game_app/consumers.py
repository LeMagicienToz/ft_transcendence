from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Game
from asgiref.sync import sync_to_async
import json
import asyncio
from pong.game_logic import GameLogic as myPongGameLogic
from .views import utils_get_user_info
from urllib.parse import parse_qs
import logging
logger = logging.getLogger(__name__)

class Consumer(AsyncWebsocketConsumer):
    user_info = None
    game_id = None
    game = None
    player = None
    async def connect(self):
        try:
            # Access the query string from the scope
            query_string = self.scope['query_string'].decode('utf-8')  # Decode from bytes type
            # Parse the query string
            params = parse_qs(query_string)
            token = params.get('token', [None])[0]  # Get token, or None if not found
            token42 = params.get('42_access_token', [None])[0]
            self.user_info = utils_get_user_info(token, token42)
        except:
            return
        # check if user_info is caught
        if self.user_info is None:
            return
        # import game_id from url, cast into int, and get Game instance
        if await self.get_game() is False:
            return
        # check if the player is in the game
        if await sync_to_async(self.is_player_in_game)() is False:
            return
        # pick game_logic
        if (self.pick_game_logic()) is False:
            return
        await self.game_logic.on_connect()
        #assign the index of player, because a game has 2 or 4 player, we assign 1 to the first and so forth
        if self.player.player_index is 0:
            await sync_to_async(self.assign_player_index)()
        self.channel_layer.group_send(
            f"game_{self.game.id}",
            {
                "type": "player_joined"
            }
        )
        await self.listen()

    async def player_joined(self, event):
        self.game.refresh_from_db()

    def assign_player_index(self):
        indexes = list(self.game.players.values_list('player_index', flat=True))
        # Find the maximum value in the indexes list, defaulting to -1 if empty
        max_index = max(indexes, default=0)
        # Assign the next index to self.player.player_index
        self.player.player_index = max_index + 1
        # Save the updated player instance to the database
        self.player.save()
        self.game.refresh_from_db()
        if self.game.status == 'waiting' and self.game.is_full():
            self.game.status = 'ready_to_play'
            self.game.save()

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
        # get game info
        try:
            self.game = await sync_to_async(Game.objects.get)(id=self.game_id)
        except Game.DoesNotExist:
            return False
        return True

    def pick_game_logic(self):
        # pick game_logic, can add any game here
        if self.game.game_type == "pong":
            self.game_logic = myPongGameLogic(self)
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
        await self.game_logic.end(close_code)

    # I receive only text because json is only text
    # ex: json is {"action" : "moveUp", "player_id": "1"}
    async def receive(self, text_data):
        await self.game_logic.on_receiving_data(text_data)
        #if player start moving, and game is not start, start the game
        if (self.game.status == "ready_to_play"):
            self.game.status = 'playing'
            await sync_to_async(self.game.save)()
            # if player1 moves, it starts the game
            if (self.player.player_index == 1):
                asyncio.create_task(self.start_game_loop()())
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
        # Convert str in int (because JSON gives only str)
        self.game_logic.game_data["player_positions"] = {int(key): value for key, value in self.game_logic.game_data["player_positions"].items()}
        # Send game state by WebSocket
        await self.send(text_data=event["message"])

    def is_player_1(self):
        return self.player and self.player.player_index == 1

    async def start_game_loop(self, event):
        #game has started
        self.game.status = "playing"
        if (self.is_player_1()):
            asyncio.create_task(self.game_logic.start_game_loop())
