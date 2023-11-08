import typing

class Card:
	def __init__(self, figure: "Figure", srcGame: "Game"):
		self.figure = figure
		self.game = srcGame
	def execute(self):
		pass
	def getName(self):
		return ""

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
	def getName(self):
		return "forwards"

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
	def getName(self):
		return "turn"

class ChangeLevelCard(Card):
	def __init__(self, figure: Figure, srcGame: "Game"):
		super().__init__(figure, srcGame)
	def execute(self):
		if self.figure.stunned:
			self.figure.stunned = False
		else:
			self.figure.height = not self.figure.height
	def getName(self):
		return "changeLevel"

class ShootCard(Card):
	def __init__(self, figure: Figure, srcGame: "Game"):
		super().__init__(figure, srcGame)
	def execute(self):
		if self.figure.stunned:
			self.figure.stunned = False
		else:
			self.game.shoot(self.figure)
	def getName(self):
		return "shoot"

class RevengeCard(Card):
	def __init__(self, figure: Figure, srcGame: "Game"):
		super().__init__(figure, srcGame)
	def execute(self):
		if self.figure.stunned:
			self.figure.stunned = False
			self.game.shoot(self.figure)
		else:
			pass
	def getName(self):
		return "revenge"

card_types: "list[type[Card]]" = [MoveForwardsCard, TurnCard, ChangeLevelCard, ShootCard, RevengeCard]

class Player:
	def __init__(self, name: str):
		self.name: str = name
		self.figure: Figure = Figure(self)
		self.plan: list[Card] = []
		self.ready: bool = False
	def setPlan(self, srcGame: "Game", data: list[str]):
		self.plan = []
		for item in data:
			card = {
				c(self.figure, srcGame).getName(): c
				for c in card_types
			}[item]
			self.plan.append(card(self.figure, srcGame))
		self.ready = True

def shiftPlayerList(oldList: list[Player], offset: int) -> list[Player]:
	newList = [*oldList] # not in place
	for _ in range(offset):
		newList.append(newList.pop(0))
	return newList

class Game:
	def __init__(self):
		self.status: typing.Literal["joining", "schemin", "executing"] = "joining"
		self.players: list[Player] = []
		self.train: list[list[Figure]] = []
		self.lastcard: tuple[Card, str] | None = None
		self.playerOffset: int = 0
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
				"ready": p.ready,
				"planSize": len(p.plan)
			} for p in self.players],
			"train": [[{
				"player": f.player.name if f.player != None else None,
				"direction": f.direction,
				"height": f.height,
				"stunned": f.stunned
			} for f in car] for car in self.train],
			"lastcard": [self.lastcard[0].getName(), self.lastcard[1]] if self.lastcard != None else None,
			"playeroffset": self.playerOffset
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
		elif self.status == "executing":
			allready = True
			for p in self.players:
				if not p.ready:
					allready = False
			if allready:
				self.startCard()
	def startRound(self):
		self.status = "schemin"
		self.lastcard = None
		for p in self.players:
			p.ready = False
	def setPlan(self, data: list[str]):
		playername = data[0]
		for p in self.players:
			if p.name == playername:
				p.setPlan(self, data[1:])
		allready = True
		for p in self.players:
			if not p.ready:
				allready = False
		if allready:
			self.startCard()
	def startCard(self):
		self.status = "executing"
		for p in self.players:
			p.ready = False
		# Find the card
		maxcards = -1
		maxcplayer = self.players[0]
		for p in shiftPlayerList(self.players, self.playerOffset):
			if len(p.plan) > maxcards:
				maxcards = len(p.plan)
				maxcplayer = p
		if maxcards == 0:
			# We are out of cards!
			self.playerOffset += 1
			self.startRound()
		else:
			self.lastcard = (maxcplayer.plan.pop(0), maxcplayer.name)
			self.lastcard[0].execute()

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
