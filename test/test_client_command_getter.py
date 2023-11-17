import typing
from test_client_lib import Command
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

def get_command(commands: list[Command]) -> list[str]:
	currentS: str = ""
	selectedComplete: int = 0
	def getSyntax(cmdname: str) -> "list[tuple[str, list[str] | type[int] | type[str]] | typing.Literal['...']]":
		for cmd in commands:
			if cmdname == cmd["name"]:
				return cmd["syntax"]
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
		if itemno - 1 < 0: return cmdname in [c["name"] for c in commands]
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
		if len(s) == 1: return [c["name"] for c in commands]
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
