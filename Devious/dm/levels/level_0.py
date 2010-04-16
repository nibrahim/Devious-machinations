import logging

from common import std_tools

NAME = "Tutorial level : Leverage"

tools = []

def init(game_window):
    b0 = std_tools.Ball(game_window.world,
                       game_window.space,
                       game_window.main_window,
                       0,
                       0,
                       game_window.g2w,
                       game_window.w2g,
                       game_window.scale)
    b0.name = "Ball 0"
    b1 = std_tools.Ball(game_window.world,
                       game_window.space,
                       game_window.main_window,
                       0,
                       0,
                       game_window.g2w,
                       game_window.w2g,
                       game_window.scale)
    b1.name = "Ball 1"
    tools.extend([b0, b1])
    
                       
    
    
