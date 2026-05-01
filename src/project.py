import pygame
from pygame.locals import *
from vector import *
from constants import *
import numpy as np

class GameController(object):

    def __init__(self, screen, background):
        self.screen = screen
        self.background = background

    def startGame(self):
        #self.maze = Maze()
        self.maze = Maze("maze1.txt")
        #self.pacman = Pacman(self.maze.nodeList[0])
        self.pacman = Pacman(self.maze.getStartTempNode())

    def update(self, dt):
        self.pacman.update(dt)
        self.checkEvents()
        self.draw()

    def checkEvents(self):
        pass

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.maze.draw(self.screen)
        self.pacman.draw(self.screen)

class Pacman(object):

    def __init__(self, node):
        self.name = PACMAN
        #self.position = Vector2(200, 400)
        self.directions = {
            STOP:Vector2(),
            UP:Vector2(0, -1),
            DOWN:Vector2(0, 1),
            LEFT:Vector2(-1, 0),
            RIGHT:Vector2(1, 0)
        }
        self.direction = STOP
        self.speed = 100 #* TILEAREA/25
        self.radius = 10
        self.color = yellow
        self.node = node
        self.setPosition()
        self.target = node

    def setPosition(self):
        self.position = self.node.position.copy()

    def update(self, dt):
        self.position += self.directions[self.direction] * self.speed * dt
        direction = self.getValidKey()

        if self.overshotTarget():
            self.node = self.target
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                #self.direction = STOP
            #self.setPosition()
                self.target = self.getNewTarget(self.direction)
            if self.target is self.node:
                self.direction = STOP
            self.setPosition()
        else:
            if self.oppositeDirection(direction):
                self.reverseDirection()

    def validDirection(self,direction):
        if direction is not STOP:
            if self.node.neighbors[direction] is not None:
                return True
        return False
    
    def getNewTarget(self, direction):
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        return self.node

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
    
    def overshotTarget(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitude()
            node2Self = vec2.magnitude()
            return node2Self >= node2Target
        return False
    
    def reverseDirection(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    def oppositeDirection(self, direction):
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False
            
    def draw(self, screen):
        p = self.position.asIntTup()
        pygame.draw.circle(screen, yellow, p, self.radius)

class Node(object):

    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT:None, PORTAL: None}

    def draw(self, screen):
        for i in self.neighbors.keys():
            if self.neighbors[i] is not None:
                line_start = self.position.asTuple()
                line_end = self.neighbors[i].position.asTuple()
                pygame.draw.line(screen, white, line_start, line_end, 4)
                pygame.draw.circle(screen, red, self.position.asIntTup(), 12)

class Maze(object):

    def __init__(self, level):
        self.nodeList = []
        self.level = level
        self.nodesLUT = {}
        self.nodeSymbols = ["+"]
        self.pathSymbols = ["."]
        data = self.readMazeFile(level)
        self.createNodeTable(data)
        self.connectHorizontally(data)
        self.connectVertically(data)

    def readMazeFile(self, textfile):
        return np.loadtxt(textfile, dtype="<U1")

    def createNodeTable(self, data, x_offset=0, y_offset=0):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    x, y = self.constructKey(col+x_offset, row+y_offset)
                    self.nodesLUT[(x, y)] = Node(x, y)

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