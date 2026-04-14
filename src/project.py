import pygame
from pygame.locals import *
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