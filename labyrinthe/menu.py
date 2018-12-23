#! /usr/bin/env python3
# coding: utf-8
"""
display the menu
"""
import pygame
# from pygame.locals import *


class Menu():
    """
    display the menu
    """

    CURSOR_DICT = {0: ["small", (280, 250), (10, 10)],
                   1: ["medium", (270, 300), (15, 13)],
                   2: ["large", (280, 350), (21, 15)],
                   3: ["quit", (290, 400), False]}
    CURSOR_POS = 0

    def __init__(self, window):
        """ init th window """
        self.window = window.window
        self.myfont = window.myfont

    @property
    def run(self):
        """ main function to run the menu screen """
        self.refresh_screen()
        loop = True
        while loop:
            # pour limiter à 30fps
            # pygame.time.Clock().tick(30)
            for event in pygame.event.get():
                if event.type == 12:  # pygame.QUIT:
                    loop = False
                if event.type == 2:  # KEYDOWN:
                    # print(event.key)
                    if event.key in [13, 271, 32]:  # Enter or Spacebar
                        message = self.CURSOR_DICT[self.CURSOR_POS][2]
                        return message
                    if event.key == 274:  # K_DOWN:
                        self.cursor_down()
                    if event.key == 273:  # K_UP:
                        self.cursor_up()
                self.refresh_screen()

    def refresh_screen(self):
        """ call the screen componants """
        self.show_background()
        self.write_menu()
        position = self.CURSOR_DICT[self.CURSOR_POS][1][1]
        self.cursor(position)
        pygame.display.flip()

    def show_background(self):
        """ background componant """
        pygame.draw.rect(self.window,
                         pygame.Color('#FFFFFFFF'),
                         (0, 0, 640, 480))
        menu_backgroung = pygame.image.load("data/menu.png").convert_alpha()
        self.window.blit(menu_backgroung, (0, 0))

    def write_menu(self):
        """ choices componants """
        for menu_choice in self.CURSOR_DICT.keys():
            text = self.CURSOR_DICT[menu_choice][0]
            position = self.CURSOR_DICT[menu_choice][1]
            label = self.myfont.render(text, 1, (0, 0, 0))
            self.window.blit(label, position)

    def cursor(self, position):
        """ show the cursor at the selectec position """
        cursor_img = pygame.image.load("data/perso.png").convert_alpha()
        self.window.blit(cursor_img, (220, position))

    def cursor_down(self):
        """ move the crusor down """
        if self.CURSOR_POS < 3:
            self.CURSOR_POS += 1
        else:
            self.CURSOR_POS = 0

    def cursor_up(self):
        """ move the cursor up """
        if self.CURSOR_POS > 0:
            self.CURSOR_POS -= 1
        else:
            self.CURSOR_POS = 3


def main():
    """ test function """
    from window import Window
    window = Window()
    print(Menu(window).run)
    # print(Menu.run(Menu(window)))
    pass

if __name__ == "__main__":
    main()
