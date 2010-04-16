#!/usr/bin/env python

import logging


from dm import graphics
from dm import utils

logging.basicConfig(level = logging.INFO,
                    format = "%(levelname)-8s|%(module)-12s:%(lineno)d - %(message)s")

def anim_loop(screen, empty):
    "The main animation loop which plays the game"
    logging.debug("Starting animation loop")
    fps = 30
    while True:
        graphics.handle_events()
        graphics.sync_frames(fps)
        

def level_setup(level, screen):
    "The function that sets up the tools in the level and places the intial objects"
    pass
    
                    
def main(fullscreen):
    logging.debug("Creating Window")
    screen, empty = graphics.create_window(fullscreen)
    level = utils.load_level("0")
    try:
        level_setup(level, screen)
    except Exception,m:
        logging.critical("Error during setting up level - '%s'"%m)
    anim_loop(screen, empty)

if __name__ == "__main__":
    import sys
    full = False
    if "-f" in sys.argv: full = True
    if "-v" in sys.argv: logging.root.setLevel(logging.DEBUG)
    main(full)
