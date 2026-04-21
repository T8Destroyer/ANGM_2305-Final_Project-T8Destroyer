import pygame
from pygame.locals import *
from vector import *
from constants import *

class GameController(object):

    def __init__(self, screen, background):
        self.screen = screen
        self.background = background

    def startGame(self):
        self.maze = Maze()
        self.maze.setupTestNodes()
        self.pacman = Pacman(self.maze.nodeList[0])

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
                self.direction = STOP
            self.setPosition()

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
            
    def draw(self, screen):
        p = self.position.asIntTup()
        pygame.draw.circle(screen, yellow, p, self.radius)

class Node(object):

    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT:None}

    def draw(self, screen):
        for i in self.neighbors.keys():
            if self.neighbors[i] is not None:
                line_start = self.position.asTuple()
                line_end = self.neighbors[i].position.asTuple()
                pygame.draw.line(screen, white, line_start, line_end, 4)
                pygame.draw.circle(screen, red, self.position.asIntTup(), 12)

class Maze(object):

    def __init__(self):
        self.nodeList = []

    def setupTestNodes(self):
        nd_A = Node(80, 160)
        nd_B = Node(160, 160)
        nd_C = Node(160, 80)
        nd_D = Node(240, 160)
        nd_E = Node(160, 240)
        nd_F = Node(240, 240)

        self.nodeList = (
            nd_A,
            nd_B,
            nd_C,
            nd_D,
            nd_E,
            nd_F
        )

        nd_A.neighbors[RIGHT] = nd_B
        nd_B.neighbors[LEFT] = nd_A
        nd_B.neighbors[UP] = nd_C
        nd_B.neighbors[RIGHT] = nd_D
        nd_B.neighbors[DOWN] = nd_E
        nd_C.neighbors[DOWN] = nd_B
        nd_D.neighbors[LEFT] = nd_B
        nd_D.neighbors[DOWN] = nd_F
        nd_E.neighbors[UP] = nd_B
        nd_E.neighbors[RIGHT] = nd_F
        nd_F.neighbors[LEFT] = nd_E
        nd_F.neighbors[UP] = nd_D

    def draw (self, screen):
        for node in self.nodeList:
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