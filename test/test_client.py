import typing
import json
import re # :(
import requests
from getch import getch

RESET = "\u001b[0m"
RED = "\u001b[31m"
YELLOW = "\u001b[33m"
GREEN = "\u001b[32m"

CURSOR_UP    = lambda n: f"\u001b[{n}A"
CURSOR_DOWN  = lambda n: f"\u001b[{n}B"
CURSOR_RIGHT = lambda n: f"\u001b[{n}C"
CURSOR_LEFT  = lambda n: f"\u001b[{n}D"

DELETE_LINE = "\r\u001b[2K"

def call_assertstate(args: list[str]):
	status: dict[str, typing.Any] | list[typing.Any] | str | int = json.loads(requests.get("http://0.0.0.0:8080/status", timeout=10).text)
	for arg in args[1:]:
		if isinstance(status, dict):
			try:
				status = status[arg]
			except (ValueError, KeyError):
				print(f"ASSERT STATE FAIL: cannot get {repr(arg)} from {repr(status)}")
				return
		elif isinstance(status, list):
			try:
				status = status[int(arg)]
			except (ValueError, KeyError):
				print(f"ASSERT STATE FAIL: cannot get index {repr(arg)} from {repr(status)}")
				return
		else:
			print(f"ASSERT STATE FAIL: cannot get name {repr(arg)} from {repr(status)}")
			return
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
		print(f"ASSERT STATE FAIL: {repr(status)} is not equal to {repr(args[0])}")

commands: list[
		# name and func
	tuple[str, typing.Callable[[ list[str] ], typing.Any],
		# syntax
		list[
			tuple[str, list[str] | type[int] | type[str]] | typing.Literal["..."]
		]
	]
] = [
	("addplayer", lambda args : requests.post("http://0.0.0.0:8080/join_game", data=args[0].encode("UTF-8"), timeout=10), [
		("playername", str)
	]),
	("ready", lambda args : requests.post("http://0.0.0.0:8080/ready", data=args[0].encode("UTF-8"), timeout=10), [
		("playername", str)
	]),
	("submitplan", lambda args : requests.post("http://0.0.0.0:8080/submit_plan", data='\n'.join(args).encode("UTF-8"), timeout=10), [
		("playername", str),
		("card1", ["forwards", "turn", "changeLevel", "shoot", "revenge"]),
		("card2", ["forwards", "turn", "changeLevel", "shoot", "revenge"]),
		("card3", ["forwards", "turn", "changeLevel", "shoot", "revenge"])
	]),
	("assertstate", call_assertstate, [
		("targetvalue", str),
		("path", str),
		"..."
	])
	# ("test", call_addplayer, [
	# 	("testy1", ["a", "bbbbbbb", "c"]),
	# 	("testy2", str),
	# 	("testy3", int)
	# ])
]

def get_command() -> list[str]:
	currentS: str = ""
	selectedComplete: int = 0
	def getSyntax(cmdname: str) -> "list[tuple[str, list[str] | type[int] | type[str]] | typing.Literal['...']]":
		for cmd in commands:
			if cmdname == cmd[0]:
				return cmd[2]
		return []
	def getSyntaxString() -> str:
		if len(currentS.split(" ")) <= 1: return ""
		s = currentS.split(" ")
		syntax = getSyntax(s[0])
		syntax = syntax[len(s) - 2:]
		result: list[str] = []
		for item in syntax:
			if isinstance(item[1], list):
				result.append(f"<{item[0]}>")
			elif isinstance(item, str):
				result.append(f"[...{getSyntax(s[0])[-2][0]}]")
			elif isinstance(item[1](), str):
				result.append(f"<{item[0]}: string>")
			elif isinstance(item[1](), int):
				result.append(f"<{item[0]}: number>")
		if len(result) == 0:
			if getSyntax(s[0])[-1] == "...":
				result.append(f"[...{getSyntax(s[0])[-2][0]}]")
			else: return ""
		padding = " " * (len(' '.join(s)) - (len(s[-1]) - 2))
		firstIPad = YELLOW + result[0].ljust(max(len(result[0]), len(s[-1])) + 1) + RESET
		return padding + firstIPad + " ".join(result[1:])
	def validate(cmdname: str, itemno: int, item: str):
		if itemno - 1 < 0: return cmdname in [c[0] for c in commands]
		syntax = getSyntax(cmdname)
		if itemno - 1 >= len(syntax):
			return syntax[-1] == "..."
		argument = syntax[itemno - 1][1]
		if isinstance(argument, list):
			return item in argument
		elif isinstance(argument, str):
			return True
		elif isinstance(argument(), str):
			return True
		elif isinstance(argument(), int):
			for char in item:
				if char not in [*"0123456789"]:
					return False
			return True
	def getComplete():
		results: list[str] = []
		s = currentS.split(" ")
		if len(s) == 1: return [c[0] for c in commands]
		if len(s) - 2 >= len(getSyntax(s[0])): return []
		syntax = getSyntax(s[0])[len(s) - 2][1]
		if isinstance(syntax, list):
			results.extend(syntax)
		# print(repr(results) + "\n\n")
		return results
	def getFilteredComplete():
		results: list[str] = []
		pre: list[str] = getComplete()
		alreadyTyped = currentS.split(" ")[-1]
		for item in pre:
			if item.startswith(alreadyTyped):
				results.append(item)
		return results
	def printState():
		splitCmd = currentS.split(" ")
		# Syntax
		cmdname = splitCmd[0]
		if len(splitCmd) > 1:
			print(getSyntaxString())
		else:
			print()
		# Current string placeholder
		print()
		# Examples
		n = 1
		for i, ex in enumerate(getFilteredComplete()):
			n += 1
			padding = " " * (len(' '.join(splitCmd)) - (len(splitCmd[-1]) - 2))
			print(padding + (YELLOW if i == selectedComplete else "") + ex + RESET)
		# Current string (with validation)
		n += 1
		print(CURSOR_UP(n - 1), end=">")
		for i in range(len(splitCmd)):
			part = splitCmd[i]
			print(end=" ")
			if validate(cmdname, i, part):
				print(GREEN+part+RESET, end="")
			else:
				print(RED+part+RESET, end="")
		return n
	def eraseState(n):
		print(CURSOR_DOWN(n - 1), end="")
		for _ in range(n):
			print(DELETE_LINE, end="")
			print(CURSOR_UP(1), end="")
		print(DELETE_LINE, end="")
	while True:
		n_lines = printState()
		char = getch()
		if char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789":
			currentS += char
			selectedComplete = 0
		elif char == "\x7f":
			# delete
			currentS = currentS[:-1]
			selectedComplete = 0
		elif char == "\r":
			# enter
			eraseState(n_lines)
			print("\n> " + currentS + "\n")
			return currentS.split(" ")
		elif char == "\t":
			complete = getFilteredComplete()
			if selectedComplete < len(complete):
				currentS = currentS[:currentS.rfind(" ") + 1] + complete[selectedComplete] + " "
			selectedComplete = 0
		elif char == "\x1b":
			# esc
			getch()
			char2 = getch()
			if char2 == "B":
				# down
				selectedComplete += 1
				maxC = len(getFilteredComplete()) - 1
				# print("\n", "\n", f"a:{selectedComplete},{maxC}:a", "\n", "\n", "\n", sep="\n")
				if selectedComplete >= maxC: selectedComplete = maxC
			elif char2 == "A":
				selectedComplete -= 1
				if selectedComplete < 0: selectedComplete = 0
			else:
				print(repr(char))
		else:
			print(repr(char))
		eraseState(n_lines)

def read_cmd_from_file():
	f = open("alice_murders_bob_brutally_hahahaha.txt", "r")
	t = re.sub(r"[ \t]*#.*\n", "", f.read()).split("\n")
	f.close()
	nextLine = 0
	for lineno in range(len(t)):
		if t[lineno].startswith("> "):
			t[lineno] = t[lineno][2:]
			nextLine = lineno + 1
	while t[nextLine].startswith("#"): nextLine += 1
	t[nextLine] = "> " + t[nextLine]
	f = open("alice_murders_bob_brutally_hahahaha.txt", "w")
	f.write("\n".join(t))
	f.close()
	exec_cmd(t[nextLine][2:].split(" "))
	print(f"[From file] {t[nextLine][2:]}")

def exec_cmd(cmd: list[str]):
	func = None
	for ex in commands:
		if ex[0] == cmd[0]:
			func = ex[1]

	if isinstance(func, typing.Callable):
		func(cmd[1:])
	else:
		print("Invalid command")

def main():
	while True:
		cmd = get_command()
		if len(cmd) == 1 and cmd[0] == '':
			read_cmd_from_file()
		else:
			exec_cmd(cmd)
main()
