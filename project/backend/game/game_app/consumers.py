from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Game
from asgiref.sync import sync_to_async
import json
import asyncio
from pong.game_logic import GameLogic as myPongGameLogic

import logging
logger = logging.getLogger(__name__)

class Consumer(AsyncWebsocketConsumer):
    player_id = 0
    async def connect(self):
        # import game_id from url, cast into int
        if await self.get_game() == False:
            await self.send(text_data=json.dumps({"error": "Game not found"}))
            return
        if (self.pick_game_logic()) == False:
            await self.send(text_data=json.dumps({"error": "Invalid game type"}))
            return

        # add the player if not yet here
        #if not await sync_to_async(self.game.players.filter(id=self.player_id).exists)():
        #    await sync_to_async(self.game.players.add)(self.player_id)

        await self.game_logic.on_connect()
        await self.listen()

    def pick_game_logic(self):
        # pick game_logic
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

    async def disconnect(self, close_code):
        await self.game_logic.end(close_code)

    # I receive only text because json is only text
    # ex: json is {"action" : "moveUp", "plyer_id": "1"}
    async def receive(self, text_data):
        await self.game_logic.on_receiving_data(text_data)

    async def game_onchange(self, event):
        #update self.game_logic.game_data
        data_json = json.loads(event["message"])
        self.game_logic.game_data = data_json.get("game_data")
        # Convert str in int
        self.game_logic.game_data["player_positions"] = {int(key): value for key, value in self.game_logic.game_data["player_positions"].items()}
        # Send game state by WebSocket
        await self.send(text_data=event["message"])

    def is_player_1(self):
        return (self.game.players.first().user_id == self.player_id)

    async def start_game_loop(self, event):
        if (self.is_player_1()):
            self.game.status = "playing"
            asyncio.create_task(self.game_logic.start_game_loop())
