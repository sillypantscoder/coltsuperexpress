import typing
import os
import json
import sys
from game import Game, Player, MoveForwardsCard, TurnCard, ChangeLevelCard, ShootCard, RevengeCard

class URLQuery:
	def __init__(self, q):
		self.orig = q
		self.fields = {}
		for f in q.split("&"):
			s = f.split("=")
			if len(s) >= 2:
				self.fields[s[0]] = s[1]
	def get(self, key):
		if key in self.fields:
			return self.fields[key]
		else:
			return ''

def read_file(filename: str) -> bytes:
	"""Read a file and return the contents."""
	f = open(filename, "rb")
	t = f.read()
	f.close()
	return t

def write_file(filename: str, content: bytes):
	"""Write data to a file."""
	f = open(filename, "wb")
	f.write(content)
	f.close()

class HttpResponse(typing.TypedDict):
	"""A dict containing an HTTP response."""
	status: int
	headers: dict[str, str]
	content: str | bytes

game: Game = Game()

# game.addPlayer(Player("someone"))
# game.addPlayer(Player("someone else"))
# game.addPlayer(Player("a third person"))

def get(path: str, query: URLQuery) -> HttpResponse:
	# playername = query.get("name")
	if path == "/script.js":
		return {
			"status": 200,
			"headers": {
				"Content-Type": "text/javascript"
			},
			"content": read_file("public_files/script.js").replace("x.send(body)", 'x.send(body.replaceAll("\\n", "\\\\n"))')
		}
	elif os.path.isfile("public_files" + path):
		return {
			"status": 200,
			"headers": {
				"Content-Type": {
					"html": "text/html",
					"js": "text/javascript",
					"css": "text/css",
					"svg": "image/svg+xml",
					"ico": "image/x-icon"
				}[path.split(".")[-1]]
			},
			"content": read_file("public_files" + path)
		}
	elif os.path.isdir("public_files" + path):
		return {
			"status": 200,
			"headers": {
				"Content-Type": "text/html"
			},
			"content": read_file("public_files" + path + "index.html")
		}
	elif path == "/status":
		return {
			"status": 200,
			"headers": {
				"Content-Type": "application/json"
			},
			"content": json.dumps(game.toDict(), indent='\t')
		}
	elif path.startswith("/card/"):
		data = path.split("/")[2:]
		card = {
			"move_forwards": MoveForwardsCard,
			"turn": TurnCard,
			"change_level": ChangeLevelCard,
			"shoot": ShootCard,
			"revenge": RevengeCard
		}[data[0]]
		figure = game.players[int(data[1])].figure
		card(figure, game).execute()
		return {
			"status": 200,
			"headers": {
				"Content-Type": "text/html"
			},
			"content": ""
		}
	else: # 404 page
		print("404 GET " + path, file=sys.stderr)
		return {
			"status": 404,
			"headers": {
				"Content-Type": "text/html"
			},
			"content": ""
		}

def post(path: str, body: str) -> HttpResponse:
	bodydata = body.split("\n")
	if path == "/join_game":
		game.addPlayer(Player(bodydata[0]))
		return {
			"status": 200,
			"headers": {},
			"content": ""
		}
	elif path == "/ready":
		game.readyPlayer(bodydata[0])
		return {
			"status": 200,
			"headers": {},
			"content": ""
		}
	elif path == "/submit_plan":
		game.setPlan(bodydata)
		return {
			"status": 200,
			"headers": {},
			"content": ""
		}
	else:
		print("404 POST " + path, file=sys.stderr)
		return {
			"status": 404,
			"headers": {
				"Content-Type": "text/html"
			},
			"content": ""
		}

class MyServer:
	def handle_request(self):
		r = json.loads(input())
		res: HttpResponse = {
				"status": 404,
			"headers": {},
			"content": ""
		}
		if r["method"] == "GET":
			res = self.do_GET(r["path"])
		if r["method"] == "POST":
			res = self.do_POST(r["path"], r["body"])
		print(res["status"], end="")
		print("|||", end="")
		print(",".join([f"{a}:{b}" for a, b in res["headers"].items()]), end="")
		print("|||", end="")
		print(repr(res["content"])[1:-1], end="")
		print()
		sys.stdout.flush()
		# print(f"Sent response", file=sys.stderr)
	def do_GET(self, path):
		splitpath = path.split("?")
		res = get(splitpath[0], URLQuery(''.join(splitpath[1:])))
		c = res["content"]
		if isinstance(c, bytes): c = c.decode("utf-8")
		return {
				"status": res["status"],
			"headers": res["headers"],
			"content": c
		}
	def do_POST(self, path: str, body: bytes):
		res = post(path, body)
		c = res["content"]
		if isinstance(c, bytes): c = c.decode("utf-8")
		return {
				"status": res["status"],
			"headers": res["headers"],
			"content": c
		}

if __name__ == "__main__":
	running = True
	webServer = MyServer()
	print(f"Fake server started", file=sys.stderr)
	# sys.stdout.flush()
	while running:
		try:
			webServer.handle_request()
		except KeyboardInterrupt:
			running = False
	print("Server stopped", file=sys.stderr)
