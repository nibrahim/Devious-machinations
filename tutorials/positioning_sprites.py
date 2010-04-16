#!/usr/bin/env python


from common import *

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Ball,self).__init__()
        self.image = pygame.Surface((40, 40)).convert()
        self.image.set_colorkey((0,0,0))
        pygame.draw.circle(self.image, (200, 0, 200), (20, 20), 20, 0)
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.picked_up = False


    def pick_up(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            print "Yes"
            self.picked_up = True

    def drop(self):
        self.picked_up = False


    def update(self):
        if self.picked_up:
            self.rect.center = pygame.mouse.get_pos()
        else:
            x, y = self.rect.center
            x+=2
            y+=0.5
            self.rect.center = x, y



def main():
    screen, empty = create_window()
    ball = Ball(128,128)
    group = pygame.sprite.Group(ball)
    fps = 40
    clock = pygame.time.Clock()
    while True:
        clock.tick(40)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and
                                      event.key == K_ESCAPE):
                return
            if event.type == MOUSEBUTTONDOWN:
                ball.pick_up()
            if event.type == MOUSEBUTTONUP:
                ball.drop()
                
                
        group.clear(screen, empty)
        group.update()
        group.draw(screen)
        pygame.display.flip()

        


if __name__ == "__main__":
    main()

    
