SCALE = 4.0

import ode, pygame
from pygame.locals import *


def g_to_w(x, y, z):
    "Converts the x,y and z coordinates from graphics to world (pygame to ODE)"
    rx = (x - 256)/SCALE
    ry = (256 - y)/SCALE
    rz = 0
    return (rx, ry, rz)

    
def w_to_g(x, y, z):
    "Converts the x,y and z coordinates from world to graphics (ODE to pygame)"
    rx = SCALE*x + 256
    ry = 256 - SCALE*y
    rz = 0
    return (rx, ry, rz)


def create_world():
    "Creates the world and related components"
    world = ode.World()
    world.setGravity( (0, -9.81, 0) )
    world.setERP(0.8)
    world.setCFM(1E-5)
    return world

def create_space():
    "Creates the space for collision detection"
    space = ode.Space()
    floor = ode.GeomPlane(space, (0, 1, 0), -25)
    right_wall = ode.GeomPlane(space, (-1, 0, 0), -45)
    left_wall = ode.GeomPlane(space, (1, 0, 0), -45)
    return space

def create_window():
    screen = pygame.display.set_mode((512, 512), DOUBLEBUF)#)|FULLSCREEN)
    empty = pygame.Surface((512, 512)).convert()
    pygame.mouse.set_visible(True)
    return screen, empty
