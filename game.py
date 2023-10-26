import typing

class Player:
	def __init__(self, name: str):
		self.name: str = name

class Game:
	def __init__(self):
		self.status: typing.Literal["joining", "schemin", "executing"] = "joining"
		self.players: list[Player] = []

"""

class Game:
	status
	players
	train = list[list[Figure]]

class Figure:
	player: Player | None
	stunned
	height
	direction

class Player:
	name
	figure
	plan

class Card:
	abstract execute()
	abstract getIcon()

"""
