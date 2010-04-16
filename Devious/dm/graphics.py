import logging

import pygame
from pygame.locals import *

WINSIZE = (1024,800)

def create_window(full = False):
    flags = DOUBLEBUF
    if full:
        logging.debug("Fullscreen mode")
        flags |= FULLSCREEN
    screen = pygame.display.set_mode(WINSIZE, flags)
    empty = pygame.Surface(WINSIZE).convert()
    pygame.mouse.set_visible(True)
    return screen, empty

