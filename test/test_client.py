import test_client_command_getter as getter
from test_client_lib import exec_cmd, commands, read_cmd_from_file

def run_cmd_from_file() -> tuple[bool, str]:
	data = read_cmd_from_file("alice_murders_bob_brutally_hahahaha.txt")
	if data == None:
		return (False, "No more data from file!")
	print(f"[From file] {' '.join(data)}")
	return exec_cmd(data)

def print_result(returns: tuple[bool, str]):
	if not returns[0]:
		print(getter.RED + "*", getter.RESET, end=getter.YELLOW)
	print(returns[1], getter.RESET, sep="")

def main():
	while True:
		cmd = getter.get_command(commands)
		if len(cmd) == 1 and cmd[0] == '':
			print_result(run_cmd_from_file())
		else:
			print_result(exec_cmd(cmd))
main()
