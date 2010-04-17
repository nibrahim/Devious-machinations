import logging

from common import std_tools

NAME = "Tutorial level : Leverage"

tools = []

def _create_tools(game_window):
    b0 = std_tools.Ball(game_window.world,
                        game_window.space,
                        game_window.main_window,
                        "data/tennis_ball.png",
                        0,
                        0,
                        20,
                        (200,200,255),
                        game_window.g2w,
                        game_window.w2g,
                        game_window.scale,
                        False)
    b0.name = "Tennis ball"
    b1 = std_tools.Ball(game_window.world,
                        game_window.space,
                        game_window.main_window,
                        "data/bowling_ball.png",
                        0,
                        0,
                        200,
                        (50,50,50),
                        game_window.g2w,
                        game_window.w2g,
                        game_window.scale,
                        True)
    b1.name = "Bowling ball"
    l0 = std_tools.Lever(game_window.world,
                         game_window.space,
                         game_window.main_window,
                         "data/lever.png",
                         0,
                         0,
                         game_window.g2w,
                         game_window.w2g,
                         game_window.scale,
                         True)
    l0.name = "See saw"
    return b0, b1, l0

def init(game_window):
    b0, b1, l0 = _create_tools(game_window)
    
    
    tools.extend([b0, b1, l0])
    
