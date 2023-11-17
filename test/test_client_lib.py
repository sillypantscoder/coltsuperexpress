import typing
import json
import requests

class Command(typing.TypedDict):
	name: str
	# function return value is [0] whether it succeded [1] the info to return
	func: typing.Callable[[ list[str] ], tuple[bool, str]]
	syntax: list[
		tuple[str, list[str] | type[int] | type[str]] | typing.Literal["..."]
	]

def make_call_command(path: str, data: typing.Callable[[list[str]], str]) -> typing.Callable[[list[str]], tuple[bool, str]]:
	def call_command(args: list[str]):
		req = requests.post(f"http://0.0.0.0:8080/{path}", data=data(args).encode("UTF-8"), timeout=10)
		if req.status_code == 200:
			return (True, f"{path} request succeded")
		else:
			return (False, f"{path} request failed with status code {req.status_code}!")
	return call_command

def call_assertstate(args: list[str]) -> tuple[bool, str]:
	status: dict[str, typing.Any] | list[typing.Any] | str | int = json.loads(requests.get("http://0.0.0.0:8080/status", timeout=10).text)
	for arg in args[1:]:
		if isinstance(status, dict):
			try:
				status = status[arg]
			except (ValueError, KeyError, IndexError):
				return (False, f"ASSERT STATE FAIL: cannot get {repr(arg)} from {repr(status)}")
		elif isinstance(status, list):
			if arg == ".LEN":
				status = len(status)
			else:
				try:
					status = status[int(arg)]
				except (ValueError, KeyError, IndexError):
					return (False, f"ASSERT STATE FAIL: cannot get index {repr(arg)} from {repr(status)}")
		else:
			return (False, f"ASSERT STATE FAIL: cannot get name {repr(arg)} from {repr(status)}")
	valid = False
	if isinstance(status, str):
		valid = status == args[0]
	if isinstance(status, int):
		try:
			valid = status == int(args[0])
		except ValueError:
			valid = False
	if isinstance(status, bool):
		if status:
			valid = args[0] == "true"
		else:
			valid = args[0] == "false"
	if not valid:
		return (False, f"ASSERT STATE FAIL: {repr(status)} is not equal to {repr(args[0])}")
	return (True, "Assert succeded")

commands: list[Command] = [
	{
		"name": "addplayer",
		"func": make_call_command("join_game", lambda args: args[0]),
		"syntax": [
			("playername", str)
		]
	},
	# ("addplayer", lambda args : requests.post("http://0.0.0.0:8080/join_game", data=args[0].encode("UTF-8"), timeout=10), [
	# 	("playername", str)
	# ]),
	{
		"name": "ready",
		"func": make_call_command("ready", lambda args: args[0]),
		"syntax": [
			("playername", str)
		]
	},
	{
		"name": "submitplan",
		"func": make_call_command("submit_plan", lambda args: '\n'.join(args)),
		"syntax": [
			("playername", str),
			("card1", ["forwards", "turn", "changeLevel", "shoot", "revenge"]),
			("card2", ["forwards", "turn", "changeLevel", "shoot", "revenge"]),
			("card3", ["forwards", "turn", "changeLevel", "shoot", "revenge"])
		]
	},
	{
		"name": "assertstate",
		"func": call_assertstate,
		"syntax": [
			("targetvalue", str),
			("path", str),
			"..."
		]
	}
]

def read_cmd_from_file(filename: str) -> list[str] | None:
	f = open(filename, "r")
	t = f.read().split("\n")
	f.close()
	nextLine = 0
	for lineno in range(len(t)):
		if t[lineno].startswith("> "):
			t[lineno] = t[lineno][2:]
			nextLine = lineno + 1
	try:
		while t[nextLine].startswith("#"): nextLine += 1
		t[nextLine] = "> " + t[nextLine]
		f = open(filename, "w")
		f.write("\n".join(t))
		f.close()
		return t[nextLine][2:].split(" ")
	except IndexError: return None

def get_lineno_from_file(filename: str) -> int:
	f = open(filename, "r")
	t = f.read().split("\n")
	f.close()
	nextLine = 0
	for lineno in range(len(t)):
		if t[lineno].startswith("> "):
			t[lineno] = t[lineno][2:]
			nextLine = lineno + 1
	return nextLine - 1

def reset_file(filename: str):
	f = open(filename, "r")
	t = f.read().split("\n")
	f.close()
	for lineno in range(len(t)):
		if t[lineno].startswith("> "):
			t[lineno] = t[lineno][2:]
	f = open(filename, "w")
	f.write("\n".join(t))
	f.close()

def exec_cmd(cmd: list[str]) -> tuple[bool, str]:
	func = None
	for ex in commands:
		if ex["name"] == cmd[0]:
			func = ex["func"]
	if isinstance(func, typing.Callable):
		return func(cmd[1:])
	else:
		return (False, "Invalid command name!")
