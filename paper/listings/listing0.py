#!/usr/bin/env python

import pygame
from pygame.locals import *

class Ball(pygame.sprite.Sprite):
    "The ball which we will be moving on the screen"
    def __init__(self, x, y):
        # Create the image for the sprite
        self.image = pygame.Surface((40, 40)).convert()
        # Draw a little circle inside it
        pygame.draw.circle(self.image, (200, 0, 200), (20, 20), 20, 0)
        # The sprite needs a rect attribute for positioning
        # and collision detection
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        super(Ball,self).__init__()

    def update(self):
        x, y = self.rect.center
        self.rect.center = x+1, y+1


def create_window():
    "Creates our initial game window"
    # Creates a 512x512 window
    screen = pygame.display.set_mode((512, 512), DOUBLEBUF) 
    # Creates and empty surface to to be used to clearing the screen
    empty = pygame.Surface((512, 512)).convert() 
    return screen, empty


def main():
    screen, empty = create_window()
    # Create a group holding the ball
    group = pygame.sprite.Group(Ball(10,10))
    # Initialise a timer
    clock = pygame.time.Clock()
    # 200 animation frames
    for i in range(200): 
        # Limit framerate to 30fps
        clock.tick(100)
        # Clear the screen
        group.clear(screen, empty)
        # Update all sprites in the group
        group.update()
        # Draw them on the screen
        group.draw(screen)
        # Flip the display buffer
        pygame.display.flip()
    return 0
        

if __name__ == "__main__":
    import sys
    sys.exit(main())
        
        
