import pygame
#Screen Variables
TILEAREA = 25
NROWS = 36
NCOLS = 28
SCREENWIDTH = NCOLS*TILEAREA
SCREENHEIGHT = NROWS*TILEAREA
RESOLUTION = (SCREENWIDTH, SCREENHEIGHT)
#Color variables
black = pygame.Color(0, 0, 0)
yellow = pygame.Color(255, 255, 0)
blue = pygame.Color(0, 0, 155)
red = pygame.Color(255, 0, 0)
pink = pygame.Color(247, 177, 247)
cyan = pygame.Color(0, 247, 216)
orange = pygame.Color(247, 155, 1)
white = pygame.Color(255, 255, 255)
green = pygame.Color(0, 255, 0)
purple = pygame.Color(255, 0, 255)
gray = pygame.Color(100, 100, 100)
lime = pygame.Color(100, 255, 100)
#Movement Variables
STOP = 0
UP = 1
DOWN = -1
LEFT = 2
RIGHT = -2
PORTAL = 3
#Character/Object Variables
PACMAN = 0
PELLET = 1
POWERPELLET = 2
GHOST = 3
BLINKY = 4
PINKY = 5
INKY = 6
CLYDE = 7
FRUIT = 8
HUNKY = 9
SPUNKY = 10
FUNKY = 11
#Ghost states
SCATTER = 0
CHASE = 1
FRIGHT = 2
EATEN = 3

#Note: for making mazes through text files:
#   + = node with pellet
#   P = node with powerpellet
#   n = node without pellet
#   . = path with pellet
#   p = path with powerpellet
#   -, | = path without pellet 
#   X = empty
#Build the maze in a txt file with a space between each character horizonatally, then fill any unused spaces with X

