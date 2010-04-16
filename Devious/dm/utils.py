import logging

class Error(Exception): pass

class LevelError(Error): pass
    
def load_level(l):
    "Loads the level in levels/level_l and returns it"
    lname = "level_%s"%l
    try:
        logging.info("Loading level %s"%lname)
        level = __import__("dm.levels", fromlist = [lname])
        return getattr(level,lname)
    except ImportError,m:
        err = "Couldn't load the requested level '%s' - Error was '%s'"%(l, m)
        logging.critical(err)
        raise LevelError(err)
