#!/usr/bin/python

# Created by Emanuel Ramirez on 09/08/2020

import config
import pygame, math, random, sys, time
import tkinter as tk
from tkinter import messagebox


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


FLAGS = {'start_flag'               : False,
         'start_point_chose_flag'   : False,
         'end_point_chosen_flag'    : False,
         'result_flag'              : False,
         'show_coordinates_flag'    : False,
         'show_scores_flag'         : False,
         'settings_panel_visible'   : False,
         'visualization_terminated' : False,
         'invert_grid_colors_flag'  : False,
         'game_restarted_flag'      : False}

MODES = {'creator_mode'             : True,
         'running'                  : False,
         'done'                     : False,
         'no_solution'              : False}


COLORS = {'empty_color'             : config.WHITE,
          'wall_color'              : config.BLACK,
          'start_color'             : config.GREEN,
          'end_color'               : config.BLUE,
          'openset_color'           : config.LIGHT_GREEN,
          'closedset_color'         : config.LIGHT_RED,
          'path_color'              : config.LIGHT_BLUE,
          'scores_color'            : config.DARK_GREEN,
          'coord_path_color'        : config.YELLOW,
          'coord_normal_color'      : config.LIGHT_BLUE}



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
        # If is a grid square invert the colors
        if FLAGS.get('invert_grid_colors_flag') and color == COLORS.get('empty_color'):
            pygame.draw.rect(window, color, (self.x*get_width(), self.y*get_heigth(), get_width()-1, get_heigth()-1), 1)
        # Invert the colors of the walls from black to white
        elif FLAGS.get('invert_grid_colors_flag') and color == COLORS.get('wall_color'):
            pygame.draw.rect(window, config.WHITE, (self.x*get_width(), self.y*get_heigth(), get_width()-1, get_heigth()-1), 0)

        else:
            self.color = color
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
    flagged = False
    if len(OPEN_SET) > 0:
        best_candidate_index = 0
        for i in range(len(OPEN_SET)):
            if OPEN_SET[i].f < OPEN_SET[best_candidate_index].f:
                best_candidate_index = i
        current = OPEN_SET[best_candidate_index]

        if current == end:
            temp = current
            while temp.prev:
                PATH.append(temp.prev)
                temp = temp.prev
            if not flagged:
                flagged = True
                return
            elif flagged:
                return

        if not flagged:
            OPEN_SET.remove(current)
            CLOSED_SET.append(current)

            for neighbor in current.neighbors:
                #time.sleep(-time.time()%1)
                if neighbor in CLOSED_SET or neighbor.wall:
                    continue
                temp_g_score = current.g + 1

                new_path =  False
                if neighbor in OPEN_SET:
                    if temp_g_score < neighbor.g:
                        neighbor.g = temp_g_score
                        new_path = True
                else:
                    neighbor.g = temp_g_score
                    new_path = True
                    OPEN_SET.append(neighbor)

                if new_path:
                    neighbor.h = heuristics(neighbor, end)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.prev = current
    else:
        MODES.update({'running': False})
        MODES.update({'no_solution': True})
        print("No solution was found for the current configuration.")
        return -1
    return flagged


#TODO: Make it possible for resize of text and center the coordinates on the squares.
def toogle_coordinates(window):
    ''' Toogles on the coordinate system on the grid.

    @param: pygame.display: game window object
    '''
    for i in range(0, config.WINDOW_SIZE[0], get_width()):
        for j in range(0, config.WINDOW_SIZE[1], get_width()):
            #x_pos, y_pos = i//get_width(), j//get_heigth()
            square = GRID[i//get_width()][j//get_heigth()]
            if square.color == COLORS.get('path_color') or square.color == COLORS.get('end_color'):
                text = config.FONT.render(f'{i}, {j}', True, COLORS.get('coord_path_color'))
            else:
                text = config.FONT.render(f'{i}, {j}', True, COLORS.get('coord_normal_color'))
            textRect = text.get_rect()
            textRect.center = (i+25, j+10)
            window.blit(text, textRect)


def toogle_square_scores(window):
    ''' Toogles the each square A* score if the square is either in the
        Open set, close set or in the path list.

        1. On the bottom left is showcased the "g" score which represents the movement
           cost or distance from the current square to the starting square.

        2. On the bottom right is showcased the "h" score which represents the movement
           cost or distance from the current square to the endsquare.

        3. On the top right is showcased the "f" score of the square
           which represents the total score of the square (h + g = f)

    @param: pygame object: the game window
    '''
    for i in range(0, config.WINDOW_SIZE[0], get_width()):
        for j in range(0, config.WINDOW_SIZE[1], get_width()):
            x_pos = math.floor(i//get_width())
            y_pos = math.floor(j//get_heigth())
            square = GRID[x_pos][y_pos]

            if square in OPEN_SET or square in CLOSED_SET or square in PATH:
                # F score in the top left
                f_score = config.FSCORE_FONT.render(f'{int(square.f)}', True, config.BLACK)
                f_score_rect = f_score.get_rect()
                f_score_rect.center = (i+10, j+8)

                # G score in the bottom left
                g_score = config.SCORES_FONT.render(f'{int(square.g)}', True, config.BLACK)
                g_score_rect = f_score.get_rect()
                g_score_rect.center = (i+10, j+55)

                # H score in the bottom right
                h_score = config.SCORES_FONT.render(f'{int(square.h)}', True, config.BLACK)
                h_score_rect = f_score.get_rect()
                h_score_rect.center = (i+55, j+55)

                # render the scores
                window.blit(f_score, f_score_rect)
                window.blit(g_score, g_score_rect)
                window.blit(h_score, h_score_rect)



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
            GRID[col][row].color = COLORS.get('empty_color')

    # reset all the flags
    for flag, value in FLAGS.items():
        FLAGS.update({flag: False})

    # Update the modes
    MODES.update({'running': False})
    MODES.update({'done': False})
    MODES.update({'no_solution': False})
    MODES.update({'creator_mode': True})
    return


def render_current_grid(window):
    ''' In charge of rendering the grid colors on the screen every tick'''
    window.fill((0, 0, 20))
    for i in range(config.NUM_COLS):
        for j in range(config.NUM_ROWS):

            square = GRID[j][i]
            if square.color == COLORS.get('path_color'):               # PATH
                square.draw(window, COLORS.get('path_color'))

            elif square.color == COLORS.get('start_color'):            # START_POSITION
                square.draw(window, COLORS.get('start_color'))

            elif square.color == COLORS.get('end_color'):              # END_POSITION
                square.draw(window, COLORS.get('end_color'))

            elif square in CLOSED_SET:                                 # CLOSED_SET
                square.draw(window, COLORS.get('closedset_color'))

            elif square in OPEN_SET:                                   # OPEN_SET
                square.draw(window, COLORS.get('openset_color'))

            elif square.wall:                                          # WALL
                square.draw(window, COLORS.get('wall_color'))

            else:                                                      # EMPTY SQUARE
                square.draw(window, COLORS.get('empty_color'))


def draw_settings_panel(window):
    # Draw the empty panel
    settings_panel = pygame.Surface((config.PANEL_WIDTH, config.PANEL_HEIGTH), pygame.SRCALPHA)   # per-pixel alpha
    settings_panel.fill(config.PANEL_COLOR)
    window.blit(settings_panel, (config.PANEL_X_POS, config.PANEL_Y_POS))

    render_current_mode(window)
    render_counters(window)

def render_counters(window):
    ''' Renders the counter of the amount of squares in each A* list
        1. Open Set counter
        2. Closed Set counter
        3. Path Set counter
    '''
    # Open Set render settings
    open_count_text = config.COUNT_FONT.render(f'Open: {len(OPEN_SET)}', True, config.BLACK)
    open_count_text_rect =  open_count_text.get_rect()
    open_count_text_rect.center = (config.WIDTH - 150, config.PANEL_Y_POS + 40)

    # Closed Set render settings
    close_count_text = config.COUNT_FONT.render(f'Close: {len(CLOSED_SET)}', True, config.BLACK)
    close_count_text_rect =  open_count_text.get_rect()
    close_count_text_rect.center = (config.WIDTH - 150, config.PANEL_Y_POS + 100)

    # Path Set render settings
    path_count_text = config.COUNT_FONT.render(f'Path: {len(PATH)}', True, config.BLACK)
    path_count_text_rect =  open_count_text.get_rect()
    path_count_text_rect.center = (config.WIDTH - 150, config.PANEL_Y_POS + 160)

    # Render counters on the settings panel
    window.blit(open_count_text, open_count_text_rect)
    window.blit(close_count_text, close_count_text_rect)
    window.blit(path_count_text, path_count_text_rect)


def render_current_mode(window):
    ''' Renders the current mode into the settings panel.
        Possible modes:
            - Creator mode
            - Running mode
            - Done
            - No solution
    '''
    if MODES.get('creator_mode'):
        mode_text = config.MODE_FONT.render(f'Mode: Creator', True, config.BLACK)
    elif MODES.get('running'):
        mode_text = config.MODE_FONT.render(f'Mode: Running', True, config.BLACK)
    elif MODES.get('done'):
        mode_text = config.MODE_FONT.render(f'Mode: Done', True, config.BLACK)
    elif MODES.get('no_solution'):
        mode_text = config.MODE_FONT.render(f'Mode: No solution', True, config.BLACK)

    # Render the mode
    mode_text_rect =  mode_text.get_rect()
    mode_text_rect.center = (config.PANEL_X_POS + 150, config.PANEL_Y_POS + 40)
    window.blit(mode_text, mode_text_rect)

def invert_colors(window):
    print('Invert colors')
    pass



def main():
    ''' Program driver'''
    pygame.init()
    window = pygame.display.set_mode(config.WINDOW_SIZE)
    pygame.display.set_caption("A* Pathfinding Visualizer")

    build_initial_grid()
    build_neighbors_grid()

    start_time = None

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

                # Toogle key (n) for A* pathfinding scores
                if event.key == pygame.K_n:
                    if not FLAGS.get('show_scores_flag'):
                        if FLAGS.get('show_coordinates_flag'):
                            FLAGS.update({'show_coordinates_flag': False}) # Turn off the coordinates
                        FLAGS.update({'show_scores_flag': True})
                    else:
                        FLAGS.update({'show_scores_flag': False})

                # Toogle key for the coordinate system on the grid
                if event.key == pygame.K_c:
                    if not FLAGS.get('show_coordinates_flag'):
                        if FLAGS.get('show_scores_flag'):
                            FLAGS.update({'show_scores_flag': False})     # Turn off the scores
                        FLAGS.update({'show_coordinates_flag': True})
                    else:
                        FLAGS.update({'show_coordinates_flag': False})

                # Toogle key (L_Shift + R) will reset back to the initial grid state
                if event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                    FLAGS.update({'start_flag': False})
                    reset_game()

                # Toogle key (s) add starting node to the grid on mouse click position
                if event.key == pygame.K_s:
                    if not FLAGS.get('start_point_chosen_flag'):
                        position = get_square_pos_from_mouse(pygame.mouse.get_pos())
                        STARTING_POINT = GRID[position[0]][position[1]]
                        if not STARTING_POINT.wall:
                            OPEN_SET.append(STARTING_POINT)
                            STARTING_POINT.color = COLORS.get('start_color')
                            FLAGS.update({'start_point_chosen_flag': True})
                        else:
                            print('There is a wall in this square. Try another square.')

                # Toogle key (e) add ending node to the grid on mouse click position
                if event.key == pygame.K_e:
                    if not FLAGS.get('end_point_chosen_flag'):
                        position = get_square_pos_from_mouse(pygame.mouse.get_pos())
                        END_POINT = GRID[position[0]][position[1]]
                        # check for wall or if starting node is present in the square
                        if not END_POINT.wall:
                            END_POINT.color = COLORS.get('end_color')
                            FLAGS.update({'end_point_chosen_flag': True})
                        else:
                            print('There is a wall in this square. Try another square.')
                if event.key == pygame.K_ESCAPE:
                    if FLAGS.get('settings_panel_visible'):
                        FLAGS.update({'settings_panel_visible' : False})
                    else:
                        FLAGS.update({'settings_panel_visible' : True})
                if event.key == pygame.K_i:
                    #invert_colors(window)
                    if not FLAGS.get('invert_grid_colors_flag'):
                        FLAGS.update({'invert_grid_colors_flag' : True})
                    else:
                        FLAGS.update({'invert_grid_colors_flag' : False})



        # start pathfinding
        if FLAGS.get('start_flag'):
            # Update the modes to runing
            MODES.update({'creator_mode': False})
            MODES.update({'running': True})

            try:
                result = a_star_pathfinding(True, STARTING_POINT, END_POINT)
            except:
                print('\nError: Initial node missing, both end and start nodes must be present.')
                print('Press (?) to view the available keybinds.\n')

                FLAGS.update({'start_flag' : False})
                continue

            # Avoid printing unlimited message when no solution is found!
            if result == -1:
                FLAGS.update({'start_flag': False})

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
                # Update mode to Done
                MODES.update({'running': False})
                MODES.update({'done': True})
            if GRID[square.x][square.y].color != COLORS.get('start_color'):
                GRID[square.x][square.y].color = COLORS.get('path_color')


        # Toogle coordinates on grid
        if FLAGS.get('show_coordinates_flag'):
            toogle_coordinates(window)

        # Toogle scores on the grid
        if FLAGS.get('show_scores_flag'):
            toogle_square_scores(window)

        # Toogle settings panel
        if FLAGS.get('settings_panel_visible'):
            draw_settings_panel(window)

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
