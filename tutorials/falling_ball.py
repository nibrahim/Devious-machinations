#!/usr/bin/env python

import pygame
from pygame.locals import DOUBLEBUF, KEYDOWN, QUIT, K_ESCAPE, K_LCTRL, KEYUP

import ode


class Ball(pygame.sprite.Sprite):
    def __init__(self,world):
        super(Ball,self).__init__(self.containers)
        self.x = 256
        self.y = 256
        self.image = pygame.Surface((40, 40)).convert()
        pygame.draw.circle(self.image, (200,200,200), (20,20),15,0)
        self.rect = self.image.get_rect()
        self.rect.center = 256,10

        self.world = world
        self.body = ode.Body(world)
        m = ode.Mass()
        m.setSphere(6000, 0.0015)
        self.body.setPosition( (256,256,0) )
        self.body.addForce( (0,-500,0) )

    def throw(self):
        print "Adding force"
        self.body.addForce((0,-500,0))
    
    def update(self):
        print self.body.getForce()
        x,y,z = self.body.getPosition()
        u,v,w = self.body.getLinearVel()
        self.world.step(0.1)
        self.y  = y
        self.x  = x
        self.rect.center = (self.x, self.y)

def initialise_screen():
    global group, screen, empty, world
    screen = pygame.display.set_mode((512, 512), DOUBLEBUF)#)|FULLSCREEN)
    empty = pygame.Surface((512,512)).convert()
    pygame.mouse.set_visible(False)
    group = pygame.sprite.RenderPlain()
    Ball.containers = group

    world = ode.World()
    world.setGravity((0,9.81,0))

    ball = Ball(world)
    return ball
        
    
def start_loop(ball):
    global group, screen, empty
    clock = pygame.time.Clock()
    count = 0
    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
            if event.type == KEYUP:
                if event.key == K_LCTRL:
                    ball.throw()
        group.clear(screen,empty)
        group.update()
        group.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    ball = initialise_screen()
    start_loop(ball)
    
        
        
    
