#!/usr/bin/env python

import pygame
from pygame.locals import DOUBLEBUF, KEYDOWN, QUIT, K_ESCAPE

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball,self).__init__(self.containers)
        self.x = 256
        self.y = 10
        self.image = pygame.Surface((40, 40)).convert()
        pygame.draw.circle(self.image, (200,200,200), (20,20),15,0)
        self.rect = self.image.get_rect()
        self.rect.center = 256,10
        
    def update(self):
        self.y += 2
        self.rect.center = (self.x, self.y)

def initialise_screen():
    global group, screen, empty
    screen = pygame.display.set_mode((512, 512), DOUBLEBUF)#)|FULLSCREEN)
    empty = pygame.Surface((512,512)).convert()
    pygame.mouse.set_visible(False)
    group = pygame.sprite.RenderPlain()
    Ball.containers = group
    ball = Ball()

def start_loop():
    global group, screen, empty
    clock = pygame.time.Clock()
    count = 0
    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
        group.clear(screen,empty)
        group.update()
        group.draw(screen)
        count += 2
        if count > 512:
            break
        pygame.display.flip()

if __name__ == "__main__":
    initialise_screen()
    start_loop()
    
        
        
    
