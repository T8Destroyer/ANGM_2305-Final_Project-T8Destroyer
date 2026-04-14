import pygame
from pygame.locals import *
from vector import *
from constants import *

class GameController(object):

    def __init__(self, screen, background):
        self.screen = screen
        self.background = background

    def startGame(self):
        self.pacman = Pacman()

    def update(self, dt):
        self.pacman.update(dt)
        self.checkEvents()
        self.draw()

    def checkEvents(self):
        pass

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.pacman.draw(self.screen)

class Pacman(object):

    def __init__(self):
        self.name = PACMAN
        self.position = Vector2(200, 400)
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

    def update(self, dt):
        self.position += self.directions[self.direction] * self.speed * dt
        direction = self.getValidKey()
        self.direction = direction

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
            
    def draw(self, screen):
        p = self.position.asIntTup()
        pygame.draw.circle(screen, yellow, p, self.radius)



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