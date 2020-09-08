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

    start_flag               = False
    start_point_chosen_flag  = False
    end_point_chosen_flag    = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_game()
            # For future implementation of placing stuf on the board
            if event.type == pygame.MOUSEBUTTONUP:
                if pygame.mouse.get_pressed(0):
                    # Eventually use this to draw the walls.
                    # TODO: Think about using Shift+Click or just Click for the wall creation
                    print(f'Right click Mouse position: {pygame.mouse.get_pos()}')


            if event.type == pygame.KEYDOWN:
                # Start the visualizer
                if event.key == pygame.K_RETURN:
                    start_flag = True
                if event.key == pygame.K_s: # Draw starting node on the board with (s) key
                    if not start_point_chosen_flag:
                        x_pos = math.floor(pygame.mouse.get_pos()[0]//get_width())
                        y_pos = math.floor(pygame.mouse.get_pos()[1]//get_width())
                        square = GRID[x_pos][y_pos]
                        square.draw(window, config.GREEN)
                        start_point_chosen_flag = True
                if event.key == pygame.K_e: # Draw end node on the board with (e) key
                    if not end_point_chosen_flag:
                        x_pos = math.floor(pygame.mouse.get_pos()[0]//get_width())
                        y_pos = math.floor(pygame.mouse.get_pos()[1]//get_width())
                        square = GRID[x_pos][y_pos]
                        square.draw(window, config.LIGHT_BLUE)
                        end_point_chosen_flag = True


        window.fill((0, 0, 20))
        for i in range(config.NUM_COLS):
            for j in range(config.NUM_ROWS):
                square = GRID[j][i]
                if square.color == config.LIGHT_BLUE:
                    square.draw(window, config.LIGHT_BLUE)
                elif square.color == config.GREEN:
                    square.draw(window, config.GREEN)
                else:
                    square.draw(window, config.WHITE)


        pygame.display.flip()





if __name__ == '__main__':
    main()
