#!/usr/bin/env python

from dm import graphics
import logging
logging.basicConfig(level = logging.INFO,
                    format = "%(levelname)-8s|%(module)-12s:%(lineno)d - %(message)s")

def anim_loop(screen, empty):
    logging.debug("Starting animation loop")
    
                    
def main(fullscreen):
    logging.debug("Creating Window")
    screen, empty = graphics.create_window(fullscreen)
    
    anim_loop(screen, empty)

    

if __name__ == "__main__":
    import sys
    full = False
    if "-f" in sys.argv: full = True
    if "-v" in sys.argv: logging.root.setLevel(logging.DEBUG)
    main(full)
