from src.Game import *
import os
import subprocess
import sys


def set_up(packages):

    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip3", "install", package])


def main():
    os.system('color')
    #set_up(["numpy", "keyboard"])
    g = Game()
    g.begin_game()
    g.game_round()


if __name__ == "__main__":
    main()
