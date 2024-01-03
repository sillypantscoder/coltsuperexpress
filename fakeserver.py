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

class HttpResponseStrict(typing.TypedDict):
	"""A dict containing an HTTP response. The content field is required to be bytes and not str."""
	status: int
	headers: dict[str, str]
	content: bytes

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
			"content": read_file("public_files/script.js").replace(b"x.send(body)", b'x.send(body.replaceAll("\\n", "\\\\n"))')
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
	elif path == "/status_mod":
		return {
			"status": 200,
			"headers": {
				"Content-Type": "text/html"
			},
			"content": f"""<p>Status: <b>{game.status}</b></p><p>Players:</p><ul>{"".join(["<li><button onclick='sendServerMsg("+'"r'+str(game.players.index(p))+'"'+")'>Remove</button> "+p.name+"</li>" for p in game.players])}</ul>"""
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
	elif path == "/mod":
		if bodydata[0][0] == "r":
			game.removePlayer(int(bodydata[0][1:]))
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
	def read_packet(self) -> bytes:
		headers = b""
		newChar = b""
		while newChar != b".":
			headers += newChar
			newChar = sys.stdin.buffer.read(1)
		length = int(headers)
		content = b""
		for i in range(length):
			content += sys.stdin.buffer.read(1)
		return content
	def handle_request(self):
		method = self.read_packet()
		path = self.read_packet().decode("UTF-8")
		body = self.read_packet().decode("UTF-8")
		res: HttpResponseStrict = {
			"status": 404,
			"headers": {},
			"content": b""
		}
		if method == b"GET":
			res = self.do_GET(path)
		if method == b"POST":
			res = self.do_POST(path, body)
		s: list[bytes] = [
			str(res["status"]).encode("UTF-8"),
			",".join([f"{a}:{b}" for a, b in res["headers"].items()]).encode("UTF-8"),
			res["content"]
		]
		for data in s:
			self.send_packet(data)
			# time.sleep(0.3)
	def send_packet(self, info: bytes):
		sys.stdout.buffer.write(str(len(info)).encode("UTF-8"))
		sys.stdout.buffer.write(b".")
		sys.stdout.buffer.write(info)
		sys.stdout.buffer.flush()
		# try: print("Printed[", str(len(info)), '.', info.decode("UTF-8"), "]", sep="", file=sys.stderr)
		# except UnicodeDecodeError: print("Printed[", str(len(info)), '.', info, "]", sep="", file=sys.stderr)
	def do_GET(self, path: str) -> HttpResponseStrict:
		splitpath = path.split("?")
		res = get(splitpath[0], URLQuery(''.join(splitpath[1:])))
		c: str | bytes = res["content"]
		if isinstance(c, str): c = c.encode("utf-8")
		return {
			"status": res["status"],
			"headers": res["headers"],
			"content": c
		}
	def do_POST(self, path: str, body: str) -> HttpResponseStrict:
		res = post(path, body)
		c: str | bytes = res["content"]
		if isinstance(c, str): c = c.encode("utf-8")
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
