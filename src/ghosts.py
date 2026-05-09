import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from modes import ModeController



class Ghost(Entity):

    def __init__(self, node, pacman=None, blinky=None):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.color = red
        self.goal = Vector2()
        self.directionMethod = self.goalDirection
        self.pacman = pacman
        self.mode = ModeController(self)
        self.blinky = blinky
        self.homenode= node

    def update(self, dt):
        self.mode.update(dt)
        if self.mode.current == SCATTER:
            self.scatter()
        if self.mode.current == CHASE:
            self.chase()
        Entity.update(self, dt)

    def scatter(self):
        self.goal = Vector2(TILEAREA*NCOLS, 0)

    def chase(self):
        self.goal = self.pacman.position

    def eaten(self):
        self.goal = self.spawnNode.position

    def startEaten(self):
        self.mode.setEatenMode()
        if self.mode.current == EATEN:
            self.setSpeed(150)
            self.directionMethod = self.goalDirection
            self.eaten()

    def setSpawnNode(self, node):
        self.spawnNode = node

    def startFright(self):
        self.mode.setFrightMode()
        if self.mode.current == FRIGHT:
            self.setSpeed(50)
            self.directionMethod = self.randomDirection

    def setNormal(self):
        self.setSpeed(100)
        self.directionMethod = self.goalDirection

class Blinky(Ghost):

    def __init__(self, node, pacman=None, blinky=None):
        Ghost().__init__(node, pacman, blinky)
        self.name = BLINKY
        self.color = red

    def scatter(self):
        self.goal = Vector2(TILEAREA*NCOLS, 0)

class Pinky(Ghost):
    
    def __init__(self, node, pacman=None, blinky=None):
        Ghost().__init__(node, pacman, blinky)
        self.name = PINKY
        self.color = pink

    def scatter(self):
        self.goal = Vector2()

    def chase(self):
        self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEAREA * 4
        if self.pacman.direction == UP or self.pacman.isPrevMoveUP() == True:
            self.goal = Vector2.__sub__(TILEAREA*4, 0)

class Inky(Ghost):

    def __init__(self, node, pacman=None, blinky=None):
        Ghost().__init__(node, pacman, blinky)
        self.name = INKY
        self.color = cyan

    def scatter(self):
        self.goal = Vector2(TILEAREA*NCOLS, TILEAREA*NROWS)

    def chase(self):
        vec1 = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEAREA * 2
        vec2 = (vec1 - self.blinky.position) * 2
        self.goal = self.blinky.position + vec2

class Clyde(Ghost):

    def __init__(self, node, pacman=None, blinky=None):
        Ghost().__init__(node, pacman, blinky)
        self.name = CLYDE
        self.color = orange

    def scatter(self):
        self.goal = Vector2(0, TILEAREA*NROWS)

    def chase(self):
        d = self.pacman.position - self.position
        ds = d.magnitudeSquared()
        if ds <= (TILEAREA*8)**2:
            self.scatter()
        else:
            self.goal = self.pacman.position