import typing

class Card:
	def __init__(self, figure: "Figure", srcGame: "Game"):
		self.figure = figure
		self.game = srcGame
	def execute(self):
		pass
	def getIcon(self):
		return ""
		# come on @augustoroman

class Figure:
	def __init__(self, player: "Player | None" = None):
		self.player = player
		self.stunned = False
		self.height = False
		self.direction: typing.Literal["left", "right"] = "right"
	def getDisplayHeight(self):
		return ((not self.height) * 2) + (self.stunned * 1)
	def getName(self, players: list["Player"]):
		if self.player == None:
			return "#"
		else:
			return str(players.index(self.player))

class MoveForwardsCard(Card):
	def __init__(self, figure: Figure, srcGame: "Game"):
		super().__init__(figure, srcGame)
	def execute(self):
		if self.figure.stunned:
			self.figure.stunned = False
		else:
			self.game.moveFigure(self.figure, self.figure.direction)

class TurnCard(Card):
	def __init__(self, figure: Figure, srcGame: "Game"):
		super().__init__(figure, srcGame)
	def execute(self):
		if self.figure.stunned:
			self.figure.stunned = False
		else:
			if self.figure.direction == "left":
				self.figure.direction = "right"
			else:
				self.figure.direction = "left"

class ChangeLevelCard(Card):
	def __init__(self, figure: Figure, srcGame: "Game"):
		super().__init__(figure, srcGame)
	def execute(self):
		if self.figure.stunned:
			self.figure.stunned = False
		else:
			self.figure.height = not self.figure.height

class ShootCard(Card):
	def __init__(self, figure: Figure, srcGame: "Game"):
		super().__init__(figure, srcGame)
	def execute(self):
		if self.figure.stunned:
			self.figure.stunned = False
		else:
			self.game.shoot(self.figure)

class RevengeCard(Card):
	def __init__(self, figure: Figure, srcGame: "Game"):
		super().__init__(figure, srcGame)
	def execute(self):
		if self.figure.stunned:
			self.figure.stunned = False
			self.game.shoot(self.figure)
		else:
			pass

class Player:
	def __init__(self, name: str):
		self.name: str = name
		self.figure: Figure = Figure(self)
		self.plan: list[Card] = []
		self.ready: bool = False

class Game:
	def __init__(self):
		self.status: typing.Literal["joining", "schemin", "executing"] = "joining"
		self.players: list[Player] = []
		self.train: list[list[Figure]] = []
	def addPlayer(self, player: Player):
		self.players.append(player)
		self.initTrain()
	def __str__(self):
		player_s = ''.join([f'\n |   {self.players.index(p)} - {p.name}' for p in self.players])
		def combineHz(s1: str, s2: str):
			r: list[str] = []
			for line in range(len(s1.split('\n'))):
				r.append(s1.split("\n")[line] + s2.split("\n")[line])
			return '\n'.join(r)
		def renderCar(players: list[Player], car: list[Figure]):
			if len(car) == 0: return "   \n___\n   \n___"
			rows: list[str] = ["", "", "", ""]
			for h in [0, 1, 2, 3]:
				for fig in car:
					if fig.getDisplayHeight() == h:
						if fig.direction == 'left':
							rows[h] += "."
						elif h % 2 == 1:
							rows[h] += "_"
						else:
							rows[h] += " "
						rows[h] += fig.getName(players)
						if fig.direction == 'right':
							rows[h] += "."
						elif h % 2 == 1:
							rows[h] += "_"
						else:
							rows[h] += " "
					elif h % 2 == 1:
						# genius ascii art
						rows[h] += "___"
					else:
						rows[h] += "   "
			return '\n'.join(rows)
		cars = "\n\n\n"
		for car in self.train:
			rendered = renderCar(self.players, car)
			rendered = combineHz(" \n \n \n-", rendered)
			rendered = combineHz(rendered, " \n \n \n-")
			cars = combineHz(cars, rendered)
		return f"Game:\n | status: {self.status}\n | players:{player_s}\n | train:" + \
			("\n" + cars).replace("\n", "\n |  ")
	def initTrain(self):
		self.train = [[]] # caboose
		for i in range(len(self.players)):
			player = self.players[i]
			fig = Figure(player)
			player.figure = fig
			if i >= len(self.players) // 2:
				fig.direction = 'left'
			self.train.append([fig])
		self.train.append([]) # engine
	def shoot(self, figure: Figure):
		carNo = -1
		figNo = -1
		direction = -1 if figure.direction == 'left' else 1
		for carno, car in enumerate(self.train):
			for figno, fig in enumerate(car):
				if fig == figure:
					carNo = carno
					figNo = figno
		while True:
			figNo += direction
			if figNo >= len(self.train[carNo]) or figNo < 0: # If we have traced outside of this car...
				carNo += direction # move to the next car
				if carNo >= len(self.train) or carNo < 0: # Check if we have exited the train
					return
				figNo = 0 # Reset the figure number
				if direction == -1: figNo = len(self.train[carNo]) - 1 # If we are tracing left, the figure number is the end of the car
				if figNo >= len(self.train[carNo]) or figNo < 0: continue # If we are STILL out of bounds, restart so we can check again.
				# This will only happen if there is a car with no one in it.
			# Check this figure
			target = self.train[carNo][figNo]
			if target.height == figure.height:
				if target.stunned == False:
					# aaa!
					target.stunned = True
					self.moveFigure(target, figure.direction)
					return
	def moveFigure(self, figure: Figure, direction: typing.Literal["left", "right"]):
		new_car: list[Figure] | None = None
		for carno, car in enumerate(self.train):
			if figure in car: # Python does advertise how its statements look like real life sentences
				car.remove(figure)
				offset = -1 if direction == "left" else 1
				if carno + offset >= len(self.train) or carno + offset < 0:
					# goodbye player!
					# (the player was removed above, and now will
					#  not be re-added as we are returning early)
					return
					# "aaaaaaa!"
					# 	--this player
				new_car = self.train[carno + offset]
		if not new_car == None:
			if direction == "left":
				new_car.append(figure)
			else:
				new_car.insert(0, figure)
	def toDict(self):
		return {
			"status": self.status,
			"players": [{
				"name": p.name,
				"ready": p.ready
			} for p in self.players],
			"train": [[{
				"player": f.player.name if f.player != None else None,
				"direction": f.direction,
				"height": f.height,
				"stunned": f.stunned
			} for f in car] for car in self.train]
		}
	def readyPlayer(self, name: str):
		for p in self.players:
			if p.name == name:
				p.ready = not p.ready
		if len(self.players) == 0: return
		if self.status == "joining":
			allready = True
			for p in self.players:
				if not p.ready:
					allready = False
			if allready:
				self.startRound()
	def startRound(self):
		self.status = "schemin"
		for p in self.players:
			p.ready = False

if __name__ == "__main__":
	# some testing
	game = Game()
	game.addPlayer(Player("someone"))
	game.addPlayer(Player("someone else"))
	game.addPlayer(Player("a third person"))
	game.initTrain()
	print(game)
	MoveForwardsCard(game.players[0].figure, game).execute()
	print(game)
