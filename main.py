# Python3 program to solve Knight Tour problem using Backtracking or Warnsdorff
import sys

import pygame as pg
import numpy as np
import random
import pygame.time
import timeit

import Knight
# import ChessBoard
# import BacktrackTour
import WarnsdorffTour

pg.init()

# Global variables for display
BOARD_SIZE = (512, 512)  # Size of board
OFFSET = (50, 50)  # Amount of offset of the board from the border
SCREEN_SIZE = (900, 600)  # Size of game window
SCREEN = pg.display.set_mode(SCREEN_SIZE)  # Set game window
BACKGROUND_COLOUR = (180, 241, 255)
SCREEN.fill(BACKGROUND_COLOUR)  # Set background color
BUTTON_FONT = pg.font.SysFont('Arial', 30)  # Font for buttons
BOARD_FONT = pg.font.SysFont('Arial', 20)  # Font for numbering the steps
# DEFAULT_CURSOR = pg.mouse.get_cursor()
FPS = 60
clock = pygame.time.Clock()

# Buttons
start_button = pg.Rect(600, 50, 230, 40)
reset_button = pg.Rect(600, 170, 230, 40)
backtrack_button = pg.Rect(600, 290, 230, 40)
warnsdorff_button = pg.Rect(600, 410, 230, 40)
quit_button = pg.Rect(600, 530, 230, 40)
# Default button color
button_color = (100, 100, 100)
# Color of button when cursor hovers over
hover_button_color = (170, 170, 170)

# Button text color
text_color = (255, 255, 255)
start_text = BUTTON_FONT.render("Start", True, text_color)
reset_text = BUTTON_FONT.render("Reset", True, text_color)
backtrack_text = BUTTON_FONT.render("Backtrack Method", True, text_color)
warnsdorff_text = BUTTON_FONT.render("Warnsdoff's Method", True, text_color)
quit_text = BUTTON_FONT.render("Quit", True, text_color)

# Chess board data
DIMENSIONS = 8  # Chessboard Size
# Size of each square is 64 x 64
SQ_SIZE = BOARD_SIZE[1] // DIMENSIONS
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
knight_cursor = pg.image.load("knight_piece.png")


def draw_board(screen):
    # Draw chessboard. Top left square is always light color
    for row in range(DIMENSIONS):
        for column in range(DIMENSIONS):
            color = BOARD_COLORS[(row + column) % 2]
            pg.draw.rect(screen, color,
                         # x-axis = column (left to right) , y-axis = row (top to bottom)
                         # Draw the starting point of the square
                         # Add off set if chessboard not touching the border of window
                         # SQ_SIZE means the length and width of the squares
                         pg.Rect((column * SQ_SIZE) + OFFSET[0], (row * SQ_SIZE) + OFFSET[1], SQ_SIZE, SQ_SIZE))

movement = 0
class ChessState:
    # Board is n x n matrix
    def __init__(self, dimensions):
        self.dimensions = dimensions  # Dimension of chessboard
        # Initialise board array
        self.board = np.negative(np.ones([dimensions, dimensions], dtype=int))
        # Tuple of moves (x, y) that can be done by the knight. Tuple because it will not be changed in any way.
        # x = horizontal movement. POSITIVE value moves knight to the RIGHT while NEGATIVE value moves knight to the LEFT
        # y = vertical movement. POSITIVE value moves knight DOWN while NEGATIVE value moves knight UP
        self.knight_moves = ((2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1))
        # State of chessboard (start, ready, touring, fail)
        self.state = "start"
        self.tour_found = False
        # Whether game is running
        self.running = True
        self.knight_placed = False
        self.knight_initial_pos = None
        self.knight_pos = None
        self.knight_step = 1
        self.warnsdorff = False
        self.move_log = []

    def reset_board(self):
        self.board = np.negative(np.ones([self.dimensions, self.dimensions], dtype=int))
        self.state = "start"
        self.knight_placed = False
        self.knight_initial_pos = None
        self.knight_pos = None
        self.knight_step = 1
        self.move_log = []
        SCREEN.fill(BACKGROUND_COLOUR)
        draw_board(SCREEN)

    def redo_tour(self):
        self.board = np.negative(np.ones([self.dimensions, self.dimensions], dtype=int))
        self.knight_step = 1
        self.move_log = []
        SCREEN.fill(BACKGROUND_COLOUR)
        draw_board(SCREEN)

    # Checks if user selected the same square twice. If so, remove the knight
    def place_first_knight(self, selected_sq):
        if self.state == "touring":
            return
        row = selected_sq[0]
        col = selected_sq[1]
        # Checks if user selected the same square twice. If so, remove the knight
        if selected_sq == self.knight_pos:
            print("Same Square")
            self.board[row][col] = -1
            self.knight_placed = False
            self.knight_pos = None
            self.knight_initial_pos = None
            self.state = "start"
            self.move_log.pop()
        elif not self.knight_placed:
            self.knight_placed = True
            self.knight_pos = (row, col)
            self.knight_initial_pos = (row, col)
            self.board[row][col] = 1
            self.state = "ready"
            self.move_log.append((self.knight_pos[0], self.knight_pos[1], 0))
        elif self.knight_placed:
            self.move_log.pop()
            self.board[self.knight_pos[0]][self.knight_pos[1]] = -1
            self.knight_pos = (row, col)
            self.knight_initial_pos = (row, col)
            self.board[row][col] = 1
            self.move_log.append((self.knight_pos[0], self.knight_pos[1], 0))
        self.draw_knight(SCREEN)

    def draw_knight(self, screen):
        furthest_node = self.board.max()
        # print("Furthest:", furthest_node)
        for row in range(self.dimensions):
            for column in range(self.dimensions):
                if self.board[row][column] != -1 and self.board[row][column] == furthest_node:
                    color = BOARD_COLORS[(row + column) % 2]
                    pg.draw.rect(screen, color,
                                 pg.Rect((column * SQ_SIZE) + OFFSET[0], (row * SQ_SIZE) + OFFSET[1], SQ_SIZE,
                                         SQ_SIZE))
                    screen.blit(knight_piece,
                                pg.Rect((column * SQ_SIZE) + OFFSET[0], (row * SQ_SIZE) + OFFSET[1], SQ_SIZE,
                                        SQ_SIZE))
                else:
                    color = BOARD_COLORS[(row + column) % 2]
                    pg.draw.rect(screen, color,
                                 pg.Rect((column * SQ_SIZE) + OFFSET[0], (row * SQ_SIZE) + OFFSET[1], SQ_SIZE,
                                         SQ_SIZE))
                    self.draw_number(screen, row, column)

        pg.display.update()

    def draw_number(self, screen, row, col):
        '''
        This function is responsible for drawing the numbers of the steps made by the knight
        :param screen: Pygame screen
        :param row: Row of board
        :param col: Column of board
        :return:None
        '''
        if self.board[row][col] != -1:
            stamp = ((col * SQ_SIZE) + OFFSET[0] + 30, (row * SQ_SIZE) + OFFSET[1] + 30)
            pg.draw.circle(screen, (255, 0, 0), stamp, 20)
            screen.blit(BOARD_FONT.render(str(self.board[row][col]), True, (255, 255, 255)),
                        (stamp[0] - 10, stamp[1] - 10))

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
                elif 600 <= mouse_pos[0] <= 600 + 230 and 50 <= mouse_pos[1] <= 50 + 40 and self.knight_placed:
                    self.state = "touring"
                # Reset Button. Resets the board
                elif 600 <= mouse_pos[0] <= 600 + 230 and 170 <= mouse_pos[1] <= 170 + 40:
                    self.reset_board()
                # Backtrack Button. Change the tour finding method to backtracking
                elif 600 <= mouse_pos[0] <= 600 + 230 and 290 <= mouse_pos[1] <= 290 + 40 and self.state != "touring":
                    self.warnsdorff = False
                elif 600 <= mouse_pos[0] <= 600 + 230 and 410 <= mouse_pos[1] <= 410 + 40 and self.state != "touring":
                    self.warnsdorff = True
                # Quit Button. Stops the game
                elif 600 <= mouse_pos[0] <= 600 + 230 and 530 <= mouse_pos[1] <= 530 + 40:
                    self.running = False

        # Display Start button and text
        if 600 <= mouse_pos[0] <= 600 + 230 and 50 <= mouse_pos[1] <= 50 + 40:
            pg.draw.rect(SCREEN, hover_button_color, start_button)
        else:
            pg.draw.rect(SCREEN, button_color, start_button)
        SCREEN.blit(start_text, (690, 50))
        # Display Reset button and text
        if 600 <= mouse_pos[0] <= 600 + 230 and 170 <= mouse_pos[1] <= 170 + 40:
            pg.draw.rect(SCREEN, hover_button_color, reset_button)
        else:
            pg.draw.rect(SCREEN, button_color, reset_button)
        SCREEN.blit(reset_text, (680, 170))
        if self.warnsdorff:
            # Display Backtrack button and text
            if 600 <= mouse_pos[0] <= 600 + 230 and 290 <= mouse_pos[1] <= 290 + 40:
                pg.draw.rect(SCREEN, hover_button_color, backtrack_button)
            else:
                pg.draw.rect(SCREEN, button_color, backtrack_button)
            SCREEN.blit(backtrack_text, (615, 290))
            # Remove Warnsdorff button
            pg.draw.rect(SCREEN, BACKGROUND_COLOUR, warnsdorff_button)
        else:
            # Display Warnsdorff button and text
            if 600 <= mouse_pos[0] <= 600 + 230 and 410 <= mouse_pos[1] <= 410 + 40:
                pg.draw.rect(SCREEN, hover_button_color, warnsdorff_button)
            else:
                pg.draw.rect(SCREEN, button_color, warnsdorff_button)
            SCREEN.blit(warnsdorff_text, (605, 410))
            # Remove Backtrack button
            pg.draw.rect(SCREEN, BACKGROUND_COLOUR, backtrack_button)
        # Quit button
        if 600 <= mouse_pos[0] <= 600 + 230 and 530 <= mouse_pos[1] <= 530 + 40:
            pg.draw.rect(SCREEN, hover_button_color, quit_button)
        else:
            pg.draw.rect(SCREEN, button_color, quit_button)
        SCREEN.blit(quit_text, (690, 530))

        pg.display.update()

    def draw_step_label(self, screen):
        for row in range(self.dimensions):
            for column in range(self.dimensions):
                if self.board[row][column] != -1:
                    square = ((column * SQ_SIZE) + OFFSET[0], (row * SQ_SIZE) + OFFSET[1])
                    # pg.draw.circle(screen, )
                    label = BUTTON_FONT.render(str(self.board[row][column]), True, (255, 0, 0))
                    screen.blit(label, (square[0] + 10, square[1] + 10))

    def is_valid_move(self, x, y):
        '''
            A utility function to check if i,j are valid indexes
            for N*N chessboard
        '''
        if 0 <= x < self.dimensions and 0 <= y < self.dimensions and self.board[x][y] == -1:
            return True
        return False

    def count_empty_squares(self, next_x, next_y):
        count = 0
        for i in range(8):
            if self.is_valid_move(next_x + self.knight_moves[i][0], next_y + self.knight_moves[i][1]):
                count += 1
        return count

    def find_tour(self):
        '''
            This function acts as the main component for finding tour, performs operations and is called .
        '''
        # First checks whether tour has already been found
        if not self.tour_found:
            if self.warnsdorff:
                if self.knight_step < 64:
                    self.find_tour_warnsdorff()
                else:
                    self.tour_found = True
                    self.running = False
            else:
                if len(self.move_log) == 0:
                    self.state = "fail"
                if self.knight_step < 64:
                    self.find_tour_backtrack_iterative()
                else:
                    self.tour_found = True
                    self.running = False

    def find_tour_warnsdorff(self):
        most_empty = 9
        most_empty_index = -1

        # To give some randomness when choosing a square. Only useful for next squares with the same number of next
        # valid squares
        random_num = random.randint(0, 1000) % 8
        for i in range(8):
            index = (random_num + i) % 8
            new_x = self.knight_pos[0] + self.knight_moves[index][0]
            new_y = self.knight_pos[1] + self.knight_moves[index][1]
            empty_sq_count = self.count_empty_squares(new_x, new_y)
            if self.is_valid_move(new_x, new_y) and empty_sq_count < most_empty:
                most_empty_index = index
                most_empty = empty_sq_count

        if most_empty_index == -1:
            self.state = "fail"
            return False

        new_x = self.knight_pos[0] + self.knight_moves[most_empty_index][0]
        new_y = self.knight_pos[1] + self.knight_moves[most_empty_index][1]
        self.knight_step += 1
        self.board[new_x][new_y] = self.knight_step
        self.knight_pos = (new_x, new_y)
        self.move_log.append((new_x, new_y))
        self.draw_knight(SCREEN)

    # def pick_square(self):
    #     # Maximum number of traversable squares is 8
    #     most_empty = 9
    #     most_empty_index = -1
    #
    #     # To give some randomness when choosing a square. Only useful for next squares with the same number of next
    #     # valid squares
    #     random_num = random.randint(0, 1000) % 8
    #     for i in range(self.dimensions):
    #         index = (random_num + i) % 8
    #         new_x = self.knight_pos[0] + self.knight_moves[index][0]
    #         new_y = self.knight_pos[1] + self.knight_moves[index][1]
    #         empty_count = self.count_empty_squares(new_x, new_y)
    #         if self.is_valid_move(new_x, new_y) and empty_count < most_empty:
    #             most_empty_index = index
    #             most_empty = empty_count
    #
    #     if most_empty_index == -1:
    #         print("No moves found")
    #         self.reset_board()
    #         return None
    #
    #     new_x = self.knight_pos[0] + self.knight_moves[most_empty_index][0]
    #     new_y = self.knight_pos[1] + self.knight_moves[most_empty_index][1]
    #
    #     self.knight_step += 1
    #     self.board[new_x][new_y] = self.knight_step
    #     self.knight_pos = (new_x, new_y)
    #     self.draw_knight(SCREEN)
    #
    #     return self.knight_pos

    def find_tour_backtrack_iterative(self):
        '''
        This function uses a non-recursive backtracking algorithm to solve the knight's tour. This is a brute force
        method which isn't practical as the time complexity is O(8**(N**2)).
        '''
        # move_log stores list of squares traversed by the knight
        # Each square contains (row, column, next index to use of knight_moves list)
        global movement
        movement += 1
        last_used_square = self.move_log[-1]
        contains_valid = False
        # Checks if the square has valid moves, if so, move to that new square
        for i in range(last_used_square[2], 8):
            new_x = last_used_square[0] + self.knight_moves[i][0]
            new_y = last_used_square[1] + self.knight_moves[i][1]
            if self.is_valid_move(new_x, new_y):
                self.move_log[-1] = (self.knight_pos[0], self.knight_pos[1], i + 1)
                self.knight_step += 1
                self.board[new_x][new_y] = self.knight_step
                self.knight_pos = (new_x, new_y)
                new_pos = (new_x, new_y, 0)
                self.move_log.append(new_pos)
                contains_valid = True
        # If no valid squares are present, remove square from stack
        if not contains_valid:
            self.board[self.knight_pos[0]][self.knight_pos[1]] = -1
            self.knight_step -= 1
            self.move_log.pop()
            self.knight_pos = (self.move_log[-1][0], self.move_log[-1][1])
        self.draw_knight(SCREEN)
        pg.display.update()

    # def find_tour_backtrack_iterative(self):
    #     '''
    #     This function uses a non-recursive backtracking algorithm to solve the knight's tour. This is a brute force
    #     method which isn't practical as the time complexity is O(8**(N**2)).
    #     :return: Boolean whether a solution was found
    #     '''
    #     # move_log stores list of squares traversed by the knight
    #     # Each square contains (row, column, last used index of knight_moves list)
    #     move_log = [(self.knight_pos[0], self.knight_pos[1], 0)]
    #     # movements = 0
    #     self.knight_step = 1
    #     while len(move_log) != 0 or self.knight_step < 64:
    #         # movements += 1
    #         contains_valid = False
    #         last_used_square = move_log[-1]
    #         for i in range(last_used_square[2], 8):
    #             new_x = last_used_square[0] + self.knight_moves[i][0]
    #             new_y = last_used_square[1] + self.knight_moves[i][1]
    #             if self.is_valid_move(new_x, new_y):
    #                 move_log[-1] = (self.knight_pos[0], self.knight_pos[1], i+1)
    #                 self.knight_step += 1
    #                 self.board[new_x][new_y] = self.knight_step
    #                 self.knight_pos = (new_x, new_y)
    #                 # print(self.knight_pos, self.knight_step)
    #                 new_pos = (new_x, new_y, 0)
    #                 move_log.append(new_pos)
    #                 contains_valid = True
    #                 if self.knight_step == 64:
    #                     print("Hit")
    #                     # print(movements)
    #                     return True
    #                 break
    #         if not contains_valid:
    #             self.board[self.knight_pos[0]][self.knight_pos[1]] = -1
    #             self.knight_step -= 1
    #             move_log.pop()
    #             # print("change")
    #             self.knight_pos = (move_log[-1][0], move_log[-1][1])
    #         #     print(self.knight_pos, self.knight_step)
    #         # print(self.board)
    #         # self.draw_game_state(SCREEN)
    #         # pygame.display.flip()
    #     return False

    def update_frame(self):
        if self.state == "touring":
            self.find_tour()
        if self.state == "fail":
            self.redo_tour()
            self.state = "touring"
        if not self.running:
            stop = timeit.default_timer()
            print('Time: ', stop - start)
            print(movement)
            pg.quit()
            sys.exit()
        self.check_event()
        pg.event.pump()


# Driver C

def main():
    chess_state = ChessState(DIMENSIONS)
    draw_board(SCREEN)
    while True:
        # clock.tick(FPS)
        chess_state.update_frame()


if __name__ == "__main__":
    # start = timeit.default_timer()
    # chess_state = ChessState(8)
    # chess_state.find_tour()
    start = timeit.default_timer()
    main()
    # stop = timeit.default_timer()
    # print('Time: ', stop - start)
