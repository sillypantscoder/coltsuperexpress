from http.server import BaseHTTPRequestHandler, HTTPServer
import typing
import os
import json
from game import Game

hostName = "0.0.0.0"
serverPort = 8080

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
	"""A dict containing a """
	status: int
	headers: dict[str, str]
	content: str | bytes

game: Game = Game()

def get(path: str) -> HttpResponse:
	if os.path.isfile("public_files" + path):
		return {
			"status": 200,
			"headers": {
				"Content-Type": {
					"html": "text/html",
					"js": "text/javascript",
					"css": "text/css"
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
			"content": json.dumps(game.toDict())
		}
	else: # 404 page
		return {
			"status": 404,
			"headers": {
				"Content-Type": "text/html"
			},
			"content": ""
		}

def post(path: str, body: bytes) -> HttpResponse:
	if path == "/":
		bodydata = body.decode("UTF-8").split("\n")
		return {
			"status": 200,
			"headers": {},
			"content": ""
		}
	else:
		return {
			"status": 404,
			"headers": {
				"Content-Type": "text/html"
			},
			"content": ""
		}

class MyServer(BaseHTTPRequestHandler):
	def do_GET(self):
		res = get(self.path)
		self.send_response(res["status"])
		for h in res["headers"]:
			self.send_header(h, res["headers"][h])
		self.end_headers()
		c = res["content"]
		if isinstance(c, str): c = c.encode("utf-8")
		self.wfile.write(c)
	def do_POST(self):
		res = post(self.path, self.rfile.read(int(self.headers["Content-Length"])))
		self.send_response(res["status"])
		for h in res["headers"]:
			self.send_header(h, res["headers"][h])
		self.end_headers()
		c = res["content"]
		if isinstance(c, str): c = c.encode("utf-8")
		self.wfile.write(c)
	def log_message(self, _format: str, *args) -> None:
		return
		# if 400 <= int(args[1]) < 500:
		# 	# Errored request!
		# 	print("\u001b[31m", end="")
		# print(args[0].split(" ")[0], "request to", args[0].split(" ")[1], "(status code:", args[1] + ")")
		# print("\u001b[0m", end="")
		# # don't output requests

if __name__ == "__main__":
	running = True
	webServer = HTTPServer((hostName, serverPort), MyServer)
	webServer.timeout = 1
	print(f"Server started http://{hostName}:{serverPort}")
	while running:
		try:
			webServer.handle_request()
		except KeyboardInterrupt:
			running = False
	webServer.server_close()
	print("Server stopped")
