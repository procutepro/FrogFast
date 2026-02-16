import frogfast.c.main as c_commands
import frogfast.pythonc.main as python_commands


def main() -> None:
    while True:
        raw = input("frogfast> ").strip()
        if not raw:
            continue

        command = raw.split()
        code = python_commands.main(command)
        print(f"code:{code}")

        if code == 45:
            break

        if code == 9:
            c_commands.main(command)
