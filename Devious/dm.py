#!/usr/bin/env python

import logging

from dm import graphics
from dm import utils


logging.basicConfig(level = logging.INFO,
                    format = "%(levelname)-8s|%(module)12s:%(lineno)d - %(message)s")

FPS = 30

def anim_loop(game_window):
    "The main animation loop which plays the game"
    logging.debug("Starting animation loop")
    finished = False
    while True:
        game_window.handle_events()
        game_window.sync_frames()
        if not finished:
            finished = game_window.update()

                    
def main():
    logging.debug("Creating Window")
    game_window = graphics.GameWindow(FPS)
    level = utils.load_level("0")
    try:
        game_window.level_setup(level)
    except KeyboardInterrupt,m:
        logging.critical("Error during setting up level - '%s'"%m)
    anim_loop(game_window)

if __name__ == "__main__":
    import sys
    if "-v" in sys.argv: logging.root.setLevel(logging.DEBUG)
    main()
