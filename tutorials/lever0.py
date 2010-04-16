#!/usr/bin/env python

import ode
import time
import math
import pygame
import random
from pygame.locals import DOUBLEBUF, KEYDOWN, QUIT, K_ESCAPE, K_LCTRL, KEYUP

from common import *


class Ball(pygame.sprite.Sprite):
    def __init__(self, world, space, x, y, density = 50):
        super(Ball,self).__init__()
        self.image = pygame.Surface((40, 40)).convert()
        self.image.set_colorkey((0,0,0))
        pygame.draw.circle(self.image, (200, 0, 200), (20, 20), 20, 0)
        self.rect = self.image.get_rect()
        self.rect.center = x, y

        # Body parameters for dynamics
        self.body = ode.Body(world)
        m = ode.Mass()
        m.setSphere(density, 20/SCALE) 
        self.body.setMass(m)
        self.body.setPosition(g_to_w(x, y ,0))

        # Geom parameters for collision detection.
        self.geom = ode.GeomSphere(space, 5)
        self.geom.setBody(self.body)

    def disable(self):
        self.geom.disable()
        self.body.disable()

    def enable(self):
        x, y = self.rect.center
        self.body.setPosition(g_to_w(x, y, 0))
        self.geom.enable()
        self.body.enable()
        
    def throw(self):
        print "Adding force"
        self.body.addForce((0,5000000,0))

    def update(self):
        x, y, z = w_to_g(*self.body.getPosition())

        self.rect.center = x, y
        if 450<x<550 and 450 < y < 550:
            print "We're done!"
            raise SystemExit

class Lever(pygame.sprite.Sprite):
    def __init__(self, world, space, x, y):
        super(Lever, self).__init__()
        self.image = pygame.Surface((200, 20)).convert_alpha()
        self.image.fill((0, 200, 200))
        self.original = self.image
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.rotation = 0

        # Body parameters for dynamics
        self.body = ode.Body(world)
        m = ode.Mass()
        m.setBox(50, 200/SCALE, 20/SCALE, 40/SCALE) 
        self.body.setMass(m)
        self.body.setPosition(g_to_w(x, y ,0))
        
        # Geom parameters for collision detection.
        self.geom = ode.GeomBox(space, (200/SCALE, 20/SCALE, 40/SCALE))
        self.geom.setBody(self.body)
        

    def update(self):
        x, y, z = w_to_g(*self.body.getPosition())
        qw, qx, qy, qz = self.body.getQuaternion()
        rotation = ((math.asin(2*qx*qy + 2*qz*qw) * 180)/math.pi)
        self.image = pygame.transform.rotate(self.original, rotation)
        self.rect = self.image.get_rect()
        # print self.body.getLinearVel()
        # print self.body.getPosition(),
        # print x,y
        self.rect.center = x, y


def create_world():
    "Creates the world and related components"
    world = ode.World()
    world.setGravity( (0, -9.81, 0) )
    world.setERP(1)
    world.setCFM(1E-5)
    return world

def create_space():
    "Creates the space for collision detection"
    space = ode.Space()
    floor = ode.GeomPlane(space, (0, 1, 0), -60)
    return space


def create_sprites(world, space, jgroup0, jgroup1):
    top_ball = Ball(world, space, 175, 10, 350)
    l = Lever(world, space, 256, 366)
    jgroup0.attach(l.body, ode.environment)
    jgroup0.setAnchor(l.body.getPosition())
    barrier = Ball(world, space, 360, 400)
    jgroup1.attach(barrier.body, ode.environment)
    jgroup1.setAnchor(barrier.body.getPosition())
    right_ball = Ball(world, space, 348, 320, 1)
    return [top_ball, l, right_ball, barrier]

def create_window():
    screen = pygame.display.set_mode((1024, 1024), DOUBLEBUF)#)|FULLSCREEN)
    empty = pygame.Surface((1024, 1024)).convert()
    pygame.mouse.set_visible(False)
    return screen, empty

def near_callback(args, g0, g1):
    contacts = ode.collide(g0, g1)
    world, contactgroup = args
    for c in contacts:
        c.setBounce(1)
        c.setMu(0)
        c.setMu2(0)
        j = ode.ContactJoint(world, contactgroup, c)
        j.attach(g0.getBody(), g1.getBody())

    
def main_loop(screen, empty, world, space, spheres):
    ball = spheres[0]
    ball.disable()
    group = pygame.sprite.Group(*spheres[1:])
    fps = 40
    iters_per_frame = 5
    dt = 1.0/fps
    clock = pygame.time.Clock()
    contactgroup = ode.JointGroup()
    count = 0
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
        count += 1
        if count == 15:
            ball.enable()
            group.add(ball)
        group.clear(screen, empty)
        group.update()
        group.draw(screen)
        x,y,z = w_to_g(-200, -60,0)
        pygame.draw.lines(screen,(250,250,250),False,[(x,y),(1024,y)])
        pygame.draw.lines(screen,(250,0,0),False,[(400,y-50),(450,y),(550,y),(600,y-50)])
        pygame.display.flip()
    


def main():
    world = create_world()
    space = create_space()
    screen, empty = create_window()
    j1 = ode.BallJoint(world)
    j2 = ode.BallJoint(world)
    spheres = create_sprites(world, space, j1, j2)
    main_loop(screen, empty, world, space, spheres)
    
if __name__ == "__main__":
    main()

    
