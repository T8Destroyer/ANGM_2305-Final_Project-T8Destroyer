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
red = pygame.Color(255, 0, 0)
pink = pygame.Color(247, 177, 247)
cyan = pygame.Color(0, 247, 216)
orange = pygame.Color(247, 155, 1)
white = pygame.Color(255, 255, 255)
#Movement Variables
STOP = 0
UP = 1
DOWN = -1
LEFT = 2
RIGHT = -2
PORTAL = 3
#Character Variables
PACMAN = 0

#Note: for making mazes through text files:
#   + = node
#   . = path
#   X = empty
#Build the maze in a txt file with a space between each character horizonatally, then fill any unused spaces with X

