import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from modes import ModeController

class GhostGroup(object):

    def __init__(self, node, pacman):
        self.blinky = Blinky(node, pacman)
        self.pinky = Pinky(node, pacman)
        self.inky = Inky(node, pacman, self.blinky)
        self.clyde = Clyde(node, pacman)
        self.ghostLUT = [self.blinky, self.pinky, self.inky, self.clyde]

    def __iter__(self):
        return iter(self.ghostLUT)
    
    def update(self, dt):
        for ghost in self:
            ghost.update(dt)
        
    def startFright(self):
        for ghost in self:
            ghost.startFright()
        self.resetPoints()
    
    def setSpawnNode(self, node):
        for ghost in self:
            ghost.setSpawnNode(node)

    def updatePoints(self):
        for ghost in self:
            ghost.points *= 2

    def resetPoints(self):
        for ghost in self:
            ghost.points = 200

    def reset(self):
        for ghost in self:
            ghost.reset()

    def hide(self):
        for ghost in self:
            ghost.visible = False

    def show(self):
        for ghost in self:
            ghost.visible = True

    def draw(self, screen):
        for ghost in self:
            ghost.draw(screen)

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

    def reset(self):
        Entity.reset(self)
        self.points = 200
        self.directionMethod = self.goalDirection

class Blinky(Ghost):

    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = BLINKY
        self.color = red

    def scatter(self):
        self.goal = Vector2(TILEAREA*NCOLS, 0)

class Pinky(Ghost):
    
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = PINKY
        self.color = pink

    def scatter(self):
        self.goal = Vector2()

    def chase(self):
        self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEAREA * 4

        if self.pacman.direction == UP or self.pacman.prev_UP == True:
            d = Vector2(TILEAREA*4, 0)
            self.goal = self.goal.__sub__(d)

class Inky(Ghost):

    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = INKY
        self.color = cyan

    def scatter(self):
        self.goal = Vector2(TILEAREA*NCOLS, TILEAREA*NROWS)

    def chase(self):
        vec1 = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEAREA * 2
        
        if self.pacman.direction == UP or self.pacman.prev_UP == True:
            d = Vector2(TILEAREA*2, 0)
            vec1 = self.goal.__sub__(d)

        vec2 = (vec1 - self.blinky.position) * 2
        self.goal = self.blinky.position + vec2

class Clyde(Ghost):

    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
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