from asgiref.sync import sync_to_async
import json
import asyncio

import logging
logger = logging.getLogger(__name__)

class GameLogic():
	# Playing screen dimensions
	SCREEN_W = 400
	SCREEN_H = 300

	# Paddle dimensions
	PADDLE_W = SCREEN_W // 100
	PADDLE_H = SCREEN_H // 10

	# Ball dimensions
	BALL_SIZE = SCREEN_W // 20

	# Paddle and ball speed
	PADDLE_SPEED = 7
	BALL_SPEED_X = 2
	BALL_SPEED_Y = 2

	# Speed control by how many times the game refreshes per second
	REFRESH_PER_SEC = 100

	# Score to reach to win
	SCORE_TO_WIN = 3

	# Initial positions
	bx = (SCREEN_W - BALL_SIZE) // 2 # ball position
	by = (SCREEN_H - BALL_SIZE) // 2
	p1x = 0 # first player on the left
	p1y = (SCREEN_H - PADDLE_H) // 2
	p2x = SCREEN_W - PADDLE_W - 2 # first player on the right
	p2y = (SCREEN_H - PADDLE_H) // 2
	p3x = 1 + PADDLE_W + 1 # second player on the left
	p3y = (SCREEN_H - PADDLE_H) // 2
	p4x = SCREEN_W - (2 * PADDLE_W) - 2 # second player on the right
	p4y = (SCREEN_H - PADDLE_H) // 2
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
			#"scores": {1:0 , 2: 0, 3: 0, 4: 0},
			"SCREEN_W": self.SCREEN_W,
			"SCREEN_H": self.SCREEN_H,
			"PADDLE_W": self.PADDLE_W,
			"PADDLE_H": self.PADDLE_H,
			"BALL_SIZE": self.BALL_SIZE,
			"PADDLE_SPEED": self.PADDLE_SPEED,
			"BALL_SPEED_X": self.BALL_SPEED_X,
			"BALL_SPEED_Y": self.BALL_SPEED_Y,
			"SCORE_TO_WIN": self.SCORE_TO_WIN
		}
		# Configuration for 1v1 match type
		if self.game.match_type == "1v1":
			self.game_data["player_positions"] = {
				1: [self.INITIAL_POSITIONS["player1"]["x"], self.INITIAL_POSITIONS["player1"]["y"]],
				2: [self.INITIAL_POSITIONS["player2"]["x"], self.INITIAL_POSITIONS["player2"]["y"]],
			}
			self.game_data["scores"] = {1: 0, 2: 0}
		# Configuration for 2v2 match type
		elif self.game.match_type == "2v2":
			self.game_data["player_positions"] = {
				1: [self.INITIAL_POSITIONS["player1"]["x"], self.INITIAL_POSITIONS["player1"]["y"]],
				2: [self.INITIAL_POSITIONS["player2"]["x"], self.INITIAL_POSITIONS["player2"]["y"]],
				3: [self.INITIAL_POSITIONS["player3"]["x"], self.INITIAL_POSITIONS["player3"]["y"]],
				4: [self.INITIAL_POSITIONS["player4"]["x"], self.INITIAL_POSITIONS["player4"]["y"]],
			}
			self.game_data["scores"] = {1: 0, 2: 0, 3: 0, 4: 0}

	async def on_connect(self):
		self.consumer.send(json.dumps({
			"action": "initialize",
			"game_data": self.game_data
		}))

	async def end(self, close_code):
		#self.game.status = "finished"
		#await sync_to_async(self.game.save)()
		await self.consumer.send(json.dumps({"action": "game_over", "winner": self.get_winner()}))

	async def on_receiving_data(self, text_data):
		data_json = json.loads(text_data)
		# Convertir les clés de scores en entiers
		#if "scores" in data_json:
		#	data_json["scores"] = {int(k): v for k, v in data_json["scores"].items()}
		action = data_json.get('action')
		if action == "move":
			direction = data_json.get('direction')
			player_index = self.consumer.player.player_index
			if str(player_index) in map(str, self.game_data["player_positions"].keys()) and direction in ["up", "down"]:
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
		if direction == "up":
			y = min(self.SCREEN_H - self.PADDLE_H - 1, y + self.PADDLE_SPEED)
		elif direction == "down":
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

	async def update_ball_position(self):
		# Convertir les clés de scores en entiers
		if "scores" in self.game_data:
			self.game_data["scores"] = {int(k): v for k, v in self.game_data["scores"].items()}
		ball_x, ball_y = self.game_data["ball_position"]
		dx, dy = self.BALL_SPEED_X, self.BALL_SPEED_Y

		ball_x += dx
		ball_y += dy

		if ball_y <= 0 or ball_y + self.BALL_SIZE >= self.SCREEN_H:
			dy = -dy
			self.BALL_SPEED_Y = -self.BALL_SPEED_Y

		if ball_y <= 0:
			ball_y = 0
		if ball_y + self.BALL_SIZE >= self.SCREEN_H:
			ball_y = self.SCREEN_H - self.BALL_SIZE

		if ball_x <= 0:
			if self.game.match_type == "1v1":
				self.game_data["scores"][2] += 1
			elif self.game.match_type == "2v2":
				self.game_data["scores"][2] += 1
				self.game_data["scores"][4] += 1
			if self.game_data["scores"][2] >= self.SCORE_TO_WIN:
				self.game.status = "finished"
			await sync_to_async(self.game.save)()
			self.reset_ball_position()
			await self.send_game_state()
			return
		elif ball_x + self.BALL_SIZE >= self.SCREEN_W:
			if self.game.match_type == "1v1":
				self.game_data["scores"][1] += 1
			elif self.game.match_type == "2v2":
				self.game_data["scores"][1] += 1
				self.game_data["scores"][3] += 1
			if self.game_data["scores"][1] >= self.SCORE_TO_WIN:
				self.game.status = "finished"
			await sync_to_async(self.game.save)()
			self.reset_ball_position()
			await self.send_game_state()
			return
		else:
			if self.game.match_type == "1v1":
				p1_x, p1_y = self.game_data["player_positions"][1]
				p2_x, p2_y = self.game_data["player_positions"][2]

				if p1_x <= ball_x <= p1_x + self.PADDLE_W and p1_y <= ball_y <= p1_y + self.PADDLE_H:
					dx = -dx
					self.BALL_SPEED_X = -self.BALL_SPEED_X
				elif p2_x <= ball_x + self.BALL_SIZE <= p2_x + self.PADDLE_W and p2_y <= ball_y <= p2_y + self.PADDLE_H:
					dx = -dx
					self.BALL_SPEED_X = -self.BALL_SPEED_X

			elif self.game.match_type == "2v2":
				p1_x, p1_y = self.game_data["player_positions"][1]
				p2_x, p2_y = self.game_data["player_positions"][2]
				p3_x, p3_y = self.game_data["player_positions"][3]
				p4_x, p4_y = self.game_data["player_positions"][4]

				if p1_x <= ball_x <= p1_x + self.PADDLE_W and p1_y <= ball_y <= p1_y + self.PADDLE_H:
					dx = -dx
					self.BALL_SPEED_X = -self.BALL_SPEED_X
				elif p2_x <= ball_x + self.BALL_SIZE <= p2_x + self.PADDLE_W and p2_y <= ball_y <= p2_y + self.PADDLE_H:
					dx = -dx
					self.BALL_SPEED_X = -self.BALL_SPEED_X
				elif p3_x <= ball_x <= p3_x + self.PADDLE_W and p3_y <= ball_y <= p3_y + self.PADDLE_H:
					dx = -dx
					self.BALL_SPEED_X = -self.BALL_SPEED_X
				elif p4_x <= ball_x + self.BALL_SIZE <= p4_x + self.PADDLE_W and p4_y <= ball_y <= p4_y + self.PADDLE_H:
					dx = -dx
					self.BALL_SPEED_X = -self.BALL_SPEED_X

		self.game_data["ball_position"] = [ball_x, ball_y]

	def reset_ball_position(self):
		self.game_data["ball_position"] = [
			self.INITIAL_POSITIONS["ball"]["x"],
			self.INITIAL_POSITIONS["ball"]["y"]
		]

	def get_winner(self):
		return max(self.game_data["scores"], key=self.game_data["scores"].get)

	def check_game_over(self):
		return any(score >= self.SCORE_TO_WIN for score in self.game_data["scores"].values())
