# Created by Emanuel Ramirez on 09/08/2020

import pygame, sys
import config

GRID = []


class Square:
    def __init__(self, i, j):
        self.x, self.y = i, j

    def draw(self, window, color):
        pygame.draw.rect(window, color, (self.x*get_width(), self.y*get_heigth(), get_width()-1, get_heigth()-1))


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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_game()
            # For future implementation of placing stuf on the board
            if event.type == pygame.MOUSEBUTTONUP:
                if pygame.mouse.get_pressed(0):
                    print("Mouse pressed.")
            if event.type == pygame.KEYDOWN:
                # Start the visualizer
                if event.key == pygame.K_RETURN:
                    start_flag = True
                    print(f"Start flag is: {start_flag}")

        window.fill((0, 0, 20))
        for i in range(config.NUM_COLS):
            for j in range(config.NUM_ROWS):
                square = GRID[j][i]
                square.draw(window, config.WHITE)


        pygame.display.flip()





if __name__ == '__main__':
    main()
