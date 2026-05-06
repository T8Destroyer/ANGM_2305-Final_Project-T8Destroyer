import pygame
from vector import Vector2
from constants import *
import numpy as np

class Pellet(object):

    def __init__(self, row, col):
        self.name = PELLET
        self.position = Vector2(col * TILEAREA, row * TILEAREA)
        self.color = white
        self.radius = int(4 * TILEAREA / 16)
        #self.col_radius = int(4 * TILEAREA / 16)
        self.points = 10
        self.visible = True

    def draw(self, screen):
        if self.visible:
            p = self.position.asIntTup()
            pygame.draw.circle(screen, self.color, p , self.radius)

class PowerPellet(Pellet):

    def __init__(self, row, col):
        Pellet.__init__(self, row, col)
        self.name = POWERPELLET
        self.radius = int(8 * TILEAREA / 16)
        self.points = 50
        self.flash_time = 0.2
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.flash_time:
            self.visible = not self.visible
            self.timer = 0

class PelletGroup(object):

    def __init__(self, pelletfile):
        self.pellet_list = []
        self.pow_pellet_list = []
        self.createPelletList(pelletfile)
        self.num_eaten = 0

    def update(self, dt):
        for pow_pellet in self.pow_pellet_list:
            pow_pellet.update(dt)

    def createPelletList(self, pelletfile):
        data = np.loadtxt(pelletfile, dtype="<U1") #self.readPelletFile(pelletfile)
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in [".", "+"]:
                    self.pellet_list.append(Pellet(row, col))
                elif data[row][col] in ["P", "p"]:
                    pp = PowerPellet(row, col)
                    self.pellet_list.append(pp)
                    self.pow_pellet_list.append(pp)

    def readPelletFile(self, textfile):
        return np.loadtxt(textfile, dtype="<U1")
    
    def isEmpty(self):
        if len(self.pellet_list) == 0:
            return True
        return False
    
    def draw(self, screen):
        for pellet in self.pellet_list:
            pellet.draw(screen)
