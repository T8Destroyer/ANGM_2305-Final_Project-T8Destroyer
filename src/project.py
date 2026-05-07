from vector import *
import pygame
from pygame.locals import *
from pellet import PelletGroup
import numpy as np
from modes import ModeController
from entity import Entity
from constants import *

class GameController(object):

    def __init__(self, screen, background):
        self.screen = screen
        self.background = background

    def startGame(self):
        self.maze = NodeGroup("maze1.txt")
        self.maze.setPortalPair((0, 17), (27, 17))
        self.pacman = Pacman(self.maze.getStartTempNode())
        self.ghost = Ghost(self.maze.getStartTempNode(), self.pacman)
        self.pellets = PelletGroup("maze1.txt")

    def update(self, dt):
        self.pacman.update(dt)
        self.ghost.update(dt)
        self.pellets.update(dt)
        self.checkPelletEvents()
        self.checkEvents()
        self.draw()

    def checkEvents(self):
        pass

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pellet_list)
        if pellet:
            self.pellets.num_eaten += 1
            self.pellets.pellet_list.remove(pellet)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.maze.draw(self.screen)
        self.pellets.draw(self.screen)
        self.pacman.draw(self.screen)
        self.ghost.draw(self.screen)

class Pacman(Entity):

    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = PACMAN
        self.color = yellow

    def update(self, dt):
        self.position += self.directions[self.direction] * self.speed * dt
        direction = self.getValidKey()

        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)
            if self.target is self.node:
                self.direction = STOP
            self.setPosition()
        else:
            if self.oppositeDirection(direction):
                self.reverseDirection()

    def getValidKey(self):
        key = pygame.key.get_pressed()
        if key[K_UP]:
            return UP
        if key[K_DOWN]:
            return DOWN
        if key[K_LEFT]:
            return LEFT
        if key[K_RIGHT]:
            return RIGHT
        return STOP
    
    def eatPellets(self, pelletList):
        for pellet in pelletList:
            d = self.position - pellet.position
            d_sqr = d.magnitudeSquared()
            r_sqr = (pellet.radius + self.collideRadius)**2
            if d_sqr <= r_sqr:
                return pellet
        return None

class Ghost(Entity):

    def __init__(self, node, pacman=None):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.color = red
        self.goal = Vector2()
        self.directionMethod = self.goalDirection
        self.pacman = pacman
        self.mode = ModeController(self)

    def update(self, dt):
        self.mode.update(dt)
        if self.mode.current == SCATTER:
            self.scatter()
        if self.mode.current == CHASE:
            self.chase()
        Entity.update(self, dt)

    def scatter(self):
        self.goal = Vector2()

    def chase(self):
        self.goal = self.pacman.position

class Node(object):

    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT:None, PORTAL: None}

    def draw(self, screen):
        for i in self.neighbors.keys():
            if self.neighbors[i] is not None:
                line_start = self.position.asTuple()
                line_end = self.neighbors[i].position.asTuple()
                if self.neighbors[PORTAL] is None:
                    pygame.draw.line(screen, white, line_start, line_end, 4)
                pygame.draw.circle(screen, red, self.position.asIntTup(), 12)

class NodeGroup(object):

    def __init__(self, level):
        self.nodeList = []
        self.level = level
        self.nodesLUT = {}
        self.nodeSymbols = ["+", "P", "n"]
        self.pathSymbols = [".", "-", "|", "p"]
        data = self.readMazeFile(level)
        self.createNodeTable(data)
        self.connectHorizontally(data)
        self.connectVertically(data)
        self.homekey = None

    def readMazeFile(self, textfile):
        return np.loadtxt(textfile, dtype="<U1")

    def createNodeTable(self, data, x_offset=0, y_offset=0):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    x, y = self.constructKey(col+x_offset, row+y_offset)
                    self.nodesLUT[(x, y)] = Node(x, y)

    def createHomeNodes(self, x_offset, y_offset):
        homedata = np.array([["X","X","+","X","X"],
                             ["X","X",".","X","X"],
                             ["+","X",".","X","+"],
                             [".",".","+",".","+"],
                             ["+","X","X","X","+"]])
        self.createNodeTable(homedata, x_offset, y_offset)
        self.connectHorizontally(homedata, x_offset, y_offset)
        self.connectVertically(homedata, x_offset, y_offset)
        self.homekey = self.constructKey(x_offset+2, y_offset+2)
        return self.homekey

    def constructKey(self, x, y):
        return x * TILEAREA, y * TILEAREA
    
    def connectHorizontally(self, data, x_offset=0, y_offset=0):
        for row in list (range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col + x_offset, row + y_offset)
                    else:
                        otherKey = self.constructKey(col+x_offset, row+y_offset)
                        self.nodesLUT[key].neighbors[RIGHT] = self.nodesLUT[otherKey]
                        self.nodesLUT[otherKey].neighbors[LEFT] = self.nodesLUT[key]
                        key = otherKey
                elif data[row][col] not in self.pathSymbols:
                    key = None

    def connectVertically(self, data, x_offset=0, y_offset=0):
        data_trans = data.transpose()
        for col in list(range(data_trans.shape[0])):
            key = None
            for row in list(range(data_trans.shape[1])):
                if data_trans[col][row] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col + x_offset, row + y_offset)
                    else:
                        otherKey = self.constructKey(col + x_offset, row + y_offset)
                        self.nodesLUT[key].neighbors[DOWN] = self.nodesLUT[otherKey]
                        self.nodesLUT[otherKey].neighbors[UP] = self.nodesLUT[key]
                        key = otherKey
                elif data_trans[col][row] not in self.pathSymbols:
                    key = None

    def setPortalPair(self, pair1, pair2):
        key1 = self.constructKey(*pair1)
        key2 = self.constructKey(*pair2)
        if key1 in self.nodesLUT.keys() and key2 in self.nodesLUT.keys():
            self.nodesLUT[key1].neighbors[PORTAL] = self.nodesLUT[key2]
            self.nodesLUT[key2].neighbors[PORTAL] = self.nodesLUT[key1]

    def getNodeFromPixels(self, x, y):
        if (x, y) in self.nodesLUT.keys():
            return self.nodesLUT[(x, y)]
        return None
        
    def getNodeFromTiles(self, col, row):
        x, y = self.constructKey(col, row)
        if (x, y) in self.nodesLUT.keys():
            return self.nodesLUT[(x, y)]
        return None

    def getStartTempNode(self):
        return list(self.nodesLUT.values())[0]

    def draw (self, screen):
        for node in self.nodesLUT.values():
            node.draw(screen)

def main():
    print("Hello World!")
    pygame.init()
    pygame.display.set_caption("PAC-ier MAN")
    clock = pygame.time.Clock()
    dt = 0

    font = pygame.font.SysFont("monocraft", 12)

    screen = pygame.display.set_mode(RESOLUTION)
    background = pygame.Surface(RESOLUTION)
    background.fill(black)

    game = GameController(screen, background)
    game.startGame()

    running = True
    while running:
        #event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.update(dt)

        pygame.display.flip()
        dt = clock.tick(30) / 1000.0
    pygame.quit()

if __name__ == "__main__":
    main()