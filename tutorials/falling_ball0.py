#!/usr/bin/env python

import ode
import time
import pygame
from pygame.locals import DOUBLEBUF, KEYDOWN, QUIT, K_ESCAPE, K_LCTRL, KEYUP

# The world is 512x512 pixels wide.
# Each pixel is approximately 0.25m


def g_to_w(x, y, z):
    "Converts the x,y and z coordinates from graphics to world (pygame to ODE)"
    rx = x - 256
    ry = 256 - y
    rz = 0
    return (rx, ry, rz)

    
def w_to_g(x, y, z):
    "Converts the x,y and z coordinates from world to graphics (ODE to pygame)"
    rx = x + 256
    ry = 256 - y
    rz = 0
    return (rx, ry, rz)




class Ball(pygame.sprite.Sprite):
    def __init__(self, world, space):
        super(Ball,self).__init__()
        self.image = pygame.Surface((40, 40)).convert()
        pygame.draw.circle(self.image, (200, 0, 200), (20, 20), 15, 0)
        self.rect = self.image.get_rect()
        self.rect.center = 256, 256

        # self.world = world
        self.body = ode.Body(world)
        m = ode.Mass()
        m.setSphere(1000, 5)
        self.body.setMass(m)
        print "Initial setting ", g_to_w(0, 0 ,0)
        self.body.setPosition(g_to_w(256, 256 ,0))


    def throw(self):
        print "Adding force"
        self.body.addForce((0,500000000,0))


    def update(self):
        x,y,z = w_to_g(*self.body.getPosition())

        # print x," ",y," ",z
        self.rect.center = x, y



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
    floor = ode.GeomPlane(space, (0, 1, 0), 0)
    return space

def create_sphere(world, space):
    b = Ball(world, space)
    return b

def create_window():
    screen = pygame.display.set_mode((512, 512), DOUBLEBUF)#)|FULLSCREEN)
    empty = pygame.Surface((512, 512)).convert()
    pygame.mouse.set_visible(False)
    return screen, empty

def main_loop(screen, empty, world, space, sphere):
    group = pygame.sprite.GroupSingle(sphere)
    lasttime = time.time()
    fps = 30
    dt = 1.0/fps
    clock = pygame.time.Clock()
    while True:
        clock.tick(fps)
        world.step(dt)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and
                                      event.key == K_ESCAPE):
                return
            if event.type == KEYUP:
                if event.key == K_LCTRL:
                    sphere.throw()
        group.clear(screen, empty)
        group.update()
        group.draw(screen)
        pygame.display.flip()
    


def main():
    world = create_world()
    space = create_space()
    screen, empty = create_window()
    sphere = create_sphere(world, space)
    main_loop(screen, empty, world, space, sphere)
    
    



if __name__ == "__main__":
    main()

    
