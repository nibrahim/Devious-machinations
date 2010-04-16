import logging

import pygame
from pygame.locals import *

WINSIZE = (640,480)

class GameWindow(object):
    def __init__(self, frame_rate, full = False):
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
        self.screen = screen
        self.empty = empty
        self.clock = pygame.time.Clock()
        self.frame_rate = frame_rate


    def handle_events(self):
        "Handle all events during a frame of animation"
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and
                                      event.key == K_ESCAPE):
                logging.info("Exit requested")
                raise SystemExit

    def sync_frames(self):
        "Introduces necessary delays to limit fps"
        self.clock.tick(self.frame_rate)

    def level_setup(self, level):
        "Given a level object, set it up in the game window"
        logging.info("Setting up level '%s'"%level.NAME)
        f = pygame.font.Font("data/Dalila.ttf", 20)
        text = f.render(level.NAME, True, (250, 250, 250))
        pos_x, pos_y = WINSIZE
        pos_x *= 0.60
        pos_y -= (text.get_height() + 15)
        self.screen.blit(text, (pos_x, pos_y))
        self.empty.blit(text, (pos_x, pos_y))

    def update(self):
        "Updates the screen in the animation loop"
        pygame.display.flip()
