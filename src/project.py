from vector import *
import pygame
from pygame.locals import *
from pellet import PelletGroup
import numpy as np
from modes import ModeController
from ghosts import GhostGroup
from entity import Entity
from constants import *

class GameController(object):

    def __init__(self, screen, background):
        self.screen = screen
        self.background = background
        self.fruit = None
        self.pause = Pause(True)
        self.level = 0

    def startGame(self):
        self.maze = NodeGroup("maze1.txt")
        self.maze.setPortalPair((0, 17), (27, 17))
        homekey = self.maze.createHomeNodes(11.5, 14)
        self.maze.connectHomeNodes(homekey, (12,14), LEFT)
        self.maze.connectHomeNodes(homekey, (15,14), RIGHT)
        self.pacman = Pacman(self.maze.getNodeFromTiles(15, 26))
        self.pellets = PelletGroup("maze1.txt")
        self.ghosts = GhostGroup(self.maze.getStartTempNode(), self.pacman)
        self.ghosts.blinky.setStartNode(self.maze.getNodeFromTiles(2+11.5,0+14))
        self.ghosts.pinky.setStartNode(self.maze.getNodeFromTiles(2+11.5,3+14))
        self.ghosts.inky.setStartNode(self.maze.getNodeFromTiles(0+11.5,3+14))
        self.ghosts.clyde.setStartNode(self.maze.getNodeFromTiles(4+11.5,3+14))
        self.ghosts.setSpawnNode(self.maze.getNodeFromTiles(2+11.5, 3+14))

    def update(self, dt):
        self.pellets.update(dt)
        if self.pause.paused == False:
            self.pacman.update(dt)
            self.ghosts.update(dt)
            if self.fruit != None:
                self.fruit.update(dt)
            self.checkPelletEvents()
            self.checkGhostEvents()
            self.checkFruitEvents()
        afterPause = self.pause.update(dt)
        if afterPause != None:
            afterPause()

        self.checkEvents()
        self.draw()

    def nextLevel(self):
        self.level += 1
        self.pause.paused = True
        self.startGame()

    def checkEvents(self):
        pass

    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost) == True and ghost.mode.current == FRIGHT:
                self.pacman.visible = False
                ghost.visible = False
                self.pause.setPause(pause_time=1, func=self.showEntities)
                ghost.startEaten()

    def checkFruitEvents(self):
        if self.pellets.num_eaten == 50 or self.pellets.num_eaten == 140:
            if self.fruit == None:
                self.fruit = Fruit(self.maze.getNodeFromTiles(9,20))
            if self.fruit != None:
                if self.pacman.collideCheck(self.fruit):
                    self.fruit = None
                elif self.fruit.destroy:
                    self.fruit = None

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pellet_list)
        if pellet:
            self.pellets.num_eaten += 1
            self.pellets.pellet_list.remove(pellet)
            if pellet.name == POWERPELLET:
                self.ghosts.startFright()

    def showEntities(self):
        self.pacman.visible = True
        self.ghosts.show()

    def hideEntities(self):
        self.pacman.visible = False
        self.ghosts.hide()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.maze.draw(self.screen)
        self.pellets.draw(self.screen)
        if self.fruit != None:
            self.fruit.draw(self.screen)
        self.pacman.draw(self.screen)
        self.ghosts.draw(self.screen)

class Pacman(Entity):

    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = PACMAN
        self.color = yellow
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.curr_key = self.direction
        self.prev_key = self.curr_key
        self.prev_UP = False

    def update(self, dt):
        self.position += self.directions[self.direction] * self.speed * dt
        direction = self.getValidKey()

        self.prevKey()


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
    
    def prevKey(self):
        if self.curr_key != self.direction:
            self.prev_key = self.curr_key
            self.curr_key = self.direction
        if self.prev_key == UP and self.curr_key == STOP:
            self.prev_UP = True
        else:
            self.prev_UP = False
    
    def eatPellets(self, pelletList):
        for pellet in pelletList:
            if self.collideCheck(pellet):
                return pellet
        return None
    
    def collideGhost(self, ghost):
        return self.collideCheck(ghost)
    
    def collideCheck(self, other):
        d = self.position - other.position
        d_sqr = d.magnitudeSquared()
        r_sqr = (self.collideRadius + self.collideRadius)**2
        if d_sqr <= r_sqr:
            return True
        return False

class Fruit(Entity):

    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = FRUIT
        self.color = green
        self.lifespan = 5
        self.timer = 0
        self.destroy = False
        self.points = 100
        self.setBetweenNodes(RIGHT)

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destroy = True

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
                pygame.draw.circle(screen, blue, self.position.asIntTup(), 12)

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
                             ["+",".","+",".","+"],
                             ["+","X","X","X","+"]])
        self.createNodeTable(homedata, x_offset, y_offset)
        self.connectHorizontally(homedata, x_offset, y_offset)
        self.connectVertically(homedata, x_offset, y_offset)
        self.homekey = self.constructKey(x_offset+2, y_offset)
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

    def connectHomeNodes(self, homekey, otherkey, direction):
        key = self.constructKey(*otherkey)
        self.nodesLUT[homekey].neighbors[direction] = self.nodesLUT[key]
        self.nodesLUT[key].neighbors[direction*-1] = self.nodesLUT[homekey]

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
            print("Node found from Tiles")
            return self.nodesLUT[(x, y)]
        return None

    def getStartTempNode(self):
        return list(self.nodesLUT.values())[0]

    def draw (self, screen):
        for node in self.nodesLUT.values():
            node.draw(screen)

class Pause(object):

    def __init__(self, paused=False):
        self.paused = paused
        self.timer = 0
        self.pause_time = None
        self.func = None

    def update (self, dt):
        if self.pause_time != None:
            self.timer += dt
            if self.timer >= self.pause_time:
                self.timer = 0
                self.paused = False
                self.pause_time = None
                return self.func
        return None
    
    def setPause(self, playerPaused=False, pause_time=None, func=None):
        self.timer = 0
        self.func = func
        self.pause_time = pause_time
        self.flip()

    def flip(self):
        self.paused = not self.paused
        

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
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    game.pause.setPause(playerPaused=True)
                    if not game.pause.paused:
                        game.showEntities()
                    else:
                        game.hideEntities()
                    
        game.update(dt)

        pygame.display.flip()
        dt = clock.tick(30) / 1000.0
    pygame.quit()

if __name__ == "__main__":
    main()