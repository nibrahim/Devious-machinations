import logging

import pygame
from pygame.locals import *

WINSIZE = (640,480)

clock = pygame.time.Clock()

def create_window(full = False):
    "Create the window at the start"
    flags = DOUBLEBUF
    if full:
        logging.debug("Fullscreen mode")
        flags |= FULLSCREEN
    logging.info("Resolution specified at %dx%d"%WINSIZE)
    screen = pygame.display.set_mode(WINSIZE, flags)
    pygame.display.set_caption("Devious Machinations")
    empty = pygame.Surface(WINSIZE).convert()
    pygame.mouse.set_visible(True)
    pygame.font.init()
    return screen, empty


def handle_events():
    "Handle all events during a frame of animation"
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and
                                  event.key == K_ESCAPE):
            logging.info("Exit requested")
            raise SystemExit

def sync_frames(frame_rate):
    "Introduces necessary delays to limit fps"
    clock.tick(frame_rate)
