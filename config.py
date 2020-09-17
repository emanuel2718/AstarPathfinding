# Created by Emanuel Ramirez on 09/08/2020

import pygame
#from pygame import image

''' Contains all the technical configurations of the game'''

# Size of the pygame window
WINDOW_SIZE = (900, 900) # (Width, Heigth)

# Width and heigth of the pygame window
WIDTH = WINDOW_SIZE[0]
HEIGTH = WINDOW_SIZE[1]

NUM_COLS, NUM_ROWS = 15, 15

# Settings panel position on the grid
PANEL_WIDTH = WIDTH
PANEL_HEIGTH = HEIGTH//2
PANEL_X_POS = 0
PANEL_Y_POS = HEIGTH - (HEIGTH//NUM_COLS)*3 # 3 squares from the bottom up
PANEL_COLOR = (130,146,154,200)


FPS = 60


# RGB values
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LIGHT_RED = (246, 156, 90)
GREEN = (24, 126, 51)
LIGHT_GREEN = (83, 212, 160)
DARK_GREEN = (43, 133, 16)
BLUE = (5, 102, 116)
LIGHT_BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)



# Pygame font initialization
pygame.font.init()
FONT = pygame.font.Font(pygame.font.get_default_font(), 10)
KEYBINDS_FONT = pygame.font.Font(pygame.font.get_default_font(), 40)
KEYBINDS_TITLE_FONT = pygame.font.Font(pygame.font.get_default_font(), 52)
COUNT_FONT = pygame.font.Font(pygame.font.get_default_font(), 18)
MODE_FONT = pygame.font.Font(pygame.font.get_default_font(), 36)
FSCORE_FONT = pygame.font.Font(pygame.font.get_default_font(), 14) # used for the f score. Must be bigger than @SCORES_FONT
SCORES_FONT = pygame.font.Font('fonts/arial.ttf', 10)


# Images
keybinds_image = pygame.image.load('images/keybinds.png')
