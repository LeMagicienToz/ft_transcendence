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
from ..endpoints.endpoints_utils import utils_get_user_info
from channels.db import database_sync_to_async


from ..models import GameModel, TournamentModel

import logging
logger = logging.getLogger(__name__)

# Ensure settings are configured


class GameConsumer(AsyncWebsocketConsumer):

	user_info = None
	game_id = None
	game = None
	player = None
	tournament_room_group_name = ""
	tournament = None

	async def connect(self):
		cookies = {}
		headers = dict(self.scope["headers"])
		if b"cookie" in headers:
			cookie_header = headers[b"cookie"].decode()
			cookies = {key: value for key, value in [cookie.split('=') for cookie in cookie_header.split('; ')]}
		else :
			# refuse the connection (close the websocket)
			await self.close()
			return

		token = cookies.get('token')
		refresh_token = cookies.get('refresh_token')
		token42 = cookies.get('42_access_token')
		self.user_info = utils_get_user_info(token, token42, refresh_token)

		# check if user_info is caught
		if self.user_info is None or self.user_info.get('error'):
			await self.close()
			return
		# import game_id from url, cast into int, and get Game instance
		if await self.get_game() is False:
			await self.close()
			return

		is_playing_this_game = await sync_to_async(self.is_player_in_game)()
		# check if the player is in the game, if he is in tournament he can spectate
		if self.game.tournament_id == 0 and (is_playing_this_game is False):
			await self.close()
			return
		if self.game.tournament_id != 0 and (is_playing_this_game is False):
			#await self.close()
			return
		# pick game_logic
		if (self.pick_game_logic()) is False:
			await self.close()
			return

		if self.game.status == 'finished':
		#   self.game_logic.game_data['status'] = 'finished'
			await self.game_logic.send_game_state(["status"])
		#    await self.close()
			return

		#await self.game_logic.on_connect()
		#assign the index of player, \game has 2 or 4 players, player 1 is the first one...
		if is_playing_this_game and self.player.player_index == 0:
			# check the status of the game
			await sync_to_async(self.assign_player_index)()
		await self.listen()
		await self.setup_regular_ping()
		if self.game.tournament_id != 0:
			self.tournament = await sync_to_async(TournamentModel.objects.get)(id=self.game.tournament_id)
			await self.listen_to_tournament_group()
			await self.send_to_tournament_group({
				"action": "someone joined"
			})
		await self.accept()
		if self.game.tournament_id == 0:
			await self.update_game_status_to_ready_to_play()
		await self.send(text_data=json.dumps({
			'game_data': self.present(self.game_logic.game_data)
		}))

	async def update_game_status_to_ready_to_play(self):
		if self.game.status == 'waiting' and await sync_to_async(self.game.is_full)():
			self.game.status = 'ready_to_play'
			await sync_to_async(self.game.save)()
			#tell eveyrone to update their game_data.status
			self.game_logic.game_data['status'] = 'ready_to_play'
			await self.game_logic.send_game_state(["status"])

	async def send_to_tournament_group(self, data):
		message = json.dumps(data)
		await self.channel_layer.group_send(
			self.tournament_room_group_name, {
				"type": "tournament_onchange",
				"message": message
			}
		)

	async def tournament_onchange(self, event):
		data_json = json.loads(event["message"])
		if data_json.get('action') == 'someone joined':
			if (await sync_to_async(self.tournament.is_full)()):
				await self.update_game_status_to_ready_to_play()

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

	# add current channel_name to the group and start accepting message
	async def listen_to_tournament_group(self):
		self.tournament_room_group_name = f"tournament_{self.tournament.id}"
		await self.channel_layer.group_add(
			self.tournament_room_group_name,
			self.channel_name
		)

	async def disconnect(self, close_code):
		if hasattr(self, 'game_logic') and self.game_logic and self.player:
			current_player_index = self.player.player_index
			the_other_player_index = '2' if current_player_index == 1 else '1'

			if self.game.tournament_id == 0:
				if self.game_logic.game_data['status'] == 'waiting' or self.game_logic.game_data['status'] == 'ready_to_play':
					self.game_logic.game_data['status'] = 'abandoned'
					self.game.status = 'abandoned'
					await self.game_logic.send_game_state(["status"])
					self.game.start_time = timezone.now().isoformat()
					self.game.end_time = self.game.start_time
					await sync_to_async(self.game.save)()
				elif self.game_logic.game_data['status'] == "finished":
					self.game.status = 'finished'
					self.game_logic.game_data['status'] = 'finished'
					await sync_to_async(self.game.update_player_one_score)(self.game_logic.game_data["scores"]['1'])
					await sync_to_async(self.game.update_player_two_score)(self.game_logic.game_data["scores"]['2'])
					self.game.end_time = timezone.now().isoformat()
					await sync_to_async(self.game.save)()
				elif self.game_logic.game_data['status'] == 'playing':
					self.game_logic.game_data["scores"][the_other_player_index] = self.game.score_to_win
					await sync_to_async(self.game.update_player_one_score)(self.game_logic.game_data["scores"]['1'])
					await sync_to_async(self.game.update_player_two_score)(self.game_logic.game_data["scores"]['2'])
					self.game_logic.game_data['status'] = 'abandoned'
					await self.game_logic.send_game_state(["status"])
					await sync_to_async(self.game.refresh_from_db)()
					self.game_logic.game_data['status'] = 'finished'
					self.game.status = 'finished'
					self.game.end_time = timezone.now().isoformat()
					await sync_to_async(self.game.save)()
				else:
					pass
			else:
				if  self.game_logic.game_data['status'] not in ['finished', 'abandoned']:
					tournament = await sync_to_async(TournamentModel.objects.get)(id=self.game.tournament_id)
					self.game_logic.game_data['status'] = 'abandoned'
					games = await sync_to_async(list)(tournament.games.all())  # Ensure it's an iterable
					for game in games:
						game.status = 'abandoned'
						self.game.end_time = timezone.now().isoformat()
						await sync_to_async(game.save)()
					if tournament.status == 'waiting':
						tournament.status = 'abandoned'
						await sync_to_async(tournament.save)()
					else:
						pass
				elif self.game_logic.game_data['status'] == "finished":
					self.game.status = 'finished'
					self.game_logic.game_data['status'] = 'finished'
					await sync_to_async(self.game.update_player_one_score)(self.game_logic.game_data["scores"]['1'])
					await sync_to_async(self.game.update_player_two_score)(self.game_logic.game_data["scores"]['2'])
					self.game.end_time = timezone.now().isoformat()
					await sync_to_async(self.game.save)()
				else:
					pass

	# I receive only text because json is only text
	async def receive(self, text_data):
		if (self.game.status == 'waiting' or self.game.status == 'ready_to_play'):
			await sync_to_async(self.game.refresh_from_db)()
		await self.game_logic.on_receiving_data(text_data)
		#if player start moving, and game is not start, start the game
		if (self.game_logic.game_data['status'] == "ready_to_play"):
			# if player1 moves, it starts the game
			if (self.player.player_index == 1):
				await self.onchange_start_game({})
			else:
				# send a msg to player 1 for him to start
				await self.channel_layer.group_send(
					f"game_{self.game.id}",
					{
						"type": "onchange_start_game",
						"message": "start"
					}
				)

	async def game_onchange(self, event):
		#update self.game_logic.game_data
		data_json = json.loads(event["message"])
		received_game_data = data_json.get("game_data")
		# Send game state by WebSocket
		fields = data_json.get("fields")
		should_send = True
		for field in fields:
			if (field == "keys"):
				should_send = False
				player_index = data_json.get("player_index")
				self.game_logic.game_data['keys'][player_index] = received_game_data['keys'][player_index]
			else:
				self.game_logic.game_data[field] = received_game_data[field]
		if should_send:
			try:
				await self.send(text_data=json.dumps({
					'game_data': self.present(self.game_logic.game_data)
				}))
				#logger.info(f"game_onchange game_data={self.present(self.game_logic.game_data)}")
			except:
				logger.info("try to send to a close protocol")

	def present(self, data):
		new_data = data.copy()
		del new_data["keys"]
		return new_data

	# async def finish_game(self):
	# 	self.game.status = "finished"
	# 	self.game_logic.game_data["end_time"] = timezone.now().isoformat()
	# 	self.game.end_time = self.game_logic.game_data["end_time"]
	# 	logger.info(f"@@@@@@ debut de finish game @@@@@ self.game_logic.game_data['scores']['1']={self.game_logic.game_data['scores']['1']}, self.game_logic.game_data['scores']['2']={self.game_logic.game_data['scores']['2']}")
	# 	if self.game_logic.game_data['scores']['1'] != 0 and self.game_logic.game_data['scores']['2'] != 0:
	# 		await sync_to_async(self.game.update_player_one_score)(self.game_logic.game_data["scores"]['1'])
	# 		await sync_to_async(self.game.update_player_two_score)(self.game_logic.game_data["scores"]['2'])
	# 		await sync_to_async(self.game.save)()
	# 	if self.game.tournament_id != 0:
	# 		logger.info("&&&&finish_game&&&&  in tounament")
	# 		tournament = await sync_to_async(TournamentModel.objects.get)(id=self.game.tournament_id)
	# 		finished_games = await sync_to_async(tournament.games.filter)(status='finished')
	# 		tournament_count = await sync_to_async(tournament.games.count)()
	# 		finished_count = await sync_to_async(finished_games.count)()
	# 		logger.info(f"finished_count={finished_count} tournament_count={tournament_count}")
	# 		logger.info(f"self.game_logic.game_data['status']={self.game_logic.game_data['status']}")
	# 		if finished_count == tournament_count:
	# 			tournament.status = "finished"
	# 			tournament.end_time = timezone.now().isoformat()
	# 			await sync_to_async(tournament.save)()
	# 		elif self.game_logic.game_data['status'] != 'finished':
	# 			logger.info("-------------------------------------------------------finish-------- self.game_logic.game_data['status'] != 'finished':-------------------------------------")
	# 			games = await database_sync_to_async(tournament.games.filter)(players__user_id=self.player.user_id)
	# 			not_finished_games = await sync_to_async(games.exclude)(status='finished')
	# 			count = await sync_to_async(not_finished_games.count)()
	# 			logger.info(f'Number of not finished games: {count}')

	# 			for game in await database_sync_to_async(list)(not_finished_games):
	# 				logger.info(f'set the status to finished: game.status={game.status}')
	# 				game.status = 'finished'
	# 				#logger.info(f'the status self.game_logic.game_data['status']={self.game_logic.game_data['status']}')
	# 				self.game_logic.game_data["start_time"] = timezone.now().isoformat()
	# 				self.game.start_time = self.game_logic.game_data["start_time"]
	# 				self.game_logic.game_data["end_time"] = self.game_logic.game_data["start_time"]
	# 				self.game.end_time = self.game_logic.game_data["end_time"]
	# 				await database_sync_to_async(game.save)()
	# 				other_player = await database_sync_to_async(
	# 					lambda: game.players.exclude(user_id=self.player.user_id).first()
	# 				)()
	# 				logger.info(f"self.player.user_id={self.player.user_id}, other player = {other_player.user_id if other_player else 'None'}")
	# 				if other_player:
	# 					other_player.score = self.game.score_to_win
	# 					await sync_to_async(self.game.update_player_one_score)(self.game_logic.game_data["scores"]['1'])
	# 					await sync_to_async(self.game.update_player_two_score)(self.game_logic.game_data["scores"]['2'])
	# 					logger.info(f"#### end of finish game #### self.player.user_id={self.player.user_id}, "
	# 						f"his score={self.player.score if self.player else 'None'}, "
	# 						f"other_player_score={other_player.score}")
	# 					await database_sync_to_async(other_player.save)()
	# 					await sync_to_async(self.game.save)()

	# 	self.game_logic.game_data['status'] = 'finished'

	def is_player_1(self):
		return self.player and self.player.player_index == 1

	async def regular_ping(self):
		while True:
			await asyncio.sleep(5)
			try:
				status = (await database_sync_to_async(GameModel.objects.get)(id=self.game_id)).status
				await self.send(text_data=json.dumps({
					"game_data": {
						"status": status,
					}
				}))
			except:
				pass
			if self.game_logic.game_data.get('status') != "waiting" and self.game_logic.game_data.get('status') != "ready_to_play":
				break

	async def setup_regular_ping(self):
		asyncio.create_task(self.regular_ping())

	async def onchange_start_game(self, event):
		#game has started
		self.game.status = 'playing'
		self.game.start_time = timezone.now().isoformat()
		await sync_to_async(self.game.save)()
		#tell eveyrone to update their game_data.status
		self.game_logic.game_data['status'] = 'playing'
		await self.game_logic.send_game_state(["status"])
		logger.info(f"setup start time={self.game.start_time},  self.game_logic.game_data['status']={self.game_logic.game_data['status']} ========================================================")
		if (self.is_player_1()):
			logger.info(f"is player 1={self.is_player_1()} loop started")
			asyncio.create_task(self.game_logic.start_game_loop())
			await sync_to_async(self.game.save)()
		else:
			await sync_to_async(self.game.save)()
