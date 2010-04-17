import math
import logging

import pygame
import ode

# States the tools can be in
RESERVE        = "RESERVE"        # In the sidebar
PICKED_UP      = "PICKED_UP"      # Being moved around
IN_MAIN_SCREEN = "IN_MAIN_SCREEN" # Placed on the screen
IN_SIMULATION  = "IN_SIMULATION"  # Participating in simulation


class DeviousSprites(pygame.sprite.Sprite):
    "Base class for all sprites in the game. The pickup/drop etc. logic is common to all objects"
    def __init__(self):
        print "We're running here!"
        # Disable the bodies
        self.state = RESERVE
        self._physics_enable(False)
        super(DeviousSprites,self).__init__()

    def enable(self):
        if self.state == IN_MAIN_SCREEN:
            self._physics_enable(True)
            self.state = IN_SIMULATION

    def _physics_enable(self, status):
        "Used to turn the physics simulation for this object on or off"
        if status:
            for i in self.entities:
                i.enable()
        else:
            for i in self.entities:
                i.disable()

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
                self.place(*pygame.mouse.get_pos())
            else:
                self.state = RESERVE

    def place(x,y):
        raise NotImplementedError()

class Ball(DeviousSprites):
    def __init__(self, world, space, main_window, x, y, density, colour, g_to_w, w_to_g, scale ):
        self.image = pygame.Surface((40, 40)).convert()
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, colour, (20, 20), 20, 0)
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.g2w = g_to_w
        self.w2g = w_to_g
        self.scale = scale
        self.main_window = main_window
        
        # Body parameters for dynamics
        self.body = ode.Body(world)
        m = ode.Mass()
        m.setSphere(density, 20/self.scale) 
        self.body.setMass(m)
        self.body.setPosition(self.g2w(x, y ,0))
        # self.body.setLinearVel((-15,0,0))

        # Geom parameters for collision detection.
        self.geom = ode.GeomSphere(space, 5)
        self.geom.setBody(self.body)

        # Keep lists of physical objects to enable/disable
        self.entities = [self.body, self.geom]

        super(Ball,self).__init__()


    def update(self):
        if self.state == PICKED_UP:
            self.rect.center = pygame.mouse.get_pos()
        else:
            if self.state == IN_SIMULATION:
                x, y, z = self.w2g(*self.body.getPosition())
                self.rect.center = x, y

    def place(self, x, y):
        "Method used to place the object at a given location - graphical coordinates"
        self.rect.center = x, y
        self.body.setPosition(self.g2w(x, y, 0))

class Lever(DeviousSprites):
    def __init__(self, world, space, main_window, x, y, g_to_w, w_to_g, scale):
        self.image = pygame.Surface((200, 20)).convert_alpha()
        self.image.fill((0, 200, 200))
        self.original = self.image
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.g2w = g_to_w
        self.w2g = w_to_g
        self.scale = scale
        self.main_window = main_window

        # Body parameters for dynamics
        self.body = ode.Body(world)
        m = ode.Mass()
        m.setBox(50, 200/self.scale, 20/self.scale, 40/self.scale) 
        self.body.setMass(m)
        self.body.setPosition(self.g2w(x, y ,0))
        
        # Geom parameters for collision detection.
        self.geom = ode.GeomBox(space, (200/self.scale, 20/self.scale, 40/self.scale))
        self.geom.setBody(self.body)
        
        # Create the fulcrum
        self.joint = ode.BallJoint(world)
        self.joint.attach(self.body, ode.environment)
        self.joint.setAnchor(self.body.getPosition())

        # Keep lists of physical objects to enable/disable
        self.entities = [self.body, self.geom]
        super(Lever, self).__init__()
        

    def update(self):
        if self.state == PICKED_UP:
            self.rect.center = pygame.mouse.get_pos()
        else:
            if self.state == IN_SIMULATION:
                x, y, z = self.w2g(*self.body.getPosition())
                qw, qx, qy, qz = self.body.getQuaternion()
                rotation = ((math.asin(2*qx*qy + 2*qz*qw) * 180)/math.pi)
                self.image = pygame.transform.rotate(self.original, rotation)
                self.rect = self.image.get_rect()
                self.rect.center = x, y

    def place(self, x, y):
        "Method used to place the object at a given location - graphical coordinates"
        self.rect.center = x, y
        self.body.setPosition(self.g2w(x, y, 0))
        self.joint.setAnchor(self.body.getPosition())
