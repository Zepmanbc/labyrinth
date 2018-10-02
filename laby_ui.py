#! /usr/bin/env python3
# coding: utf-8

"""
generate the GUI for the labyrinth game
init
call menu_loop() => show menu
call game_loop(labyrinth_code) => start a game
"""

import pygame
from pygame.locals import *

from laby_gen import *

# une representation graphique en utilisant pygame
# une classe qui s'occupe de la représentation graphique


class LabyGUI():
    """ CLass that generate the GUI"""
    STEP = 30

    def __init__(self):
        pygame.init()
        self.myfont = pygame.font.SysFont('Courier', 25, True)
        self.window = pygame.display.set_mode((640, 480))

    def game_loop(self, laby):
        """
        loop for a game laby
        """
        self.laby = laby[0]
        self.longuest = laby[1]
        self.last_case = self.longuest[-1]
        move_left = len(self.longuest) - 1
        # pygame.draw.rect(self.window,
        #                  pygame.Color('#FFFFFFFF'),
        #                  (0, 0, 640, 480))
        self.load_laby(self.laby)
        self.perso = Perso(self.window, self.STEP, self.laby, move_left)
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
                    print(event.key)
                    if event.key == 113:  # Q
                        loop = False
                    if event.key == K_DOWN:
                        self.perso.down()
                    if event.key == K_UP:
                        self.perso.up()
                    if event.key == K_RIGHT:
                        self.perso.right()
                    if event.key == K_LEFT:
                        self.perso.left()
                self.load_laby(self.laby)
                self.load_treasure(self.last_case)
                move_left = self.perso.load()
                self.bottom_text(move_left)
                if move_left <= 0:
                    perso_position = self.perso.return_position()
                    if perso_position == self.last_case:
                        self.end_party_text("You Win!!!")
                    else:
                        self.end_party_text("You Loose...")
                    self.show_path(self.longuest)
                    self.perso.load()
                pygame.display.flip()

    def bottom_text(self, move_left):
        label = self.myfont.render("moves left : {}".format(move_left),
                                   0, (0, 0, 0))
        self.window.blit(label, (10, 450))

    def end_party_text(self, text):
        label = self.myfont.render(text, 0, (0, 0, 0))
        self.window.blit(label, (350, 450))

    def load_treasure(self, case):
        """show the treasure icon to the specified case"""
        treasure = pygame.image.load("data/treasure.png").convert_alpha()
        self.window.blit(treasure, self.coord(case))

    def load_laby(self, code):
        """inside method for showing the laby"""
        # background => white for the moment
        pygame.draw.rect(self.window,
                         pygame.Color('#FFFFFFFF'),
                         (0, 0, 640, 480))
        x_pos, y_pos = 0, 0
        for row in code:
            x_pos = 0
            for column in row:
                fond = pygame.image.load("data/"+column+".png").convert_alpha()
                self.window.blit(fond, (x_pos, y_pos))
                x_pos += self.STEP
            y_pos += self.STEP

    def show_path(self, path):
        for case in path:
            position = pygame.image.load("data/red_dot.png").convert_alpha()
            self.window.blit(position, self.coord(case))

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

    def coord(self, case):
        """return pixel postision from a grid coordonates"""
        x_pos = case[0] * self.STEP
        y_pos = case[1] * self.STEP
        return (x_pos, y_pos)


class Perso():
    """Class that generate the perso"""
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

    def __init__(self, window, step, laby, move_left):
        """init the perso moves with the GUI object
        the step (nbr of pixel for 1 move)
        laby is the labyrith code"""
        self.window = window
        self.step = step
        self.laby = laby
        self.move_left = move_left
        # convert_alpha pour la gestion de la transparence
        self.perso = pygame.image.load(self.PERSO).convert_alpha()
        self.position_perso = self.perso.get_rect()
        self.window.blit(self.perso, self.position_perso)

    def authorized_move(self, direction):
        """test if the destination is authorized"""
        pos_x, pos_y = self.return_position()  # current perso position
        case = self.laby[pos_y][pos_x]  # get current case code
        auth = self.MOVES[case]  # translate code to walls positions
        # print(pos_x, pos_y)
        # print(case)
        for n in range(4):  # test the 4 walls with the direction
            if direction[n] == 1 and auth[n] == 0:
                self.move_left -= 1
                return True
        return False

    def right(self):
        """move the perso on the right case if possible"""
        if self.authorized_move((0, 1, 0, 0)):
            self.position_perso = self.position_perso.move(self.step, 0)

    def left(self):
        """move the perso on the left case if possible"""
        if self.authorized_move((0, 0, 0, 1)):
            self.position_perso = self.position_perso.move(-self.step, 0)

    def up(self):
        """move the perso on the upper case if possible"""
        if self.authorized_move((1, 0, 0, 0)):
            self.position_perso = self.position_perso.move(0, -self.step)

    def down(self):
        """move the perso on the down case if possible"""
        if self.authorized_move((0, 0, 1, 0)):
            self.position_perso = self.position_perso.move(0, self.step)

    def load(self):
        """refresh the new position"""
        self.window.blit(self.perso, self.position_perso)
        return self.move_left

    def return_position(self):
        """get a x,y position on the table"""
        pos_x = int(self.position_perso.left/self.step)
        pos_y = int(self.position_perso.top/self.step)
        return(pos_x, pos_y)


def main():
    """Test function"""
    game = LabyGUI()
    # game.menu_loop()
    labyrinth = LabyGenerator()
    game.game_loop(labyrinth.generate(21, 15))
    # game.game_loop(labyrinth.generate(10, 10))
    # game.game_loop(labyrinth.getout("0"))

if __name__ == "__main__":
    main()
