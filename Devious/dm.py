#!/usr/bin/env python

from dm import utils
import logging
logging.basicConfig(level = logging.INFO,
                    format = "%(levelname)-8s|%(module)-12s:%(lineno)d - %(message)s")
                    
def main(fullscreen):
    logging.debug("Creating Window")
    utils.create_window(fullscreen)

if __name__ == "__main__":
    import sys
    full = False
    if "-f" in sys.argv: full = True
    if "-v" in sys.argv: logging.root.setLevel(logging.DEBUG)
    main(full)
