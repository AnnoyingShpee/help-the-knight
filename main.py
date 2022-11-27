# Python3 program to solve Knight Tour problem using Backtracking or Warnsdorff
import pygame as pg
import numpy as np
import pygame.time
import timeit

import Knight
# import ChessBoard
# import BacktrackTour
import WarnsdorffTour

pg.init()

# Global variables for display
BOARD_SIZE = (512, 512)     # Size of board
OFFSET = (50, 50)           # Amount of offset of the board from the border
SCREEN_SIZE = (900, 600)   # Size of game window
SCREEN = pg.display.set_mode(SCREEN_SIZE)  # Set game window
SCREEN.fill((180, 241, 255))  # Set background color
FONT = pg.font.SysFont('Arial', 35)  # Define font
DEFAULT_CURSOR = pg.mouse.get_cursor()
FPS = 1
clock = pygame.time.Clock()

# # white color
# button_color = (255, 255, 255)
#
# # light shade of the button
# color_light = (170, 170, 170)
#
# # dark shade of the button
# color_dark = (100, 100, 100)
#
# text = FONT.render('quit', True, button_color)

# Chess data
DIMENSIONS = 8  # Chessboard Size
# Size of each square is 64 x 64
SQ_SIZE = BOARD_SIZE[1] // DIMENSIONS
# Track knight's position in the board (row, col)
KNIGHT_POS = ()

colors = [pg.Color("white"), pg.Color("grey")]

# Tuple of moves (x, y) that can be done by the knight. Tuple because it will not be changed in any way.
# x = horizontal movement. POSITIVE value moves knight to the RIGHT while NEGATIVE value moves knight to the LEFT
# y = vertical movement. POSITIVE value moves knight DOWN while NEGATIVE value moves knight UP

# Set window Title
pg.display.set_caption("Knight Tour")
# Set window Icon
icon = pg.image.load("knight_piece.png")
pg.display.set_icon(icon)
# Create knight piece image
knight_piece = pg.image.load("knight_piece.png")
# Replaces cursor with a knight image
knight_cursor = pg.image.load("knight_piece.png")
# Create Start Button
# start_button = pg.rect()


# def draw_board(screen):
#     # Draw chessboard. Top left square is always light color
#     for row in range(DIMENSIONS):
#         for column in range(DIMENSIONS):
#             color = colors[(row + column) % 2]
#             pg.draw.rect(screen, color,
#                          # x-axis = column (left to right) , y-axis = row (top to bottom)
#                          # Draw the starting point of the square
#                          # Add off set if chessboard not touching the border of window
#                          # SQ_SIZE means the length and width of the squares
#                          pg.Rect((column * SQ_SIZE) + OFFSET[0], (row * SQ_SIZE) + OFFSET[1], SQ_SIZE, SQ_SIZE))
#
#
# def draw_knight(screen, board):
#     max_distance = board.max()
#     for row in range(DIMENSIONS):
#         for column in range(DIMENSIONS):
#             if board[row][column] != -1:
#                 if board[row][column] == max_distance:
#                     screen.blit(knight_piece,
#                                 pg.Rect((column*SQ_SIZE) + OFFSET[0], (row*SQ_SIZE) + OFFSET[1], SQ_SIZE, SQ_SIZE))
#                 else:
#                     color = colors[(row + column) % 2]
#                     pg.draw.rect(screen, color,
#                                  pg.Rect((column * SQ_SIZE) + OFFSET[0], (row * SQ_SIZE) + OFFSET[1], SQ_SIZE, SQ_SIZE))
#
#
# def draw_game_state(screen, cs):
#     draw_board(screen)
#     draw_knight(screen, cs.board)


def draw_board(screen):
    # Draw chessboard. Top left square is always light color
    for row in range(DIMENSIONS):
        for column in range(DIMENSIONS):
            color = colors[(row + column) % 2]
            pg.draw.rect(screen, color,
                         # x-axis = column (left to right) , y-axis = row (top to bottom)
                         # Draw the starting point of the square
                         # Add off set if chessboard not touching the border of window
                         # SQ_SIZE means the length and width of the squares
                         pg.Rect((column * SQ_SIZE) + OFFSET[0], (row * SQ_SIZE) + OFFSET[1], SQ_SIZE, SQ_SIZE))


class ChessState:
    # Board is n x n matrix
    def __init__(self, dimensions, knight_start=(0, 0)):
        self.dimensions = dimensions  # Dimension of chessboard
        self.board = np.negative(np.ones([dimensions, dimensions], dtype=int))
        self.knight_moves = ((2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1))
        self.knight_placed = False
        self.knight_pos = knight_start
        self.knight_step = -1

    def draw_knight(self, screen):
        furthest_node = self.board.max()
        print("Furthest:", furthest_node)
        for row in range(DIMENSIONS):
            for column in range(DIMENSIONS):
                if self.board[row][column] != -1 and self.board[row][column] == furthest_node:
                    # if self.board[row][column] == furthest_node:
                    print(row, column, "=", self.board[row][column])
                    screen.blit(knight_piece,
                                pg.Rect((column * SQ_SIZE) + OFFSET[0], (row * SQ_SIZE) + OFFSET[1], SQ_SIZE,
                                        SQ_SIZE))
                else:
                    color = colors[(row + column) % 2]
                    pg.draw.rect(screen, color,
                                 pg.Rect((column * SQ_SIZE) + OFFSET[0], (row * SQ_SIZE) + OFFSET[1], SQ_SIZE,
                                         SQ_SIZE))

    def draw_game_state(self, screen):
        # draw_board(screen)
        self.draw_knight(screen)

    def is_valid_move(self, x, y):
        '''
            A utility function to check if i,j are valid indexes
            for N*N chessboard
        '''
        if 0 <= x < self.dimensions and 0 <= y < self.dimensions and self.board[x][y] == -1:
            return True
        return False

    def print_solution(self):
        '''
            A utility function to print Chessboard matrix
        '''
        for i in range(self.dimensions):
            for j in range(self.dimensions):
                print(self.board[i][j], end=' ')
            print()

    def solve_backtrack(self):
        '''
            This function solves the Knight Tour problem using Backtracking. The backtracking algorithm uses a
            non-recursive method instead of recursion for ease on the pygame operation.
        '''

        # Since the Knight is initially at the first block
        self.board[self.knight_pos[0]][self.knight_pos[1]] = 0

        # Checking if solution exists or not
        # if not self.solve_backtrack_recursive(0, 0, pos):
        #     print("Solution does not exist")
        if not self.solve_backtrack_iterative():
            print("Solution does not exist")
        else:
            self.print_solution()
        self.board = np.negative(np.ones([self.dimensions, self.dimensions], dtype=int))
        self.knight_pos = (0, 0)
        self.knight_step = -1

    def solve_backtrack_iterative(self):
        '''
        This function uses a non-recursive backtracking algorithm to solve the knight's tour. This is a brute force
        method which isn't practical as the time complexity is O(8**(N**2)).
        :return: Boolean whether a solution was found
        '''
        # move_log stores list of squares traversed by the knight
        # Each square contains (row, column, last used index of knight_moves list)
        move_log = [(self.knight_pos[0], self.knight_pos[1], 0)]
        # The first step of the tour
        self.knight_step += 1
        # If
        while len(move_log) != 0 or self.knight_step < 63:
            contains_valid = False
            last_used_square = move_log[-1]
            for i in range(last_used_square[2], 8):
                new_x = last_used_square[0] + self.knight_moves[i][0]
                new_y = last_used_square[1] + self.knight_moves[i][1]
                if self.is_valid_move(new_x, new_y):
                    move_log[-1] = (self.knight_pos[0], self.knight_pos[1], i+1)
                    self.knight_step += 1
                    self.board[new_x][new_y] = self.knight_step
                    self.knight_pos = (new_x, new_y)
                    # print(self.knight_pos, self.knight_step)
                    new_pos = (new_x, new_y, 0)
                    move_log.append(new_pos)
                    contains_valid = True
                    if self.knight_step == 63:
                        print("Hit")
                        return True
                    break
            if not contains_valid:
                self.board[self.knight_pos[0]][self.knight_pos[1]] = -1
                self.knight_step -= 1
                move_log.pop()
                print("change")
                self.knight_pos = (move_log[-1][0], move_log[-1][1])
            #     print(self.knight_pos, self.knight_step)
            # print(self.board)
        return False

    # def solve_warnsdorff(self):


    # def solve_backtrack_recursive(self, curr_x, curr_y, pos):
    #     '''
    #         A recursive utility function to solve Knight Tour
    #         problem
    #     '''
    #     if pos == self.DIMENSIONS ** 2:
    #         return True
    #     # self.draw_game_state(SCREEN)
    #     print("Draw", pos)
    #     # pg.display.update()
    #     print("Drawn", pos)
    #
    #     # Try all next moves from the current coordinate x, y
    #     for i in range(8):
    #         new_x = curr_x + self.knight_moves[i][0]
    #         new_y = curr_y + self.knight_moves[i][1]
    #         if self.is_valid_move(new_x, new_y):
    #             self.board[new_x][new_y] = pos
    #             # self.draw_game_state(SCREEN)
    #             # pg.display.update()
    #             if self.solve_backtrack_recursive(new_x, new_y, pos + 1):
    #                 return True
    #             # Backtracking
    #             self.board[new_x][new_y] = -1
    #             # self.draw_game_state(SCREEN)
    #             print("Update dead end", new_x, new_y)
    #             # pg.display.update()
    #             print("Updated dead end", new_x, new_y)
    #     return False


# class Move:
#     def __init__(self, start_sq, end_sq, board):
#         self.start_row = start_sq[0]
#         self.start_col = start_sq[1]
#         self.end_row = end_sq[0]
#         self.end_col = end_sq[1]

def main():
    chess_state = ChessState(DIMENSIONS, (7, 0))
    running = True
    sq_selected = ()  # No square selected initially
    global KNIGHT_POS
    draw_board(SCREEN)
    start_tour = False
    while running:
        clock.tick(FPS)
        mouse_pos = pg.mouse.get_pos()  # Returns (x, y) position of mouse as a tuple
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if OFFSET[0] < mouse_pos[0] < OFFSET[0] + BOARD_SIZE[0] and \
                        OFFSET[1] < mouse_pos[1] < OFFSET[1] + BOARD_SIZE[1]:
                    row = (mouse_pos[1] - OFFSET[1]) // SQ_SIZE
                    col = (mouse_pos[0] - OFFSET[0]) // SQ_SIZE
                    print("Cursor =", mouse_pos)
                    print("Square =", row, col)
                    sq_selected = (row, col)
                    # Checks if user selected the same square twice or out of board bounds
                    if sq_selected == KNIGHT_POS:
                        print("Same Square")
                        chess_state.knight_placed = False
                        KNIGHT_POS = ()
                        chess_state.board[row][col] = -1
                        chess_state.knight_step -= 1
                    elif not chess_state.knight_placed:
                        chess_state.knight_placed = True
                        KNIGHT_POS = (row, col)
                        chess_state.knight_step += 1
                        chess_state.board[row][col] = chess_state.knight_step
                    elif chess_state.knight_placed:
                        chess_state.board[KNIGHT_POS[0]][KNIGHT_POS[1]] = -1
                        KNIGHT_POS = (row, col)
                        chess_state.board[row][col] = chess_state.knight_step
                if

        if start_tour:
            chess_state.solve_backtrack()
            start_tour = False

                # elif chess_state.knight_placed:
                #     chess_state.board[KNIGHT_POS[0]][KNIGHT_POS[1]] = -1
                #     KNIGHT_POS = (row, col)
                #     chess_state.board[row][col] = path_index
                # elif not chess_state.knight_placed:
                #     chess_state.knight_placed = True
                #     KNIGHT_POS = (row, col)
                #     path_index += 1
                #     chess_state.board[row][col] = path_index
                # elif row < 0 or row > 7 or col < 0 or col > 7:
                #     print("Not valid")
                # elif chess_state.knight_placed:
                #     print("Knight already placed")
    #     #         elif
    #
    #     # if mouse is hovered on a button it
    #     # changes to lighter shade
    #     # if 600 <= mouse_pos[0] <= 600 + 200 and 500 <= mouse_pos[1] <= 500 + 40:
    #     #     pg.draw.rect(SCREEN, color_light, pg.Rect(600, 500, 200, 40))
    #     # else:
    #     #     pg.draw.rect(SCREEN, color_dark, pg.Rect(600, 500, 200, 40))
    #
    #     # superimposing the text onto our button
    #     # SCREEN.blit(text, (600 + 100, 500))
    #     chess_state.draw_game_state(SCREEN)
    # # chess_state.solve_backtrack()
    #     pg.display.flip()
        #


# Driver Code
if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print('Time: ', stop - start)
    # bt = bt.BacktrackTour(DIMENSIONS)
    # bt.solve_backtrack()

