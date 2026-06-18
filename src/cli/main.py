import sys
from src.cli.repl import REPL

def main():
    print("ModelX v1.0")
    repl = REPL()
    repl.loop()

if __name__ == "__main__":
    main()
