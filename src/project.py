import pygame
from pygame.locals import *
from vector import *
from constants import *

class GameController(object):

    def __init__(self):
        pass

    def startGame(self):
        pass

    def update(self):
        self.checkEvents()
        self.render()

    def checkEvents(self):
        pass

    def render(self):
        pass

class Pacman(object):

    def __init__(self):
        self.name = PACMAN
        self.position = Vector2(200, 400)
        self.directions = {
            STOP:Vector2(),
            UP: Vector2(0, -1),
            DOWN:Vector2(0, 1),
            LEFT:Vector2(-1, 0),
            RIGHT:Vector2(1, 0)
        }
        self.direction = STOP
        self.speed = 100 #tutorial does 100 * TILEAREA/25 for some reason
        self.radius = 10
        self.color = yellow

    def update(self, dt):
        self.position += self.directions[self.direction] * self.speed * dt
        direction = self.getValidKey()
        self.direction = direction

def main():
    print("Hello World!")
    pygame.init()
    pygame.display.set_caption("PAC-ier MAN")
    clock = pygame.time.Clock()
    dt = 0

    screen = pygame.display.set_mode(SCREENSIZE)
    background = pygame.Surface(SCREENSIZE)
    background.fill(black)

    game = GameController()
    game.startGame()

    running = True
    while running:
        #event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        dt = clock.tick(30) / 1000.0

if __name__ == "__main__":
    main()