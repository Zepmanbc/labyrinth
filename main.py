#! /usr/bin/env python3
# coding: utf-8

from labyrinthe import *

def main():
    window = Window()
    running_game = True
    while running_game:
        game_choice = Menu(window).run
        if game_choice:
            laby = LabyGenerator()
            laby_data = laby.generate(game_choice[0], game_choice[1])
            game = LabyGUI()
            game.game_loop(laby_data)
            print(laby_data)
        else:
            running_game = False

if __name__ == "__main__":
    main()