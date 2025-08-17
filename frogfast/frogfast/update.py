import frogfast.pythonc.main as thing
import frogfast.c.main as thing2

def main():
    while True:
        command = input("frogfast> ").strip().split(" ")
        code = thing.main(command)
        print(f"code:{code}")
        if code == 45:
            break
        if code == 9:
            thing2.main(command)