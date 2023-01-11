# Python3 program to solve Knight Tour problem using Backtracking or Warnsdorff
import sys

import pygame as pg
import numpy as np
import random
import timeit

pg.init()

# Global variables for display
SCREEN = pg.display.set_mode(size=(0, 0))  # Set game window
BACKGROUND_COLOUR = (180, 241, 255)
SCREEN.fill(BACKGROUND_COLOUR)  # Set background color
x_axis, y_axis = SCREEN.get_size()
print(x_axis, y_axis)
BOARD_SIZE = ((y_axis // 10) * 8, (y_axis // 10) * 8)  # Size of board
print(BOARD_SIZE)
OFFSET = (50, 50)  # Amount of offset of the board from the border
# SCREEN_SIZE = (900, 600)  # Size of game window
# SCREEN = pg.display.set_mode(SCREEN_SIZE)  # Set game window
BUTTON_FONT = pg.font.SysFont('Arial', 30)  # Font for buttons
BOARD_FONT = pg.font.SysFont('Arial', 20)  # Font for numbering the steps
# DEFAULT_CURSOR = pg.mouse.get_cursor()
FPS = 60
clock = pg.time.Clock()

# Buttons
# pg.Rect(x_position, y_position, width, height)
# start_button = pg.Rect(600, 50, 230, 40)
# reset_button = pg.Rect(600, 170, 230, 40)
# backtrack_button = pg.Rect(600, 290, 230, 40)
# warnsdorff_button = pg.Rect(600, 410, 230, 40)
# quit_button = pg.Rect(600, 530, 230, 40)
start_details = ((x_axis//10)*8, y_axis//10, (x_axis//100)*15, y_axis//20)
reset_details = ((x_axis//10)*8, (y_axis//10)*3, (x_axis//100)*15, y_axis//20)
backtrack_details = ((x_axis//10)*8, (y_axis//10)*5, (x_axis//100)*15, y_axis//20)
warnsdorff_details = ((x_axis//10)*8, (y_axis//10)*7, (x_axis//100)*15, y_axis//20)
quit_details = ((x_axis//10)*8, (y_axis//10)*9, (x_axis//100)*15, y_axis//20)
start_button = pg.Rect(start_details[0], start_details[1], start_details[2], start_details[3])
reset_button = pg.Rect(reset_details[0], reset_details[1], reset_details[2], reset_details[3])
backtrack_button = pg.Rect(backtrack_details[0], backtrack_details[1], backtrack_details[2], backtrack_details[3])
warnsdorff_button = pg.Rect(warnsdorff_details[0], warnsdorff_details[1], warnsdorff_details[2], warnsdorff_details[3])
quit_button = pg.Rect(quit_details[0], quit_details[1], quit_details[2], quit_details[3])
button_color = (100, 100, 100)  # Default button color
hover_button_color = (170, 170, 170)  # Color of button when cursor hovers over

# Button text color
text_color = (255, 255, 255)
start_text = BUTTON_FONT.render("Start", True, text_color)
reset_text = BUTTON_FONT.render("Reset", True, text_color)
backtrack_text = BUTTON_FONT.render("Backtrack Method", True, text_color)
warnsdorff_text = BUTTON_FONT.render("Warnsdoff's Method", True, text_color)
quit_text = BUTTON_FONT.render("Quit", True, text_color)

# Chess board data
DIMENSIONS = 8  # Chessboard Size
# Size of each square
SQ_SIZE = BOARD_SIZE[0] // DIMENSIONS
# Coloring of board
BOARD_COLORS = [pg.Color("white"), pg.Color("grey")]

# Set window Title
pg.display.set_caption("Knight Tour")
# Set window Icon
icon = pg.image.load("knight_piece.png")
pg.display.set_icon(icon)
# Create knight piece image
knight_piece = pg.image.load("knight_piece.png")
# Replaces cursor with a knight image
# knight_cursor = pg.image.load("knight_piece.png")
movement = 0


# def draw_board(screen):
#     # Draw chessboard. Top left square is always light color
#     for row in range(DIMENSIONS):
#         for column in range(DIMENSIONS):
#             color = BOARD_COLORS[(row + column) % 2]
#             pg.draw.rect(screen, color,
#                          # x-axis = column (left to right) , y-axis = row (top to bottom)
#                          # Draw the starting point of the square
#                          # Add off set if chessboard not touching the border of window
#                          # SQ_SIZE means the length and width of the squares
#                          pg.Rect((column * SQ_SIZE) + OFFSET[0], (row * SQ_SIZE) + OFFSET[1], SQ_SIZE, SQ_SIZE))

# class Cell:
#     def __init__(self):
#         self.color = None
#         self.traversed = -1
#         self.refresh = False

class Board:
    def __init__(self, dimension):
        self.dimension = dimension
        self.graph = np.negative(np.ones([dimension, dimension], dtype=int))
        # self.graph = np.ones([dimension, dimension], dtype=int)
        # for row in range(self.dimension):
        #     for column in range(self.dimension):
        #         self.graph[row][column] = (0, 0)

    def draw_board(self):
        # Draw chessboard. Top left square is always light color
        for row in range(self.dimension):
            for column in range(self.dimension):
                color = BOARD_COLORS[(row + column) % 2]
                pg.draw.rect(SCREEN, color,
                             # x-axis = column (left to right) , y-axis = row (top to bottom)
                             # Draw the starting point of the square
                             # Add off set if chessboard not touching the border of window
                             # SQ_SIZE means the length and width of the squares
                             pg.Rect((column * SQ_SIZE) + OFFSET[0], (row * SQ_SIZE) + OFFSET[1], SQ_SIZE, SQ_SIZE))

    def draw_square(self, row, col):
        color = BOARD_COLORS[(row + col) % 2]
        pg.draw.rect(SCREEN, color, pg.Rect((col * SQ_SIZE) + OFFSET[0], (row * SQ_SIZE) + OFFSET[1], SQ_SIZE, SQ_SIZE))

    def draw_number(self, row, col):
        '''
        This function is responsible for drawing the numbers of the steps made by the knight
        :param screen: Pygame screen
        :param row: Row number of board
        :param col: Column number of board
        :return:None
        '''
        if self.graph[row][col] != -1:
            stamp = ((col * SQ_SIZE) + OFFSET[0] + SQ_SIZE//2, (row * SQ_SIZE) + OFFSET[1] + SQ_SIZE//2)
            pg.draw.circle(SCREEN, (255, 0, 0), stamp, 30)
            number = self.graph[row][col]
            SCREEN.blit(BOARD_FONT.render(f"{number: 03d}", True, (255, 255, 255)),
                        (stamp[0] - SQ_SIZE*0.14, stamp[1] - SQ_SIZE*0.13))

    # def draw_line(self, screen, curr_pos, new_pos):
    #     start_point = (curr_pos[0]*SQ_SIZE + SQ_SIZE//2, curr_pos[1]*SQ_SIZE + SQ_SIZE//2)
    #     end_point = (new_pos[0]*SQ_SIZE + SQ_SIZE//2, new_pos[1]*SQ_SIZE + SQ_SIZE//2)
    #     pg.draw.line(screen, (255, 0, 0), start_point, end_point, 5)


class Knight:
    def __init__(self):
        """
            Tuple of moves (x, y) that can be done by the knight. Tuple because it will not be changed in any way.
            x = horizontal movement. POSITIVE value moves knight to the RIGHT while NEGATIVE value moves it to the LEFT
            y = vertical movement. POSITIVE value moves knight DOWN while NEGATIVE value moves knight UP
        """
        self.knight_moves = ((2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1))
        self.knight_placed = False
        self.knight_initial_pos = None
        self.knight_pos = None
        self.knight_step = 1
        self.move_log = []  # Contains the squares traversed and next
        self.possible_moves = []

    def draw_knight(self):
        SCREEN.blit(knight_piece,
                    pg.Rect((self.knight_pos[1] * SQ_SIZE) + OFFSET[0] + SQ_SIZE // 8,
                            (self.knight_pos[0] * SQ_SIZE) + OFFSET[1] + SQ_SIZE // 8,
                            SQ_SIZE, SQ_SIZE)
                    )


class ChessState:
    # def __init__(self, dimensions):
    #     self.dimensions = dimensions  # Dimension of chessboard
    #     # Initialise board array. Board is n x n matrix
    #     self.board = np.negative(np.ones([dimensions, dimensions], dtype=int))
    #     # Tuple of moves (x, y) that can be done by the knight. Tuple because it will not be changed in any way.
    #     # x = horizontal movement. POSITIVE value moves knight to the RIGHT while NEGATIVE value moves it to the LEFT
    #     # y = vertical movement. POSITIVE value moves knight DOWN while NEGATIVE value moves knight UP
    #     self.knight_moves = ((2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1))
    #     # State of chessboard (start, ready, touring, fail)
    #     self.state = "start"
    #     self.tour_found = False
    #     # Whether game is running
    #     self.running = True
    #     self.knight_placed = False
    #     self.knight_initial_pos = None
    #     self.knight_pos = None
    #     self.knight_step = 1
    #     self.warnsdorff = False
    #     self.move_log = []

    def __init__(self, board: Board, knight: Knight):
        # Initialise board array. Board is n x n matrix
        self.board = board
        self.knight = knight
        # State of chessboard (start, ready, touring, fail)
        self.state = "start"
        self.tour_found = False  # Whether knight tour is found
        self.running = True  # Whether game is running
        self.warnsdorff = False
        self.board.draw_board()

    def reset_board(self):
        self.board.graph = np.negative(np.ones([self.board.dimension, self.board.dimension], dtype=int))
        self.state = "start"
        self.tour_found = False
        self.knight.knight_placed = False
        self.knight.knight_initial_pos = None
        self.knight.knight_pos = None
        self.knight.knight_step = 1
        self.knight.move_log = []
        SCREEN.fill(BACKGROUND_COLOUR)
        self.board.draw_board()

    def redo_tour(self):
        self.state = "touring"
        self.board.graph = np.negative(np.ones([self.board.dimension, self.board.dimension], dtype=int))
        self.knight.knight_step = 1
        self.knight.move_log = []
        self.knight.knight_pos = self.knight.knight_initial_pos
        SCREEN.fill(BACKGROUND_COLOUR)
        self.board.draw_board()

    # Checks if user selected the same square twice. If so, remove the knight
    def place_first_knight(self, selected_sq):
        if self.state == "touring":
            return
        row = selected_sq[0]
        col = selected_sq[1]
        # Checks if user selected the same square twice. If so, remove the knight
        if selected_sq == self.knight.knight_pos:
            print("Same Square")
            self.board.draw_square(self.knight.knight_pos[0], self.knight.knight_pos[1])
            self.board.graph[row][col] = -1
            self.knight.knight_placed = False
            self.knight.knight_pos = None
            self.knight.knight_initial_pos = None
            self.state = "start"
            self.knight.move_log.pop()
        elif not self.knight.knight_placed:
            self.knight.knight_placed = True
            self.knight.knight_pos = (row, col)
            self.knight.knight_initial_pos = (row, col)
            self.board.graph[row][col] = 1
            self.state = "ready"
            self.knight.draw_knight()
            self.knight.move_log.append((row, col, 0))
        elif self.knight.knight_placed:
            self.board.draw_square(self.knight.knight_pos[0], self.knight.knight_pos[1])
            self.knight.move_log.pop()
            self.board.graph[self.knight.knight_pos[0]][self.knight.knight_pos[1]] = -1
            self.knight.knight_pos = (row, col)
            self.knight.knight_initial_pos = (row, col)
            self.board.graph[row][col] = 1
            self.knight.move_log.append((row, col, 0))
            self.knight.draw_knight()
        # self.redraw_board()

    def draw_lines(self):
        i = 0
        while i < len(self.knight.move_log):
            if i > 0:
                start_point = self.knight.move_log[i - 1]
                line_start_point = (start_point[0] * SQ_SIZE + SQ_SIZE // 2, start_point[1] * SQ_SIZE + SQ_SIZE // 2)
                end_point = self.knight.move_log[i]
                line_end_point = (end_point[0] * SQ_SIZE + SQ_SIZE // 2, end_point[1] * SQ_SIZE + SQ_SIZE // 2)
                pg.draw.line(SCREEN, (255, 0, 0), line_start_point, line_end_point, 5)
                i += 1

    def draw_line(self):
        start_point = self.knight.move_log[-2]
        line_start_point = (start_point[0] * SQ_SIZE + SQ_SIZE // 2, start_point[1] * SQ_SIZE + SQ_SIZE // 2)
        end_point = self.knight.move_log[-1]
        line_end_point = (end_point[0] * SQ_SIZE + SQ_SIZE // 2, end_point[1] * SQ_SIZE + SQ_SIZE // 2)
        pg.draw.line(SCREEN, (255, 0, 0), line_start_point, line_end_point, 5)

    def redraw_board(self):
        furthest_node = self.board.graph.max()
        # print("Furthest:", furthest_node)

        self.board.draw_board()
        self.draw_lines()

        if furthest_node == self.board.dimension ** 2:
            self.board.draw_number(self.knight.knight_pos[0], self.knight.knight_pos[1])
        else:
            SCREEN.blit(knight_piece,
                        pg.Rect((self.knight.knight_pos[1] * SQ_SIZE) + OFFSET[0] + SQ_SIZE // 8,
                                (self.knight.knight_pos[0] * SQ_SIZE) + OFFSET[1] + SQ_SIZE // 8,
                                SQ_SIZE, SQ_SIZE)
                        )

        # for row in range(self.board.dimension):
        #     for column in range(self.board.dimension):
        #         if self.board.graph[row][column] != -1:
        #             if self.board.graph[row][column] == furthest_node:
        #                 if furthest_node == self.board.dimension ** 2:
        #                     self.board.draw_number(row, column)
        #                 else:
        #                     # pg.draw.rect(screen, color,
        #                     #              pg.Rect((column * SQ_SIZE) + OFFSET[0], (row * SQ_SIZE) + OFFSET[1], SQ_SIZE,
        #                     #                      SQ_SIZE))
        #                     # self.draw_line()
        #                     SCREEN.blit(knight_piece,
        #                                 pg.Rect((column * SQ_SIZE) + OFFSET[0] + SQ_SIZE // 8,
        #                                         (row * SQ_SIZE) + OFFSET[1] + SQ_SIZE // 8,
        #                                         SQ_SIZE, SQ_SIZE))

        pg.display.update()

    # Handles mouse input
    def check_event(self):
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                # Checks if mouse clicks on board area
                if OFFSET[0] < mouse_pos[0] < OFFSET[0] + BOARD_SIZE[0] and \
                   OFFSET[1] < mouse_pos[1] < OFFSET[1] + BOARD_SIZE[1]:
                    row = (mouse_pos[1] - OFFSET[1]) // SQ_SIZE
                    col = (mouse_pos[0] - OFFSET[0]) // SQ_SIZE
                    sq_selected = (row, col)
                    self.place_first_knight(sq_selected)
                # Start Button. To start the tour
                elif start_details[0] <= mouse_pos[0] <= start_details[0] + start_details[2] \
                        and start_details[1] <= mouse_pos[1] <= start_details[1] + start_details[3] \
                        and self.knight.knight_placed:
                    self.state = "touring"
                # Reset Button. Resets the board
                elif reset_details[0] <= mouse_pos[0] <= reset_details[0] + reset_details[2] \
                        and reset_details[1] <= mouse_pos[1] <= reset_details[1] + reset_details[3]:
                    self.reset_board()
                # Backtrack Button. Change the tour finding method to backtracking
                elif backtrack_details[0] <= mouse_pos[0] <= backtrack_details[0] + backtrack_details[2] \
                        and backtrack_details[1] <= mouse_pos[1] <= backtrack_details[1] + backtrack_details[3] \
                        and self.state != "touring":
                    self.warnsdorff = False
                # Warnsdorff Button. Change the tour finding method to Warnsdorff
                elif warnsdorff_details[0] <= mouse_pos[0] <= warnsdorff_details[0] + warnsdorff_details[2] \
                        and warnsdorff_details[1] <= mouse_pos[1] <= warnsdorff_details[1] + warnsdorff_details[3] \
                        and self.state != "touring":
                    self.warnsdorff = True
                # Quit Button. Stops the game
                elif quit_details[0] <= mouse_pos[0] <= quit_details[0] + quit_details[2] \
                        and quit_details[1] <= mouse_pos[1] <= quit_details[1] + quit_details[3]:
                    self.running = False

        # Display Start button and text
        if start_details[0] <= mouse_pos[0] <= start_details[0] + start_details[2] \
                and start_details[1] <= mouse_pos[1] <= start_details[1] + start_details[3]:
            pg.draw.rect(SCREEN, hover_button_color, start_button)
        else:
            pg.draw.rect(SCREEN, button_color, start_button)
        SCREEN.blit(start_text, (start_details[0] + (4*start_details[2]//10), start_details[1] + 5))
        # Display Reset button and text
        if reset_details[0] <= mouse_pos[0] <= reset_details[0] + reset_details[2] \
                and reset_details[1] <= mouse_pos[1] <= reset_details[1] + reset_details[3]:
            pg.draw.rect(SCREEN, hover_button_color, reset_button)
        else:
            pg.draw.rect(SCREEN, button_color, reset_button)
        SCREEN.blit(reset_text, (reset_details[0] + (3.5*reset_details[2]//10), reset_details[1] + 5))
        if self.warnsdorff:
            # Display Backtrack button and text
            if backtrack_details[0] <= mouse_pos[0] <= backtrack_details[0] + backtrack_details[2] \
                    and backtrack_details[1] <= mouse_pos[1] <= backtrack_details[1] + backtrack_details[3]:
                pg.draw.rect(SCREEN, hover_button_color, backtrack_button)
            else:
                pg.draw.rect(SCREEN, button_color, backtrack_button)
            SCREEN.blit(backtrack_text, (backtrack_details[0]+(0.5*backtrack_details[2]//10), backtrack_details[1] + 5))
            # Remove Warnsdorff button
            pg.draw.rect(SCREEN, BACKGROUND_COLOUR, warnsdorff_button)
        else:
            # Display Warnsdorff button and text
            if warnsdorff_details[0] <= mouse_pos[0] <= warnsdorff_details[0] + warnsdorff_details[2] \
                    and warnsdorff_details[1] <= mouse_pos[1] <= warnsdorff_details[1] + warnsdorff_details[3]:
                pg.draw.rect(SCREEN, hover_button_color, warnsdorff_button)
            else:
                pg.draw.rect(SCREEN, button_color, warnsdorff_button)
            SCREEN.blit(warnsdorff_text, (warnsdorff_details[0], warnsdorff_details[1] + 5))
            # Remove Backtrack button
            pg.draw.rect(SCREEN, BACKGROUND_COLOUR, backtrack_button)
        # Quit button
        if quit_details[0] <= mouse_pos[0] <= quit_details[0] + quit_details[2] \
                and quit_details[1] <= mouse_pos[1] <= quit_details[1] + quit_details[3]:
            pg.draw.rect(SCREEN, hover_button_color, quit_button)
        else:
            pg.draw.rect(SCREEN, button_color, quit_button)
        SCREEN.blit(quit_text, (quit_details[0] + (4*quit_details[2]//10), quit_details[1] + 5))

        pg.display.update()

    def is_valid_move(self, x, y):
        """
            A utility function to check if i,j are valid indexes
            for N*N chessboard
            :param x: row number of square
            :param y: column number of square
        """
        if 0 <= x < self.board.dimension and 0 <= y < self.board.dimension and self.board.graph[x][y] == -1:
            return True
        return False

    def count_empty_squares(self, next_x, next_y):
        count = 0
        for i in range(8):
            if self.is_valid_move(next_x + self.knight.knight_moves[i][0], next_y + self.knight.knight_moves[i][1]):
                count += 1
        return count

    # def print_solution(self):
    #     '''
    #         A utility function to print Chessboard matrix
    #     '''
    #     for i in range(self.dimensions):
    #         for j in range(self.dimensions):
    #             print(self.board[i][j], end=' ')
    #         print()
    #     print()

    def find_tour(self):
        """
            This function acts as the main component for finding tour, performs operations and is called .
        """
        # First checks whether tour has already been found
        if not self.tour_found:
            if self.warnsdorff:
                if self.knight.knight_step < 64:
                    self.find_tour_warnsdorff()
                else:
                    self.tour_found = True
                    # self.print_solution()
            else:
                if len(self.knight.move_log) == 0:
                    self.state = "fail"
                if self.knight.knight_step < 64:
                    self.find_tour_backtrack_iterative()
                else:
                    self.tour_found = True

    def find_tour_warnsdorff(self):
        most_empty = 9
        most_empty_index = -1

        # To give some randomness when choosing a square. Only useful for next squares with the same number of next
        # valid squares
        random_num = random.randint(0, 1000) % 8
        for i in range(8):
            index = (random_num + i) % 8
            new_x = self.knight.knight_pos[0] + self.knight.knight_moves[index][0]
            new_y = self.knight.knight_pos[1] + self.knight.knight_moves[index][1]
            empty_sq_count = self.count_empty_squares(new_x, new_y)
            if self.is_valid_move(new_x, new_y) and empty_sq_count < most_empty:
                most_empty_index = index
                most_empty = empty_sq_count
            if self.is_valid_move(new_x, new_y) and empty_sq_count == most_empty:
                possible_move = (new_x, new_y)
                self.knight.possible_moves.append(possible_move)

        if most_empty_index == -1:
            self.state = "fail"
            return False

        new_x = self.knight.knight_pos[0] + self.knight.knight_moves[most_empty_index][0]
        new_y = self.knight.knight_pos[1] + self.knight.knight_moves[most_empty_index][1]
        self.knight.knight_step += 1
        self.board.graph[new_x][new_y] = self.knight.knight_step
        self.knight.knight_pos = (new_x, new_y)
        self.knight.move_log.append((new_x, new_y))
        self.knight.draw_knight()
        # self.redraw_board()

    def find_tour_backtrack_iterative(self):
        """
        This function uses a non-recursive backtracking algorithm to solve the knight's tour. This is a brute force
        method which isn't practical as the time complexity is O(8**(N**2)).

        The steps are as follows
        1.  Get last square of the move log
        2.  Check if there are valid moves to be made by the knight from the square
        3.  If a valid move is found, use the move to move the knight and add the new square to the log. Update the
            previous square with the next move.
        4. If no valid move is found, remove the square from the log
        """
        # move_log stores list of squares traversed by the knight
        # Each square contains (row, column, next index to use of knight_moves list)
        last_used_square = self.knight.move_log[-1]
        contains_valid = False
        # Checks if the square has valid moves, if so, move to that new square
        for i in range(last_used_square[2], 8):
            new_x = last_used_square[0] + self.knight.knight_moves[i][0]
            new_y = last_used_square[1] + self.knight.knight_moves[i][1]
            if self.is_valid_move(new_x, new_y):
                # Update the last square of move_log so that the next knight move to check will be the next one
                self.knight.move_log[-1] = (self.knight.knight_pos[0], self.knight.knight_pos[1], i + 1)
                self.knight.knight_step += 1
                self.board.graph[new_x][new_y] = self.knight.knight_step
                self.knight.knight_pos = (new_x, new_y)
                new_pos = (new_x, new_y, 0)
                self.knight.move_log.append(new_pos)
                contains_valid = True
                break
        # If no valid moves can be done, remove square from stack
        if not contains_valid:
            self.board.graph[self.knight.knight_pos[0]][self.knight.knight_pos[1]] = -1
            self.knight.knight_step -= 1
            self.knight.move_log.pop()
            self.knight.knight_pos = (self.knight.move_log[-1][0], self.knight.move_log[-1][1])

        # self.print_solution()
        self.redraw_board()
        # pg.display.update()

    def update_frame(self):
        if self.state == "touring":
            self.find_tour()
        if self.state == "fail":
            self.redo_tour()
        if not self.running:
            stop = timeit.default_timer()
            print('Time: ', stop - start, "seconds")
            print(movement, "Iterations")
            pg.quit()
            sys.exit()
        self.check_event()
        pg.event.pump()


def main():
    board = Board(DIMENSIONS)
    knight = Knight()
    chess_state = ChessState(board, knight)
    while True:
        clock.tick(FPS)
        chess_state.update_frame()


if __name__ == "__main__":
    # start = timeit.default_timer()
    # chess_state = ChessState(8)
    # chess_state.find_tour()
    start = timeit.default_timer()
    main()
    # stop = timeit.default_timer()
    # print('Time: ', stop - start)
