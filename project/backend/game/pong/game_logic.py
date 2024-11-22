from asgiref.sync import sync_to_async
import json
import asyncio
from django.utils import timezone

import logging
logger = logging.getLogger('myapp')

class GameLogic():
	# Playing screen dimensions
	SCREEN_X = 399 # 0 to 399 => 400 units
	SCREEN_Y = 299
	# Paddle dimensions
	PADDLE_DIM_X = 0
	PADDLE_DIM_Y = 70
	# Ball dimensions
	BALL_SIZE = 20
	# Paddle and ball speed
	PADDLE_SPEED = 4
	BALL_SPEED_X = 1
	BALL_SPEED_Y = 1
	# Speed control by how many times the game refreshes per second
	REFRESH_PER_SEC = 50
	# Initial positions
	bx = (SCREEN_X - BALL_SIZE + 1) // 2 # ball position
	by = (SCREEN_Y - BALL_SIZE + 1) // 2
	p1x = 0 # first player on the left
	p1y = (SCREEN_Y - PADDLE_DIM_Y + 1) // 2
	p2x = SCREEN_X # first player on the right
	p2y = (SCREEN_Y - PADDLE_DIM_Y + 1) // 2
	p3x = 0 # second player on the left
	p3y = p1y // 2
	p4x = SCREEN_X # second player on the right
	p4y = p2y // 2
	INITIAL_POSITIONS = {
		"ball": {"x": bx, "y": by},
		"player1": {"x": p1x, "y": p1y},
		"player2": {"x": p2x, "y": p2y},
		"player3": {"x": p3x, "y": p3y},
		"player4": {"x": p4x, "y": p4y},
	}

	def __init__(self, consumer):
		self.consumer = consumer
		self.game = consumer.game
		# Initialize positions and scores based on match type
		self.game_data = {
			"ball_position": [
				self.INITIAL_POSITIONS["ball"]["x"],
				self.INITIAL_POSITIONS["ball"]["y"]
			],
			"player_positions": {},
			#"SCREEN_X": self.SCREEN_X,
			#"SCREEN_Y": self.SCREEN_Y,
			#"PADDLE_DIM_X": self.PADDLE_DIM_X,
			#"PADDLE_DIM_Y": self.PADDLE_DIM_Y,
			#"BALL_SIZE": self.BALL_SIZE,
			#"PADDLE_SPEED": self.PADDLE_SPEED,
			#"BALL_SPEED_X": self.BALL_SPEED_X,
			#"BALL_SPEED_Y": self.BALL_SPEED_Y,
			#"SCORE_TO_WIN": self.game.score_to_win,
			"status": self.game.status,
		}
		# Configuration for 1v1 match type
		if self.game.match_type == "1v1":
			self.game_data["player_positions"] = {
				1: [self.INITIAL_POSITIONS["player1"]["x"], self.INITIAL_POSITIONS["player1"]["y"]],
				2: [self.INITIAL_POSITIONS["player2"]["x"], self.INITIAL_POSITIONS["player2"]["y"]],
			}
			self.game_data["scores"] = {'1': 0, '2': 0}
		# Configuration for 2v2 match type
		elif self.game.match_type == "2v2":
			self.game_data["player_positions"] = {
				1: [self.INITIAL_POSITIONS["player1"]["x"], self.INITIAL_POSITIONS["player1"]["y"]],
				2: [self.INITIAL_POSITIONS["player2"]["x"], self.INITIAL_POSITIONS["player2"]["y"]],
				3: [self.INITIAL_POSITIONS["player3"]["x"], self.INITIAL_POSITIONS["player3"]["y"]],
				4: [self.INITIAL_POSITIONS["player4"]["x"], self.INITIAL_POSITIONS["player4"]["y"]],
			}
			self.game_data["scores"] = {'1': 0, '2': 0, '3': 0, '4': 0}

	async def on_connect(self):
		self.consumer.send(json.dumps({
			"action": "initialize",
			"game_data": self.game_data
		}))

	async def end(self, close_code):
		if (self.game.status == "playing"):
			self.game_data["status"] = "finished"
			self.game.status = "finished"
			self.game_data['end_time'] = timezone.now().isoformat()
			self.game.end_time = self.game_data['end_time']
			await sync_to_async(self.game.save)()
			await self.send_game_state()

	async def on_receiving_data(self, text_data):
		data_json = json.loads(text_data)
		action = data_json.get('action')
		if action == "move":
			direction = data_json.get('direction')
			player_index = self.consumer.player.player_index
			if str(player_index) in map(str, self.game_data["player_positions"].keys()) and direction in ["left", "right"]:
				await self.update_player_position(player_index, direction)
			else:
				await self.consumer.send(json.dumps({
					"action": "error",
					"message": "Invalid player ID or direction"
				}))
		elif action == "game over":
			await self.end(close_code=1000)
		elif action == "ping":
			await self.consumer.send(json.dumps({"action": "pong"}))
		else:
			await self.consumer.send(json.dumps({
				"action": "error",
				"message": "Unknown action"
			}))

	async def update_player_position(self, player_index, direction):
		x, y = self.game_data["player_positions"][player_index]
		if direction == "left":
			y = min(self.SCREEN_Y - self.PADDLE_DIM_Y - 1, y + self.PADDLE_SPEED)
		elif direction == "right":
			y = max(0, y - self.PADDLE_SPEED)
		self.game_data["player_positions"][player_index] = [x, y]
		await self.send_game_state()

	async def send_game_state(self):
		message = json.dumps({
			"action": "update",
			"game_data": self.game_data
		})
		await self.consumer.channel_layer.group_send(
			self.consumer.room_group_name, {
				"type": "game_onchange",
				"message": message
			}
		)

	async def start_game_loop(self):
		while self.game.status == "playing":
			await asyncio.sleep(1 / self.REFRESH_PER_SEC)
			await self.update_ball_position()
			await self.send_game_state()

	def is_ball_touched_by_player(self):
		ball_x, ball_y = self.game_data["ball_position"]
		if self.game.match_type == "1v1":
			p1_x, p1_y = self.game_data["player_positions"][1]
			p2_x, p2_y = self.game_data["player_positions"][2]
			if p1_y <= ball_y + self.BALL_SIZE - 1 and p1_y + self.PADDLE_DIM_Y - 1 >= ball_y and p1_x == ball_x:
				"""
				logger.debug(
					f"Ball touched by Player 1!\n"
					f"--- Interaction Details ---\n"
					f"Player 1 Position: x={p1_x}, y range=[{p1_y}, {p1_y + self.PADDLE_DIM_Y - 1}]\n"
					f"Ball Position: x range=[{ball_x}, {ball_x + self.BALL_SIZE - 1}], y range=[{ball_y}, {ball_y + self.BALL_SIZE - 1}]\n"
					f"Paddle Dimensions: Width={self.PADDLE_DIM_X}, Height={self.PADDLE_DIM_Y}\n"
				)
				"""
				self.BALL_SPEED_X = -self.BALL_SPEED_X
				return True
			elif p2_y <= ball_y + self.BALL_SIZE - 1 and p2_y + self.PADDLE_DIM_Y - 1 >= ball_y and p2_x == ball_x + self.BALL_SIZE - 1:
				"""
				logger.debug(
					f"Ball touched by Player 2!\n"
					f"--- Interaction Details ---\n"
					f"Player 2 Position: x={p2_x}, y range=[{p2_y}, {p2_y + self.PADDLE_DIM_Y - 1}]\n"
					f"Ball Position: x range=[{ball_x}, {ball_x + self.BALL_SIZE - 1}], y range=[{ball_y}, {ball_y + self.BALL_SIZE - 1}]\n"
					f"Paddle Dimensions: Width={self.PADDLE_DIM_X}, Height={self.PADDLE_DIM_Y}\n"
				)
				"""
				self.BALL_SPEED_X = -self.BALL_SPEED_X
				return True
			"""
			logger.debug(
				f"Ball not touched by any player\n"
				f"--- Ball and Players Positions ---\n"
				f"Ball Position: x range=[{ball_x}, {ball_x + self.BALL_SIZE - 1}], "
				f"y range=[{ball_y}, {ball_y + self.BALL_SIZE - 1}]\n"
				f"Player 1 Position: x={p1_x}, y range=[{p1_y}, {p1_y + self.PADDLE_DIM_Y - 1}]\n"
				f"Player 2 Position: x={p2_x}, y range=[{p2_y}, {p2_y + self.PADDLE_DIM_Y - 1}]\n"
				f"Paddle Dimensions: Width={self.PADDLE_DIM_X}, Height={self.PADDLE_DIM_Y}\n"
				f"Ball Size: {self.BALL_SIZE}\n"
				f"--- Player 1 Conditions ---\n"
				f"p1_y <= ball_y + BALL_SIZE - 1: {p1_y} <= {ball_y + self.BALL_SIZE - 1} is {p1_y <= ball_y + self.BALL_SIZE - 1}\n"
				f"ball_y + BALL_SIZE - 1 < p1_y + PADDLE_DIM_Y: {ball_y + self.BALL_SIZE - 1} < {p1_y + self.PADDLE_DIM_Y} is {ball_y + self.BALL_SIZE - 1 < p1_y + self.PADDLE_DIM_Y}\n"
				f"p1_x == ball_x + BALL_SIZE - 1: {p1_x} == {ball_x + self.BALL_SIZE - 1} is {p1_x == ball_x + self.BALL_SIZE - 1}\n"
				f"--- Player 2 Conditions ---\n"
				f"p2_y <= ball_y + BALL_SIZE - 1: {p2_y} <= {ball_y + self.BALL_SIZE - 1} is {p2_y <= ball_y + self.BALL_SIZE - 1}\n"
				f"ball_y + BALL_SIZE - 1 < p2_y + PADDLE_DIM_Y: {ball_y + self.BALL_SIZE - 1} < {p2_y + self.PADDLE_DIM_Y} is {ball_y + self.BALL_SIZE - 1 < p2_y + self.PADDLE_DIM_Y}\n"
				f"p2_x == ball_x + BALL_SIZE - 1: {p2_x} == {ball_x + self.BALL_SIZE - 1} is {p2_x == ball_x + self.BALL_SIZE - 1}\n"
			)
			"""
		elif self.game.match_type == "2v2":
			p1_x, p1_y = self.game_data["player_positions"][1]
			p2_x, p2_y = self.game_data["player_positions"][2]
			p3_x, p3_y = self.game_data["player_positions"][3]
			p4_x, p4_y = self.game_data["player_positions"][4]
			if p1_x <= ball_x < p1_x + self.PADDLE_DIM_X and p1_y == ball_y:
				self.BALL_SPEED_X = -self.BALL_SPEED_X
				return True
			elif p2_x <= ball_x + self.BALL_SIZE < p2_x + self.PADDLE_DIM_X and p2_y == ball_y:
				self.BALL_SPEED_X = -self.BALL_SPEED_X
				return True
			elif p3_x <= ball_x < p3_x + self.PADDLE_DIM_X and p3_y == ball_y:
				self.BALL_SPEED_X = -self.BALL_SPEED_X
				return True
			elif p4_x <= ball_x + self.BALL_SIZE < p4_x + self.PADDLE_DIM_X and p4_y == ball_y:
				self.BALL_SPEED_X = -self.BALL_SPEED_X
				return True
		return False

	async def update_ball_position(self):
		ball_x, ball_y = self.game_data["ball_position"]
		dx, dy = self.BALL_SPEED_X, self.BALL_SPEED_Y
		ball_x += dx
		ball_y += dy
		if ball_y <= 0 or ball_y + self.BALL_SIZE > self.SCREEN_Y:
			"""
			logger.debug(
				f"Ball bounced off the wall!\n"
				f"--- Interaction Details ---\n"
				f"Ball Position: y range=[{ball_y}, {ball_y + self.BALL_SIZE - 1}]\n"
			)
			"""
			dy = -dy
			self.BALL_SPEED_Y = -self.BALL_SPEED_Y
		if ball_y <= 0:
			ball_y = 0
		if ball_y + self.BALL_SIZE > self.SCREEN_Y + 1:
			ball_y = self.SCREEN_Y - self.BALL_SIZE + 1
		self.game_data["ball_position"] = [ball_x, ball_y]
		if ball_x <= 0 or ball_x + self.BALL_SIZE - 1 >= self.SCREEN_X:
			if self.is_ball_touched_by_player():
				return
		if ball_x <=0:
			if self.game.match_type == "1v1":
				self.game_data["scores"]['2'] += 1
			elif self.game.match_type == "2v2":
				self.game_data["scores"]['2'] += 1
				self.game_data["scores"]['4'] += 1
			await sync_to_async(self.game.update_player_two_score)(self.game_data["scores"]['2'])
			if self.game_data["scores"]['2'] >= self.game.score_to_win:
				self.game.status = "finished"
				self.game_data['status'] = "finished"
			await sync_to_async(self.game.save)()
			self.reset_ball_position()
			return
		elif ball_x + self.BALL_SIZE > self.SCREEN_X:
			if self.game.match_type == "1v1":
				self.game_data["scores"]['1'] += 1
			elif self.game.match_type == "2v2":
				self.game_data["scores"]['1'] += 1
				self.game_data["scores"]['3'] += 1
			await sync_to_async(self.game.update_player_one_score)(self.game_data["scores"]['1'])
			if self.game_data["scores"]['1'] >= self.game.score_to_win:
				self.game.status = "finished"
				self.game_data['status'] = "finished"
			await sync_to_async(self.game.save)()
			self.reset_ball_position()
			return
		self.game_data["ball_position"] = [ball_x, ball_y]

	def reset_ball_position(self):
		self.game_data["ball_position"] = [
			self.INITIAL_POSITIONS["ball"]["x"],
			self.INITIAL_POSITIONS["ball"]["y"]
		]
