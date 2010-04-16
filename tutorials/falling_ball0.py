#!/usr/bin/env python

import ode
import time
import pygame
import random
from pygame.locals import DOUBLEBUF, KEYDOWN, QUIT, K_ESCAPE, K_LCTRL, KEYUP

from common import *

# The world is 512x512 pixels wide.
# Each pixel is approximately 0.25m



class Ball(pygame.sprite.Sprite):
    def __init__(self, world, space, x, y):
        super(Ball,self).__init__()
        self.image = pygame.Surface((40, 40)).convert()
        self.image.set_colorkey((0,0,0))
        pygame.draw.circle(self.image, (200, 0, 200), (20, 20), 20, 0)
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.picked_up = False

        # Body parameters for dynamics
        self.body = ode.Body(world)
        m = ode.Mass()
        m.setSphere(20, 20/SCALE) 
        self.body.setMass(m)
        self.body.setPosition(g_to_w(x, y ,0))

        # Geom parameters for collision detection.
        self.geom = ode.GeomSphere(space, 5)
        self.geom.setBody(self.body)
        self.body.setLinearVel((15,0,0))

    def pick_up(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.body.disable()
            self.geom.disable()
            self.picked_up = True

    def drop(self):
        if self.picked_up:
            self.picked_up = False
            self.body.enable()
            self.geom.enable()
            x, y = self.rect.center
            self.body.setPosition(g_to_w(x, y, 0))
        
    def throw(self):
        print "Adding force"
        self.body.addForce((0,5000000,0))
        self.body.addForce((5000000,0,0))

    def update(self):
        if self.picked_up:
            self.rect.center = pygame.mouse.get_pos()
        else:
            x, y, z = w_to_g(*self.body.getPosition())
            # print self.body.getLinearVel()
            # print self.body.getPosition(),
            # print x,y
            self.rect.center = x, y

def create_sphere(world, space):
    retval = []
    for i in range(15):
        retval.append(Ball(world, space, random.randint(200, 300), random.randint(0,50)))
    return retval


def near_callback(args, g0, g1):
    # print "We're getting called ", g0, g1
    contacts = ode.collide(g0, g1)
    world, contactgroup = args
    for c in contacts:
        c.setBounce(1)
        c.setMu(0)
        c.setMu2(0)
        j = ode.ContactJoint(world, contactgroup, c)
        j.attach(g0.getBody(), g1.getBody())

    
def main_loop(screen, empty, world, space, spheres):
    group = pygame.sprite.Group(*spheres)
    fps = 40
    iters_per_frame = 5
    dt = 1.0/fps
    clock = pygame.time.Clock()
    contactgroup = ode.JointGroup()
    while True:
        clock.tick(fps)
        for i in range(iters_per_frame):
            space.collide((world, contactgroup), near_callback)
            world.step(dt)
            contactgroup.empty()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and
                                      event.key == K_ESCAPE):
                return
            if event.type == KEYUP:
                if event.key == K_LCTRL:
                    for i in spheres:
                        i.throw()

            if event.type == MOUSEBUTTONDOWN:
                for i in spheres:
                    i.pick_up()
            if event.type == MOUSEBUTTONUP:
                for i in spheres:
                    i.drop()
                        
        group.clear(screen, empty)
        group.update()
        group.draw(screen)
        pygame.display.flip()


def main():
    world = create_world()
    space = create_space()
    screen, empty = create_window()
    spheres = create_sphere(world, space)
    main_loop(screen, empty, world, space, spheres)
    
    



if __name__ == "__main__":
    main()

    
