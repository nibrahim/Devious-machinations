import logging

import ode
import pygame
from pygame.locals import *

WINSIZE = (1024,768)

SCALE = 4.0

def g_to_w(x, y, z):
    "Converts the x,y and z coordinates from graphics to world (pygame to ODE)"
    rx = (x - WINSIZE[0]/2)/SCALE
    ry = (WINSIZE[1]/2 - y)/SCALE
    rz = 0
    return (rx, ry, rz)

    
def w_to_g(x, y, z):
    "Converts the x,y and z coordinates from world to graphics (ODE to pygame)"
    rx = SCALE*x + WINSIZE[0]/2
    ry = WINSIZE[1]/2 - SCALE*y
    rz = 0
    return (rx, ry, rz)


def near_callback(args, g0, g1):
    contacts = ode.collide(g0, g1)
    world, contactgroup = args
    for c in contacts:
        c.setBounce(1)
        c.setMu(0)
        c.setMu2(0)
        j = ode.ContactJoint(world, contactgroup, c)
        j.attach(g0.getBody(), g1.getBody())


class GameWindow(object):
    def _set_graphics_attrs(self, frame_rate):
        self.clock = pygame.time.Clock()
        self.frame_rate = frame_rate
        self.g2w = g_to_w
        self.w2g = w_to_g
        self.scale = SCALE
        self.object_group = pygame.sprite.Group()
        self.all_group = pygame.sprite.Group()
        self.main_window = pygame.Rect(0, 0, WINSIZE[0] - 250, WINSIZE[1] - 50)
        self.play_button = pygame.image.load("data/play.png")
        self.play_button.set_colorkey((0, 0, 0))
        a,b,c,d = self.play_button.get_rect()
        self.play_button_rect = pygame.Rect(0.8 * WINSIZE[0], WINSIZE[1] - 150, c, d)
        self.screen.blit(self.play_button, (0.8 * WINSIZE[0], WINSIZE[1] - 150))

        
    def _set_physics_attrs(self):
        self.world = ode.World()
        self.world.setGravity( (0, -9.81, 0) )
        self.world.setERP(0.8)
        self.world.setCFM(1E-5)
        self.iters_per_frame = 10

        self.space = ode.Space()
        # These conversions are done just to convert coordinates to
        # get physical locations of the main window
        tx = WINSIZE[0] - 250
        ty = WINSIZE[1] - 50
        tx, ty, dummy = self.g2w(tx, ty, 0)
        floor = ode.GeomPlane(self.space, (0, 1, 0), ty)
        right_wall = ode.GeomPlane(self.space, (-1, 0, 0), -tx)
        tx = 0
        tx, dummy, dummy = self.g2w(tx, 0, 0)
        left_wall = ode.GeomPlane(self.space, (1, 0, 0), tx)
        self.contactgroup = ode.JointGroup()

    def _draw_grid(self):
        "To draw a grid useful for visual feedback"
        # Verticals
        for i in range(0, WINSIZE[0] - 250, 50):
            pygame.draw.line(self.screen, (50, 150, 0), (i,0), (i,WINSIZE[1] - 50))
            pygame.draw.line(self.empty, (50, 150, 0), (i,0), (i,WINSIZE[1] - 50))
        # Horizontals
        for i in range(0, WINSIZE[1] - 50, 50):
            pygame.draw.line(self.screen, (50, 150, 0), (0,i), (WINSIZE[0] - 250, i))
            pygame.draw.line(self.empty, (50, 150, 0), (0,i), (WINSIZE[0] - 250, i))

    def _level_complete(self):
        logging.info("Completed level")
        sound = pygame.mixer.Sound("data/tada.wav")
        sound.play()
        f = pygame.font.Font("data/Dalila.ttf", 50)
        text0 = f.render("Level completed", True, (250, 250, 250))
        self.screen.blit(text0, (100, 50))
        self.update(False)
        self.all_group.empty()
        
        
    def __init__(self, frame_rate):
        "Create the window at the start"
        flags = DOUBLEBUF|FULLSCREEN
        logging.info("Resolution specified at %dx%d"%WINSIZE)
        screen = pygame.display.set_mode(WINSIZE, flags)
        screen.fill((0,25,0))
        pygame.display.set_caption("Devious Machinations")
        empty = pygame.Surface(WINSIZE).convert()
        empty.fill((0,25,0))
        pygame.mouse.set_visible(True)
        pygame.font.init()
        pygame.mixer.init()
        self.screen = screen
        self.empty = empty
        self._set_graphics_attrs(frame_rate)
        self._set_physics_attrs()

    def handle_events(self):
        "Handle all events during a frame of animation"
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and
                                      event.key == K_ESCAPE):
                logging.info("Exit requested")
                raise SystemExit

            if event.type == MOUSEBUTTONDOWN:
                if self.play_button_rect.collidepoint(pygame.mouse.get_pos()):
                    for i in self.object_group.sprites():
                        i.enable()
                else:
                    for i in self.object_group.sprites():
                        i.pick_up()
            if event.type == MOUSEBUTTONUP:
                for i in self.object_group.sprites():
                    i.drop()


    def sync_frames(self):
        "Introduces necessary delays to limit fps"
        self.clock.tick(self.frame_rate)

    def level_setup(self, level):
        "Given a level object, set it up in the game window"
        logging.info("Setting up level '%s'"%level.NAME)
        logging.debug("Initialising")
        level.init(self)

        # Print level name
        logging.debug("Displaying level name")
        f = pygame.font.Font("data/Dalila.ttf", 20)
        text0 = f.render(level.NAME, True, (250, 250, 250))
        f = pygame.font.Font("data/Dalila.ttf", 15)
        text1 = f.render('Instructions : %s'%level.INSTRUCTIONS, True, (200, 200, 200))
        
        pos_x, pos_y = WINSIZE
        pos_x *= 0.77
        pos_y -= (text0.get_height() + 15)
        self.screen.blit(text0, (pos_x, pos_y))
        self.empty.blit(text0, (pos_x, pos_y))
        self.screen.blit(text1, (5, WINSIZE[1]-20))
        self.empty.blit(text0, (5, WINSIZE[1]-20))

        # Get list of sprites and put them on the sidebar
        logging.debug("Obtaining list of tools provided by level")
        pos_x = WINSIZE[0] - 120
        pos_y = 50
        for i in level.tools:
            if i.movable:
                x,y = pos_x, pos_y
                pos_y += 50
                i.place(x, y)
                logging.debug("Positioning '%s' at (%s,%s)"%(i.name, x, y))
            self.object_group.add(i)
            self.all_group.add(i)

        self.level = level

    def update(self, check = True):
        "Updates the screen in the animation loop and advances the physics world"
        pygame.draw.lines(self.screen, (0,250,0), False, [(0,WINSIZE[1] - 50),
                                                          (WINSIZE[0] - 250, WINSIZE[1] - 50),
                                                          (WINSIZE[0] - 250, 0)],
                          5)
        self._draw_grid()
        for i in range(self.iters_per_frame):
            self.space.collide((self.world, self.contactgroup), near_callback)
            self.world.step(1.0/(self.frame_rate))
            self.contactgroup.empty()
        self.all_group.clear(self.screen, self.empty)
        self.all_group.update()
        self.all_group.draw(self.screen)
        pygame.display.flip()
        if check and self.level.success():
            self._level_complete()
            return True
