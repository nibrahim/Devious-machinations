import math
import logging

import pygame
import ode

# States the tools can be in
RESERVE        = "RESERVE"        # In the sidebar
PICKED_UP      = "PICKED_UP"      # Being moved around
IN_MAIN_SCREEN = "IN_MAIN_SCREEN" # Placed on the screen
IN_SIMULATION  = "IN_SIMULATION"  # Participating in simulation

class Ball(pygame.sprite.Sprite):
    def __init__(self, world, space, main_window, x, y, g_to_w, w_to_g, scale ):
        super(Ball,self).__init__()
        self.image = pygame.Surface((40, 40)).convert()
        self.image.set_colorkey((0,0,0))
        pygame.draw.circle(self.image, (200, 255, 200), (20, 20), 20, 0)
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.picked_up = False
        self.g2w = g_to_w
        self.w2g = w_to_g
        self.scale = scale
        self.main_window = main_window
        self.state = RESERVE
        
        # Body parameters for dynamics
        self.body = ode.Body(world)
        m = ode.Mass()
        m.setSphere(20, 20/self.scale) 
        self.body.setMass(m)
        self.body.setPosition(self.g2w(x, y ,0))
        # self.body.setLinearVel((-15,0,0))

        # Geom parameters for collision detection.
        self.geom = ode.GeomSphere(space, 5)
        self.geom.setBody(self.body)
        self._physics_enable(False)

    def enable(self):
        if self.state == IN_MAIN_SCREEN:
            self._physics_enable(True)
            self.state = IN_SIMULATION

    def _physics_enable(self, status):
        "Used to turn the physics simulation for this object on or off"
        if status:
            self.body.enable()
            self.geom.enable()
        else:
            self.body.disable()
            self.geom.disable()

    def pick_up(self):
        if self.state != IN_SIMULATION:
            logging.debug("  We're inside with %s"%self.state)
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self._physics_enable(False)
                self.state = PICKED_UP

    def drop(self):
        if self.state == PICKED_UP:
            if self.main_window.collidepoint(pygame.mouse.get_pos()): #Dropping inside main window
                self.state = IN_MAIN_SCREEN
                x, y = self.rect.center
                self.body.setPosition(self.g2w(x, y, 0))
            else:
                self.state = RESERVE

    def update(self):
        if self.state == PICKED_UP:
            self.rect.center = pygame.mouse.get_pos()
        else:
            if self.state == IN_SIMULATION:
                x, y, z = self.w2g(*self.body.getPosition())
                self.rect.center = x, y
            

# class Lever(pygame.sprite.Sprite):
#     def __init__(self, world, space, main_window, x, y, g_to_w, w_to_g, scale):
#         super(Lever, self).__init__()
#         self.image = pygame.Surface((200, 20)).convert_alpha()
#         self.image.fill((0, 200, 200))
#         self.original = self.image
#         self.rect = self.image.get_rect()
#         self.rect.center = x, y
#         self.rotation = 0
#         self.g2w = g_to_w
#         self.w2g = w_to_g
#         self.scale = scale


#         # Body parameters for dynamics
#         self.body = ode.Body(world)
#         m = ode.Mass()
#         m.setBox(50, 200/self.scale, 20/self.scale, 40/self.scale) 
#         self.body.setMass(m)
#         self.body.setPosition(self.g2w(x, y ,0))
        
#         # Geom parameters for collision detection.
#         self.geom = ode.GeomBox(space, (200/self.scale, 20/self.scale, 40/self.scale))
#         self.geom.setBody(self.body)
        

#     def update(self):
#         x, y, z = self.w2g(*self.body.getPosition())
#         qw, qx, qy, qz = self.body.getQuaternion()
#         rotation = ((math.asin(2*qx*qy + 2*qz*qw) * 180)/math.pi)
#         self.image = pygame.transform.rotate(self.original, rotation)
#         self.rect = self.image.get_rect()

#         self.rect.center = x, y
