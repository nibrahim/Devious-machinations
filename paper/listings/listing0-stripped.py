#!/usr/bin/env python

import pygame
from pygame.locals import *

class Ball(pygame.sprite.Sprite):
    "The ball which we will be moving on the screen"
    def __init__(self, x, y):
        self.image = pygame.Surface((40, 40)).convert()
        pygame.draw.circle(self.image, (200, 0, 200), (20, 20), 20, 0)
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        super(Ball,self).__init__()

    def update(self):
        x, y = self.rect.center
        self.rect.center = x+1, y+1


def create_window():
    "Creates our initial game window"
    screen = pygame.display.set_mode((512, 512), DOUBLEBUF) 
    empty = pygame.Surface((512, 512)).convert() 
    return screen, empty


def main():
    screen, empty = create_window()
    group = pygame.sprite.Group(Ball(10,10))
    clock = pygame.time.Clock()
    for i in range(200): 
        clock.tick(100)
        group.clear(screen, empty)
        group.update()
        group.draw(screen)
        pygame.display.flip()
    return 0
        

if __name__ == "__main__":
    import sys
    sys.exit(main())
        
        
