import logging

class Error(Exception): pass

class LevelError(Error): pass
    
def load_level(l):
    "Loads the level in levels/level_l and returns it"
    lname = "dm.levels.level_%s"%l
    try:
        level = __import__(lname)
        return level
    except ImportError,m:
        err = "Couldn't load the requested level '%s' - Error was '%s'"%(l, m)
        logging.critical(err)
        raise LevelError(err)
