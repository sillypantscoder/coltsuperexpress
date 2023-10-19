import typing

class Game:
	def __init__(self):
		self.status: typing.Literal["joining", "playing"] = "joining"
