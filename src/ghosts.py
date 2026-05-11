import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from modes import ModeController

class GhostGroup(object):

    def __init__(self, node, pacman):
        #self.blinky = Blinky(node, pacman)
        #self.pinky = Pinky(node, pacman)
        #self.inky = Inky(node, pacman)
        #self.clyde = Clyde(node, pacman)
        #self.hunky = Hunky(node, pacman)
        self.blinky_at = None
        #self.ghostList = [self.blinky, self.pinky, self.inky, self.clyde, self.hunky]
        self.ghostLUT = [None, None, None, None]
        self.chooseGhosts(node, pacman)

    def __iter__(self):
        return iter(self.ghostLUT)
    
    def chooseGhosts(self, node, pacman):
        print(f"\nChoose Four Ghosts:\n-Blinky\n-Pinky\n-Inky\n-Clyde\n-Hunky\n-Spunky\n-Funky\n-Alexander\n")
        running = True
        blinky_found = False
        self.blinky_at = None
        count = 0
        inky_count = []

        while running:
            ghost = input(f"Ghost #{count+1}: ").upper()
            match ghost:
                case "BLINKY":
                    self.ghostLUT[count] = Blinky(node, pacman)
                    if blinky_found == False:
                        self.blinky_at = count
                        blinky_found = True
                case "PINKY":
                    self.ghostLUT[count] = Pinky(node, pacman)
                case "INKY":
                    inky_count.append(count)
                case "CLYDE":
                    self.ghostLUT[count] = Clyde(node, pacman)
                case "HUNKY":
                    self.ghostLUT[count] = Hunky(node, pacman)
                case "SPUNKY":
                    self.ghostLUT[count] = Spunky(node, pacman)
                case "FUNKY":
                    self.ghostLUT[count] = Funky(node, pacman)
                case "ALEXANDER":
                    self.ghostLUT[count] = Alexander(node, pacman)
                case _:
                    print("Ghost not recognized. Please try again.")
                    count-=1
            count+=1
            if count >= 4:
                if len(inky_count) > 0:
                    for i in range(len(inky_count)):
                        if blinky_found:
                            self.ghostLUT[inky_count[i]] = Inky(node, pacman, self.ghostLUT[self.blinky_at])
                        else:
                            self.ghostLUT[inky_count[i]] = Inky(node, pacman, self.ghostLUT[int(inky_count[i] - 1)])
                running = False
    
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
        self.scatter_rev = True
        self.chase_rev = True

    def update(self, dt):
        self.mode.update(dt)
        if self.mode.current == SCATTER:
            self.scatter()
            if self.scatter_rev:
                self.reverseDirection()
                self.scatter_rev = False
                self.chase_rev = True
        if self.mode.current == CHASE:
            self.chase()
            if self.chase_rev:
                self.reverseDirection()
                self.chase_rev = False
                self.scatter_rev = True
        Entity.update(self, dt)

    def scatter(self):
        self.goal = Vector2(TILEAREA*NCOLS, 0)

    def startChase(self):
        self.reverseDirection()
        self.chase()

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
            self.reverseDirection()
            self.setSpeed(50)
            self.directionMethod = self.randomDirection

    def setNormal(self):
        self.setSpeed(100)
        self.directionMethod = self.goalDirection
        self.homenode.denyAccess(DOWN, self)

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
        self.follow = blinky

    def scatter(self):
        self.goal = Vector2(TILEAREA*NCOLS, TILEAREA*NROWS)

    def chase(self):
        vec1 = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEAREA * 2
        
        if self.pacman.direction == UP or self.pacman.prev_UP == True:
            d = Vector2(TILEAREA*2, 0)
            vec1 = self.goal.__sub__(d)

        vec2 = (vec1 - self.follow.position) * 2
        self.goal = self.follow.position + vec2

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

class Hunky(Ghost):
    
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = HUNKY
        self.color = gray

    def scatter(self):
        self.goal = Vector2(TILEAREA*NCOLS, 0)

    def chase(self):
        d = Vector2(0, TILEAREA*4)
        p = self.pacman.position.asIntTup()
        if p[1] <= (TILEAREA*NROWS) / 2:
            self.goal = self.pacman.position.__sub__(d)
        else:
            self.goal = self.pacman.position.__add__(d)

class Spunky(Ghost):

    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = SPUNKY
        self.color = purple

    def scatter(self):
        self.goal = Vector2()

    def chase(self):
        c = Vector2((TILEAREA*NCOLS)/2, (TILEAREA*NROWS)/2)
        vec = (self.pacman.position - c) / 2
        self.goal = vec + c

class Funky(Ghost):

    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = FUNKY
        self.color = lime

    def scatter(self):
        self.goal = Vector2(TILEAREA*NCOLS, TILEAREA*NROWS)

    def chase(self):
        d = self.pacman.position - self.position
        ds = d.magnitudeSquared()
        if ds <= (TILEAREA*8)**2:
            self.goal = (self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEAREA * 8) - d
            p = self.goal.asIntTup()
            if self.pacman.direction == UP or self.pacman.prev_UP == True:
                c = Vector2(p[0], 0)
                self.goal = self.goal.__sub__(c)
        else:
            self.goal = self.pacman.position

class Alexander(Ghost):

    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = ALEXANDER
        self.color = light_blue

    def scatter(self):
        self.goal = Vector2(0, TILEAREA*NROWS)

    def chase(self):
        d = self.pacman.position - self.position
        ds = d.magnitudeSquared()
        if ds <= (TILEAREA*8)**2:
            self.goal = self.pacman.position
        else:
            c = Vector2(0,TILEAREA*NROWS)
            vec = (self.pacman.position - c) / 2
            self.goal = vec + c