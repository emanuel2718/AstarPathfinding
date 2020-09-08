# Created by Emanuel Ramirez on 09/08/2020

import pygame, math, sys
import config

GRID = []


class Square:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.color = None

    def draw(self, window, color):
        self.color = color
        pygame.draw.rect(window, color, (self.x*get_width(), self.y*get_heigth(), get_width()-1, get_heigth()-1), 0)


# With a Screen Width of 900 and 60 columns ---> square width = 15
def get_width():
    ''' Returns the width of each square on the board

    @return: int: width of each square
    '''
    return config.WIDTH//config.NUM_COLS

def get_heigth():
    ''' Returns the heigth of each square on the board

    @return: int: heigth of each square
    '''
    return config.HEIGTH//config.NUM_ROWS

def close_game():
    ''' Close the game'''
    pygame.quit()
    sys.exit()

def build_initial_board():
    for i in range(config.NUM_COLS):
        array = []
        for j in range(config.NUM_ROWS):
            array.append(Square(i, j))
        GRID.append(array)


def main():
    pygame.init()
    window = pygame.display.set_mode(config.WINDOW_SIZE)

    build_initial_board()

    start_flag = False
    end_point_chosen_flag = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_game()
            # For future implementation of placing stuf on the board
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # Right click
                    print(f'Right click Mouse position: {pygame.mouse.get_pos()}')

                if not(end_point_chosen_flag) and event.button == 3: # Left click
                    square = GRID[math.floor(pygame.mouse.get_pos()[0]//15)][math.floor(pygame.mouse.get_pos()[1]//15)]
                    square.draw(window, config.LIGHT_BLUE) # Draw the endpoint on the board
                    end_point_chosen_flag = True # End point established
                    #print(f'Mouse 0 --> {math.floor(pygame.mouse.get_pos()[0]//15)}')

            if event.type == pygame.KEYDOWN:
                # Start the visualizer
                if event.key == pygame.K_RETURN:
                    start_flag = True

        window.fill((0, 0, 20))
        for i in range(config.NUM_COLS):
            for j in range(config.NUM_ROWS):
                square = GRID[j][i]
                if square.color == config.LIGHT_BLUE:
                    square.draw(window, config.LIGHT_BLUE)
                else:
                    square.draw(window, config.WHITE)


        pygame.display.flip()





if __name__ == '__main__':
    main()
