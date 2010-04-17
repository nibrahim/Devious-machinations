import logging

import pygame

from common import std_tools

NAME = "Tutorial level : Leverage"
INSTRUCTIONS = "Get the yellow tennis ball into the stone container"

tools = []

bucket = pygame.image.load("data/endbucket.png");

def _inital_positions(game_window, tennis_ball, bucket):
    tennis_ball.place(300,300)
    bucket.place(550,350)


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

    b2 = std_tools.Ball(game_window.world,
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
                        True)
    b2.name = "Tennis ball"

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
    l0.name = "Lever 0"

    l1 = std_tools.Lever(game_window.world,
                         game_window.space,
                         game_window.main_window,
                         "data/lever.png",
                         0,
                         0,
                         game_window.g2w,
                         game_window.w2g,
                         game_window.scale,
                         True)
    l1.name = "Lever 1"
    
    e = std_tools.Bucket(game_window.world,
                         game_window.space,
                         game_window.main_window,
                         "data/endbucket.png",
                         0,
                         0,
                         game_window.g2w,
                         game_window.w2g,
                         game_window.scale,
                         False)
    e.name = "Bucket"
    return b0, b1, b2, l0, l1, e

def init(game_window):
    b0, b1, b2, l0, l1, e = _create_tools(game_window)
    _inital_positions(game_window, b0, e)
    tools.extend([b0, b1, b2, l0, l1, e])

def success():
    b0, b1, b2, l0, l1, e = tools
    return e.rect.contains(b0)
    

