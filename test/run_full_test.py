import subprocess
import os
import time
import test_client_lib as test
import test_client_command_getter as getter
import requests

filenames = ["alice_murders_bob_brutally_hahahaha.txt"]

def print_result(returns: tuple[bool, str]):
	if not returns[0]:
		print(getter.RED + "*", getter.RESET, end=getter.YELLOW)
	print(returns[1], getter.RESET, sep="")

def run_test(filename: str):
	test.reset_file(filename)
	p = subprocess.Popen(["python3", "main.py"], cwd=os.path.split(os.getcwd())[0])
	time.sleep(1)
	cmd: list[str] | None = test.read_cmd_from_file(filename)
	while cmd != None:
		out = test.exec_cmd(cmd)
		print_result(out)
		cmd = test.read_cmd_from_file(filename)
		if out[0] == False:
			print(f"\nFailed on line {test.get_lineno_from_file(filename)} of file {repr(filename)}; server status is:")
			print(requests.get("http://0.0.0.0:8080/status", timeout=10).text)
			break
	p.send_signal(2)
	p.wait()
	test.reset_file(filename)

run_test(filenames[0])
