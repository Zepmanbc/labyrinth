#! /usr/bin/env python3
# coding: utf-8
import pygame
from pygame.locals import *

from laby_gen import *

"""
une representation graphique en utilisant pygame
une classe qui s'occupe de la représentation graphique
"""


class laby_ui():

    STEP = 30

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((640, 480))

    def game_loop(self, laby):
        """
        loop for a game laby
        """
        self.laby = laby
        pygame.draw.rect(self.window,
                         pygame.Color('#FFFFFFFF'),
                         (0, 0, 640, 480))
        self.load_laby(self.laby)
        self.perso = Perso(self.window, self.STEP, self.laby)
        pygame.display.flip()

        # pour rester appuyé sur le bouton
        pygame.key.set_repeat(400, 30)

        loop = True
        while loop:
            # pour limiter à 30fps
            pygame.time.Clock().tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                if event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        self.perso.down()
                    if event.key == K_UP:
                        self.perso.up()
                    if event.key == K_RIGHT:
                        self.perso.right()
                    if event.key == K_LEFT:
                        self.perso.left()
                pygame.draw.rect(self.window,
                                 pygame.Color('#FFFFFFFF'),
                                 (0, 0, 640, 480))
                self.load_laby(self.laby)
                self.perso.load()
                # self.window.blit(perso, position_perso)
                pygame.display.flip()

    def load_laby(self, code):
        """
        inside method for showing the laby
        """
        x_pos, y_pos = 0, 0
        # pygame.draw.rect(self.window,pygame.Color('#FFFFFFFF'),(0,0,640,480))
        for row in code:
            x_pos = 0
            for column in row:
                fond = pygame.image.load("data/"+column+".png").convert_alpha()
                self.window.blit(fond, (x_pos, y_pos))
                x_pos += self.STEP
            y_pos += self.STEP

    def menu_loop(self):
        """
        first screen
        """
        fond = pygame.image.load("data/menu.jpg").convert()
        self.window.blit(fond, (0, 0))
        pygame.display.flip()

        loop = True
        while loop:
            # pour limiter à 30fps
            pygame.time.Clock().tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    loop = False
                if event.type == KEYDOWN:
                    loop = False
                self.window.blit(fond, (0, 0))
                pygame.display.flip()


class Perso():

    PERSO = "data/perso.png"
    MOVES = {
        "0": (0, 0, 0, 0),
        "1": (0, 1, 0, 0),
        "2": (0, 0, 1, 0),
        "3": (0, 0, 0, 1),
        "4": (1, 0, 0, 0),
        "5": (1, 1, 0, 0),
        "6": (0, 1, 1, 0),
        "7": (0, 0, 1, 1),
        "8": (1, 0, 0, 1),
        "9": (1, 1, 1, 0),
        "A": (0, 1, 1, 1),
        "B": (1, 0, 1, 1),
        "C": (1, 1, 0, 1),
        "D": (1, 1, 1, 1),
        "E": (0, 1, 0, 1),
        "F": (1, 0, 1, 0)
    }

    def __init__(self, window, step, laby):
        self.window = window
        self.step = step
        self.laby = laby
        # convert_alpha pour la gestion de la transparence
        self.perso = pygame.image.load(self.PERSO).convert_alpha()
        self.position_perso = self.perso.get_rect()
        self.window.blit(self.perso, self.position_perso)

    def authorized_move(self, direction):
        x, y = self.return_position()
        case = self.laby[y][x]
        auth = self.MOVES[case]
        print(x, y)
        print(case)
        for n in range(4):
            if direction[n] == 1 and auth[n] == 0:
                return True
        return False

    def right(self):
        if self.authorized_move((0, 1, 0, 0)):
            self.position_perso = self.position_perso.move(self.step, 0)

    def left(self):
        if self.authorized_move((0, 0, 0, 1)):
            self.position_perso = self.position_perso.move(-self.step, 0)

    def up(self):
        if self.authorized_move((1, 0, 0, 0)):
            self.position_perso = self.position_perso.move(0, -self.step)

    def down(self):
        if self.authorized_move((0, 0, 1, 0)):
            self.position_perso = self.position_perso.move(0, self.step)

    def load(self):
        self.window.blit(self.perso, self.position_perso)

    def return_position(self):
        pos_x = int(self.position_perso.left/self.step)
        pos_y = int(self.position_perso.top/self.step)
        return(pos_x, pos_y)


def main():
    game = laby_ui()
    game.menu_loop()
    labyrinth = Laby_gen()
    game.game_loop(labyrinth.generate(21, 15))

if __name__ == "__main__":
    main()
