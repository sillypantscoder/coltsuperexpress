import typing

class Card:
	def __init__(self, figure: "Figure"):
		self.figure = figure
	def execute(self):
		pass
	def getIcon(self):
		return ""
		# come on @augustoroman

class Figure:
	def __init__(self, player: "Player" | None = None):
		self.player = player
		self.stunned = False
		self.height = False
		self.direction: typing.Literal["left", "right"] = "right"

class MoveForwardsCard(Card):
	def __init__(self, figure: Figure, game: "Game"):
		super().__init__(figure)
		self.game = game
	def execute(self):
		if self.figure.stunned:
			self.figure.stunned = False
		else:
			new_car: list[Figure] | None = None
			for carno, car in enumerate(self.game.train):
				if self.figure in car: # Python does advertise how its statements look like real life sentences
					car.remove(self.figure)
					offset = -1 if self.figure.direction == "left" else 1
					new_car = self.game.train[carno + offset]
			if not new_car == None:
				if self.figure.direction == "left":
					new_car.append(self.figure)
				else:
					new_car.insert(0, self.figure)

class TurnCard(Card):
	def __init__(self, figure: Figure):
		super().__init__(figure)
	def execute(self):
		if self.figure.stunned:
			self.figure.stunned = False
		else:
			if self.figure.direction == "left":
				self.figure.direction = "right"
			else:
				self.figure.direction = "left"

class UpOrDownCard(Card):
	# anyone got a better name for this?
	# :/
	def __init__(self, figure: Figure):
		super().__init__(figure)
	def execute(self):
		if self.figure.stunned:
			self.figure.stunned = False
		else:
			self.figure.height = not self.figure.height

class ShootCard(Card):
	def __init__(self, figure: Figure, game: "Game"):
		super().__init__(figure)
		self.game = game
	def execute(self):
		if self.figure.stunned:
			self.figure.stunned = False
		else:
			self.game.shoot(self.figure)

class Player:
	def __init__(self, name: str):
		self.name: str = name
		self.figure: Figure | None = Figure(self)
		self.plan: list[Card] = []

class Game:
	def __init__(self):
		self.status: typing.Literal["joining", "schemin", "executing"] = "joining"
		self.players: list[Player] = []
		self.train: list[list[Figure]] = []
	def initTrain(self):
		self.train = [[]] # caboose
		for i in range(len(self.players)):
			player = self.players[i]
			fig = Figure(player)
			player.figure = fig
			self.train.append([fig])
		self.train.append([]) # engine
	def shoot(self, figure: Figure):
		# uhhhhh
		pass