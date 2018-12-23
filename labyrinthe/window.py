#! /usr/bin/env python3
# coding: utf-8

import pygame
from pygame.locals import *


class Window():
    """ CLass that generate the GUI"""

    def __init__(self):
        pygame.init()
        self.myfont = pygame.font.SysFont('Courier', 25, True)
        self.window = pygame.display.set_mode((640, 480))


def main():
    """Test function"""
    window = Window()
    pass

if __name__ == "__main__":
    main()
