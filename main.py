# Created by Emanuel Ramirez on 09/08/2020

import pygame, math, sys, time
import config

# TODO: Refactor this later to make it mora pythonic!!!
# TODO: Propler docstrings
GRID = []
OPEN_SET, CLOSED_SET = [], []
PATH = []

STARTING_POINT = None
END_POINT      = None


clock = pygame.time.Clock()


class Square:
    def __init__(self, x, y):
        self.x = x # x coordinate
        self.y = y # y coordinate
        self.g = 0 # Distance from current node to starting node
        self.h = 0 # Distance from current node to end node
        self.f = 0 # g_total + h_total
        self.color = None
        self.neighbors = []
        self.wall = False
        self.prev = None

    def draw(self, window, color):
        self.color = color
        if self.wall:
            self.color = config.BLACK
        pygame.draw.rect(window, color, (self.x*get_width(), self.y*get_heigth(), get_width()-1, get_heigth()-1), 0)

    def add_neighbors(self, grid):
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


def build_neighbors_grid():
    ''' Create grid network of neighbors for each square'''
    for i in range(config.NUM_COLS):
        for j in range(config.NUM_ROWS):
            GRID[i][j].add_neighbors(GRID)


def build_initial_board():
    ''' Build the initial board state'''
    for col in range(config.NUM_COLS):
        array = []
        for row in range(config.NUM_ROWS):
            array.append(Square(col, row))
        GRID.append(array)


def draw_wall(mouse_pos, state):
    ''' Add a wall flag to the specified mouse poisition'''
    x_pos = mouse_pos[0]//get_width()
    y_pos = mouse_pos[1]//get_width()
    GRID[x_pos][y_pos].wall = True


def heuristics(a, b):
    ''' Returns an estimated the distance from current node to the end node'''
    return math.sqrt(abs(a.x-b.x)**2 + abs(a.y-b.y)**2)


def a_star_pathfinding(start_flag, start, end):
    ''' TODO: Think about a concise A* star explanation'''
    flag = False
    if not flag:
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
                    #print("We are done here!")
                    return
                elif flag:
                    return

            if not flag:
                OPEN_SET.remove(current)
                CLOSED_SET.append(current)

                for neighbor in current.neighbors:
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
                        #print(f'Neighbor: {neighbor} | End: {end}')
                        neighbor.h = heuristics(neighbor, end)
                        neighbor.f = neighbor.g + neighbor.h
                        neighbor.prev = current
            return flag
        else:
            print("No solution was found for the current configuration.")
            return -1



def main():
    ''' Program driver'''
    pygame.init()
    window = pygame.display.set_mode(config.WINDOW_SIZE)
    pygame.display.set_caption("A* Pathfinding Visualizer by Emanuel Ramirez")

    build_initial_board()
    build_neighbors_grid()

    start_flag               = False
    start_point_chosen_flag  = False
    end_point_chosen_flag    = False
    result_flag              = False

    start_time               = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_game()

            # Mouse click events
            if event.type == pygame.MOUSEBUTTONUP:
                if pygame.mouse.get_pressed(0):
                    draw_wall(pygame.mouse.get_pos(), True)
                if pygame.mouse.get_pressed(2):
                    draw_wall(pygame.mouse.get_pos(), False)

                if pygame.mouse.get_pressed(2):
                    draw_wall(pygame.mouse.get_pos(), False)

            # Mouse click and drag events
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    draw_wall(pygame.mouse.get_pos(), True)


            if event.type == pygame.KEYDOWN:
                # Start the visualizer
                if event.key == pygame.K_RETURN:
                    start_flag = True
                    start_time = pygame.time.get_ticks()
                if event.key == pygame.K_s: # Draw starting node on the board with (s) key
                    if not start_point_chosen_flag:
                        x_pos = math.floor(pygame.mouse.get_pos()[0]//get_width())
                        y_pos = math.floor(pygame.mouse.get_pos()[1]//get_width())
                        square = GRID[x_pos][y_pos]
                        STARTING_POINT = square
                        OPEN_SET.append(GRID[x_pos][y_pos]) # Add starting node to the open set
                        square.draw(window, config.GREEN)
                        start_point_chosen_flag = True
                if event.key == pygame.K_e: # Draw end node on the board with (e) key
                    if not end_point_chosen_flag:
                        x_pos = math.floor(pygame.mouse.get_pos()[0]//get_width())
                        y_pos = math.floor(pygame.mouse.get_pos()[1]//get_width())
                        square = GRID[x_pos][y_pos]
                        END_POINT = square
                        square.draw(window, config.LIGHT_BLUE)
                        end_point_chosen_flag = True

        # start pathfinding
        if start_flag:
            result = a_star_pathfinding(start_flag, STARTING_POINT, END_POINT)
            if result == -1:
                start_flag = False


        # Draw the current squares colors to the window
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
                elif square.color == config.BLACK:
                    square.draw(window, config.BLACK)
                else:
                    square.draw(window, config.WHITE)
        # Highlight the final path
        for square in PATH:
            square.draw(window, config.LIGHT_BLUE)
            start_flag = False
        pygame.display.flip()
        clock.tick(config.FPS) # Limit to 60 frames per second


def close_game():
    ''' Close the game'''
    pygame.quit()
    sys.exit()



if __name__ == '__main__':
    main()
