#!/usr/bin/python

# Created by Emanuel Ramirez on 09/08/2020

import config
import pygame, math, random, sys, time
import tkinter as tk


# TODO: Refactor this later to make it more pythonic!!!
OPEN_SET   = [] # All the squares being cosidered to find the shortest path
CLOSED_SET = [] # All the square NOT being cosidered anymore
GRID       = []
PATH       = []

# Initial starting and ending squares
STARTING_POINT = None
END_POINT      = None

DIAGONALS = False # Will decide if the A* algorithm uses diagonal movement as valid or not.
                  # set as command line argument '-d'

FLAGS = {'start_flag': False,
         'start_point_chose_flag': False,
         'end_point_chosen_flag': False,
         'result_flag': False,
         'show_coordinates_flag': False,
         'visualization_terminated': False,
         'game_restarted_flag': False}


clock = pygame.time.Clock()


class Square:

    def __init__(self, x, y):
        ''' Initialize a single square on the grid'''
        self.x = x # x coordinate
        self.y = y # y coordinate
        self.g = 0 # Distance from current square to starting square
        self.h = 0 # Distance from current square to end square
        self.f = 0 # Score of the square: g_total + h_total
        self.color = None
        self.neighbors = []
        self.wall = False
        self.prev = None


    def draw(self, window, color):
        ''' Color each square white or black. If the square represents a wall,
            then it shall be colored BLACK. If it is a normal square; WHITE.

        @param: pygame.display, tuple: window object and RGB hex tuple
        '''
        self.color = color
        if self.wall:
            self.color = config.BLACK # Current square is a wall. Make it black!
        pygame.draw.rect(window, color, (self.x*get_width(), self.y*get_heigth(), get_width()-1, get_heigth()-1), 0)


    def add_neighbors(self, grid):
        ''' Add the respective neighbors of the current square to the neighbor list
            when creating the neighbor grid list.

        @param: list: grid itself
        '''

        # East neighbor
        if self.x < config.NUM_COLS - 1:
            self.neighbors.append(GRID[self.x+1][self.y])

        # West neighbor
        if self.x > 0:
            self.neighbors.append(GRID[self.x-1][self.y])

        # North neighbor
        if self.y < config.NUM_ROWS - 1:
            self.neighbors.append(GRID[self.x][self.y+1])

        # South neighbor
        if self.y > 0:
            self.neighbors.append(GRID[self.x][self.y-1])


        if DIAGONALS:
            # North-East neighbor
            if self.x < config.NUM_COLS - 1 and self.y < config.NUM_ROWS - 1:
                self.neighbors.append(GRID[self.x+1][self.y+1])

            # South-East neighbor
            if self.x < config.NUM_COLS - 1 and self.y > 0:
                self.neighbors.append(GRID[self.x+1][self.y-1])

            # North-West neighbor
            if self.x > 0 and self.y > config.NUM_ROWS - 1:
                self.neighbors.append(GRID[self.x-1][self.y+1])

            # South-West neighbor
            if self.x > 0 and self.y > 0:
                self.neighbors.append(GRID[self.x-1][self.y-1])



def get_width():
    ''' Returns the width of each square on the board
        With a Screen Width of 900 and 60 columns ---> square width = 15

    @return: int: width of each square
    '''
    return config.WIDTH//config.NUM_COLS


def get_heigth():
    ''' Returns the heigth of each square on the board
        With a Screen Height of 900 and 60 rows ---> square width = 15

    @return: int: heigth of each square
    '''
    return config.HEIGTH//config.NUM_ROWS


def build_neighbors_grid():
    ''' Create grid network of neighbors for each square'''
    for i in range(config.NUM_COLS):
        for j in range(config.NUM_ROWS):
            GRID[i][j].add_neighbors(GRID)


def build_initial_grid():
    ''' Build the initial board state'''
    for col in range(config.NUM_COLS):
        array = []
        for row in range(config.NUM_ROWS):
            array.append(Square(col, row))
        GRID.append(array)


def draw_wall(mouse_pos):
    ''' Add a wall flag to given specified mouse position.

    @param: tuple: registered mouse click position on the screen range of [0, WINDOW_SIZE]
    '''
    x_pos, y_pos = mouse_pos[0]//get_width(), mouse_pos[1]//get_width()
    GRID[x_pos][y_pos].wall = True


def remove_wall(mouse_pos):
    ''' Remove wall flag from the given specified mouse position.

    @param: tuple: registered mouse click position on the screen range of [0, WINDOW_SIZE]
    '''
    x_pos, y_pos = mouse_pos[0]//get_width(), mouse_pos[1]//get_width()
    GRID[x_pos][y_pos].wall = False


def get_square_pos_from_mouse(mouse_pos):
    ''' Receives current @mouse_pos and returns a scaled
        tuple of X and Y positions of the square relative to the grid
    '''
    x_pos, y_pos = math.floor(mouse_pos[0]//get_width()), math.floor(mouse_pos[1]//get_width())
    return (x_pos, y_pos)



def heuristics(a, b):
    ''' Returns an estimated the distance from current node to the end node'''
    return math.sqrt(abs(a.x-b.x)**2 + abs(a.y-b.y)**2)


def a_star_pathfinding(start_flag, start, end):
    ''' TODO: Think about a concise A* star explanation'''
    flag = False
    if len(OPEN_SET) > 0:
        winner = 0
        for i in range(len(OPEN_SET)):
            if OPEN_SET[i].f < OPEN_SET[winner].f:
                winner = i
        current = OPEN_SET[winner]

        if current == end:
            temp = current
            while temp.prev:
                PATH.append(temp.prev)
                temp = temp.prev
            if not flag:
                flag = True
                return
            elif flag:
                return

        if not flag:
            OPEN_SET.remove(current)
            CLOSED_SET.append(current)

            for neighbor in current.neighbors:
                #time.sleep(-time.time()%1)
                if neighbor in CLOSED_SET or neighbor.wall:
                    continue
                tempG = current.g + 1

                newPath =  False
                if neighbor in OPEN_SET:
                    if tempG < neighbor.g:
                        neighbor.g = tempG
                        newPath = True
                else:
                    neighbor.g = tempG
                    newPath = True
                    OPEN_SET.append(neighbor)

                if newPath:
                    neighbor.h = heuristics(neighbor, end)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.prev = current
    else:
        print("No solution was found for the current configuration.")
        return -1
    return flag


#TODO: Make it possible for resize of text and center the coordinates on the squares.
def toogle_coordinates(window):
    ''' Toogles on the coordinate system on the grid.

    @param: pygame.display: game window object
    '''
    for i in range(0, config.WINDOW_SIZE[0], get_width()):
        for j in range(0, config.WINDOW_SIZE[1], get_width()):
            if GRID[i//get_width()][j//get_width()].color == config.LIGHT_BLUE:
                text = config.FONT.render(f'{i}, {j}', True, config.YELLOW)
            else:
                text = config.FONT.render(f'{i}, {j}', True, config.LIGHT_BLUE)
            textRect = text.get_rect()
            textRect.center = (i+25, j+10)
            window.blit(text, textRect)


def toogle_square_scores(window):
    # TODO: show the F score in the upper right.
    #       show the G score in the bootom left
    #       show the H score in the bootom right
    pass


def reset_game():
    # reset the starting nodes
    STARTING_POINT = None
    END_POINT      = None

    # Empty the current sets, path, and grid lists
    OPEN_SET.clear()
    CLOSED_SET.clear()
    PATH.clear()
    GRID.clear()

    # Build a new grid and neighbor's grid state
    build_initial_grid()
    build_neighbors_grid()

    # remove all the walls and change every square to white
    for col in range(config.NUM_COLS):
        for row in range(config.NUM_ROWS):
            GRID[col][row].wall = False
            GRID[col][row].color = config.WHITE

    # reset all the flags
    for flag, value in FLAGS.items():
        FLAGS.update({flag: False})
    return


def render_current_grid(window):
    ''' In charge of rendering the grid colors on the screen every tick'''
    window.fill((0, 0, 20))
    for i in range(config.NUM_COLS):
        for j in range(config.NUM_ROWS):

            square = GRID[j][i]
            if square.color == config.LIGHT_BLUE:
                square.draw(window, config.LIGHT_BLUE)
            elif square in CLOSED_SET:
                square.draw(window, config.LIGHT_RED)
            elif square in OPEN_SET:
                square.draw(window, config.LIGHT_GREEN)
            elif square.color == config.GREEN:
                square.draw(window, config.GREEN)
            elif square.wall:
                square.draw(window, config.BLACK)
            else:
                square.draw(window, config.WHITE)


def main():
    ''' Program driver'''
    pygame.init()
    window = pygame.display.set_mode(config.WINDOW_SIZE)
    pygame.display.set_caption("A* Visualizer by Emanuel Ramirez")

    build_initial_grid()
    build_neighbors_grid()

    start_time               = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_game()

            # Mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Left click --> Add wall to square
                if pygame.mouse.get_pressed()[0]:
                    draw_wall(pygame.mouse.get_pos())

                # Right click --> Remove wall from square
                if pygame.mouse.get_pressed()[2]:
                    remove_wall(pygame.mouse.get_pos())


            # Mouse click and drag events
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]: # Left click
                    draw_wall(pygame.mouse.get_pos())

                if pygame.mouse.get_pressed()[2]: # Right click
                    remove_wall(pygame.mouse.get_pos())


            if event.type == pygame.KEYDOWN:
                # Start the visualizer
                if event.key == pygame.K_RETURN:
                    FLAGS.update({'start_flag': True})
                    start_time = pygame.time.get_ticks()

                # TODO: Eventually will be the maze generation keybinding
                if event.key == pygame.K_m:
                    pass

                # Toogle key for the coordinate system on the grid
                if event.key == pygame.K_c:
                    if not FLAGS.get('show_coordinates_flag'):
                        FLAGS.update({'show_coordinates_flag': True})
                    else:
                        FLAGS.update({'show_coordinates_flag': False})

                # L_Shift + R will reset back to the initial grid state
                if event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                    FLAGS.update({'start_flag': False})
                    reset_game()

                if event.key == pygame.K_s: # Draw starting node on the board with (s) key
                    if not FLAGS.get('start_point_chosen_flag'):
                        position = get_square_pos_from_mouse(pygame.mouse.get_pos())
                        STARTING_POINT = GRID[position[0]][position[1]]
                        OPEN_SET.append(STARTING_POINT) # Add starting node to the open set
                        STARTING_POINT.draw(window, config.GREEN)
                        FLAGS.update({'start_point_chosen_flag': True})

                if event.key == pygame.K_e: # Draw end node on the board with (e) key
                    if not FLAGS.get('end_point_chosen_flag'):
                        position = get_square_pos_from_mouse(pygame.mouse.get_pos())
                        END_POINT = GRID[position[0]][position[1]]
                        END_POINT.draw(window, config.LIGHT_BLUE)
                        FLAGS.update({'end_point_chosen_flag': True})


        # start pathfinding
        if FLAGS.get('start_flag'):
            a_star_pathfinding(True, STARTING_POINT, END_POINT)
            #result = a_star_pathfinding(True, STARTING_POINT, END_POINT)
            #if result == -1:
            #    FLAGS.update({'start_flag': False})

        # Draw the current squares colors to the window
        render_current_grid(window)


        # Highlight the final path
        for i, square in enumerate(PATH):
            if i == 0:
                FLAGS.update({'start_flag': False})
            # TODO: This is temporary
            # Way to let the prgram know that the algorithm has stopped running.
            if i == len(PATH)-1 and not FLAGS.get('visualization_terminated'):
                FLAGS.update({'visualization_terminated': True})
                print('A* Pathfinding visualization has terminated. Press Left Shift + R to reset the grid.')
            #square.draw(window, config.LIGHT_BLUE)
            GRID[square.x][square.y].color = config.LIGHT_BLUE


        # Toogle coordinates on screen
        if FLAGS.get('show_coordinates_flag'):
        #if show_coordinates_flag:
            toogle_coordinates(window)

        pygame.display.flip()
        clock.tick(config.FPS) # Limit to 60 frames per second


def close_game():
    ''' Close the game'''
    pygame.quit()
    sys.exit()



if __name__ == '__main__':
    for arg in sys.argv:
        # Diagonal flag
        if arg == '-d':
            print('\nNote: Diagonal neighbors will be considered during the A* algorithm.\n')
            DIAGONALS = True

    main()
