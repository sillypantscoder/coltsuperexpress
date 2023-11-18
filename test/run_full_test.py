import subprocess
import os
import time
import test_client_lib as test
import test_client_command_getter as getter
import requests

filenames = [f"tests/{f}" for f in os.listdir("tests")]

def print_result(returns: tuple[bool, str]):
	if not returns[0]:
		print(getter.RED + "*", getter.RESET, end=getter.YELLOW)
	print(returns[1], getter.RESET, sep="")

def run_test(filename: str):
	print("Begin test for:", filename)
	test.reset_file(filename)
	p = subprocess.Popen(["python3", "main.py"], cwd=os.path.split(os.getcwd())[0], stdout=subprocess.PIPE)
	if p.stdout != None: p.stdout.readline()
	else: time.sleep(1)
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

if __name__ == "__main__":
	for file in filenames:
		run_test(file)
