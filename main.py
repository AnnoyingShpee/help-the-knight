# Python3 program to solve Knight Tour problem using Backtracking or Warnsdorff
import sys
import pygame as pg
import numpy as np
import random
import json
import ctypes
from ctypes import windll
from datetime import datetime
import Components

pg.init()

# Colours
BACKGROUND_COLOUR = (180, 241, 255)
BUTTON_COLOUR = (100, 100, 100)  # Default button color
HOVER_BUTTON_COLOUR = (170, 170, 170)  # Color of button when cursor hovers over
BUTTON_TEXT_COLOUR = (255, 255, 255)
TEXT_COLOUR = (0, 0, 0)
# Colours for move stamps and lines
STAMP_COLOURS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (144, 142, 0)]  # Red, Green, Blue, Colour Blind
MOVE_COLOURS = [(0, 0, 0), (0, 0, 0), (255, 255, 255), (255, 255, 255)]

# Global variables for display
ctypes.windll.user32.SetProcessDPIAware()
true_res = (windll.user32.GetSystemMetrics(0),windll.user32.GetSystemMetrics(1))
SCREEN = pg.display.set_mode((0, 0), pg.FULLSCREEN)  # Set game window
SCREEN.fill(BACKGROUND_COLOUR)  # Set background color
x_axis, y_axis = SCREEN.get_size()
BOARD_SIZE = ((y_axis // 10) * 8, (y_axis // 10) * 8)  # Size of board
OFFSET = (y_axis // 15, y_axis // 15)  # Amount of offset of the board from the border
TITLE_FONT = pg.font.SysFont('Arial', 50, bold=True)  # Font for title
BUTTON_FONT = pg.font.SysFont('Arial', 35)  # Font for button text
TEXT_FONT = pg.font.SysFont('Arial', 30)  # Font for text below the board
BOLD_TEXT_FONT = pg.font.SysFont('Arial', 30, bold=True)

# Title
title_text = Components.Square((x_axis // 100) * 2, 0, (x_axis // 100) * 20, OFFSET[1], pg,
                               BACKGROUND_COLOUR, None, "Knight's Tour Finder", TEXT_COLOUR, TITLE_FONT)

# Start, Help, Colour, Reset, and Quit buttons and text in one area
# The buttons
start_button = Components.Square((x_axis // 100) * 90, (y_axis // 100) * 10, (x_axis // 100) * 10, y_axis // 20, pg,
                                 BUTTON_COLOUR, HOVER_BUTTON_COLOUR, "Start", BUTTON_TEXT_COLOUR, BUTTON_FONT)
help_button = Components.Square((x_axis // 100) * 90, (y_axis // 100) * 30, (x_axis // 100) * 10, y_axis // 20, pg,
                                BUTTON_COLOUR, HOVER_BUTTON_COLOUR, "Help", BUTTON_TEXT_COLOUR, BUTTON_FONT)
colour_button = Components.Square((x_axis // 100) * 90, (y_axis // 100) * 50, (x_axis // 100) * 10, y_axis // 20, pg,
                                  BUTTON_COLOUR, HOVER_BUTTON_COLOUR, "Green", BUTTON_TEXT_COLOUR, BUTTON_FONT)
reset_button = Components.Square((x_axis // 100) * 90, (y_axis // 100) * 70, (x_axis // 100) * 10, y_axis // 20, pg,
                                 BUTTON_COLOUR, HOVER_BUTTON_COLOUR, "Reset", BUTTON_TEXT_COLOUR, BUTTON_FONT)
quit_button = Components.Square((x_axis // 100) * 90, (y_axis // 100) * 90, (x_axis // 100) * 10, y_axis // 20, pg,
                                BUTTON_COLOUR, HOVER_BUTTON_COLOUR, "Quit", BUTTON_TEXT_COLOUR, BUTTON_FONT)
# The text "Colour" above Colour button
colour_text = Components.Square((x_axis // 100) * 90, colour_button.y_pos - (y_axis // 20), (x_axis // 100) * 10, y_axis // 20, pg,
                                BACKGROUND_COLOUR, None, "Colour", TEXT_COLOUR, TEXT_FONT)

# Tour Type, FPS, and Dimension buttons in another area
algorithms_button = Components.Square((x_axis // 100) * 55, (y_axis // 100) * 10,
                                      (x_axis // 10) * 2, (y_axis // 100) * 10,
                                      pg, BUTTON_COLOUR, HOVER_BUTTON_COLOUR,
                                      "Algorithms", BUTTON_TEXT_COLOUR, BUTTON_FONT)
algorithms_type_button = Components.Square(algorithms_button.x_pos, algorithms_button.y_pos + algorithms_button.height,
                                           algorithms_button.width, algorithms_button.height,
                                           pg, BUTTON_COLOUR, HOVER_BUTTON_COLOUR,
                                           "[Backtrack]", BUTTON_TEXT_COLOUR, BUTTON_FONT)
# Buttons to select Tour Type
backtrack_button = Components.Square(algorithms_button.x_pos, algorithms_button.y_pos,
                                     algorithms_button.width, y_axis // 20,
                                     pg, BUTTON_COLOUR, HOVER_BUTTON_COLOUR,
                                     "Backtrack Method", BUTTON_TEXT_COLOUR, BUTTON_FONT)
warnsdorff_button = Components.Square(algorithms_button.x_pos, algorithms_type_button.y_pos+algorithms_type_button.height-(y_axis // 20),
                                      algorithms_button.width, y_axis // 20,
                                      pg, BUTTON_COLOUR, HOVER_BUTTON_COLOUR,
                                      "Warnsdoff's Method", BUTTON_TEXT_COLOUR, BUTTON_FONT)
# Area to display row number text
row_text = Components.Square(algorithms_button.x_pos, (y_axis // 100) * 45,
                             algorithms_button.width, y_axis // 20,
                             pg, BACKGROUND_COLOUR, None,
                             "Rows: 8", TEXT_COLOUR, TEXT_FONT)
# Area to display column number text
col_text = Components.Square(algorithms_button.x_pos, (y_axis // 100) * 60,
                             algorithms_button.width, y_axis // 20,
                             pg, BACKGROUND_COLOUR, None,
                             "Columns: 8", TEXT_COLOUR, TEXT_FONT)
# Area to display FPS text
fps_text = Components.Square(algorithms_button.x_pos, (y_axis // 100) * 75,
                             algorithms_button.width, y_axis // 20,
                             pg, BACKGROUND_COLOUR, None,
                             "FPS: 30", TEXT_COLOUR, TEXT_FONT)
# Buttons to decrease/increase number of rows
row_down_button = Components.Square(row_text.x_pos, row_text.y_pos,  # Position on screen
                                    row_text.width // 5, row_text.height,  # Width and height
                                    pg, BUTTON_COLOUR, HOVER_BUTTON_COLOUR,  # Button Colours
                                    "-1", BUTTON_TEXT_COLOUR, BUTTON_FONT)  # Text colour
row_up_button = Components.Square(row_text.x_pos + row_text.width - row_down_button.width, row_text.y_pos,
                                  row_down_button.width, row_down_button.height,
                                  pg, BUTTON_COLOUR, HOVER_BUTTON_COLOUR,
                                  "+1", BUTTON_TEXT_COLOUR, BUTTON_FONT)
# Buttons to decrease/increase number of columns
col_down_button = Components.Square(col_text.x_pos, col_text.y_pos,
                                    col_text.width // 5, col_text.height,
                                    pg, BUTTON_COLOUR, HOVER_BUTTON_COLOUR,
                                    "-1", BUTTON_TEXT_COLOUR, BUTTON_FONT)
col_up_button = Components.Square(col_text.x_pos + col_text.width - col_down_button.width, col_text.y_pos,
                                  col_down_button.width, col_down_button.height,
                                  pg, BUTTON_COLOUR, HOVER_BUTTON_COLOUR,
                                  "+1", BUTTON_TEXT_COLOUR, BUTTON_FONT)
# Buttons to decrease/increase FPS
fps_down_button = Components.Square(fps_text.x_pos, fps_text.y_pos,
                                    fps_text.width // 5, fps_text.height,
                                    pg, BUTTON_COLOUR, HOVER_BUTTON_COLOUR,
                                    "-5", BUTTON_TEXT_COLOUR, BUTTON_FONT)
fps_up_button = Components.Square(fps_text.x_pos + fps_text.width - fps_down_button.width, fps_text.y_pos,
                                  fps_down_button.width, fps_down_button.height,
                                  pg, BUTTON_COLOUR, HOVER_BUTTON_COLOUR,
                                  "+10", BUTTON_TEXT_COLOUR, BUTTON_FONT)

# Button to load save file
load_button = Components.Square(algorithms_button.x_pos, (y_axis // 100) * 90,
                                algorithms_button.width, y_axis // 20,
                                pg, BUTTON_COLOUR, HOVER_BUTTON_COLOUR,
                                "Load Tour", BUTTON_TEXT_COLOUR, BUTTON_FONT)
# Button to save knight's tour
save_button = Components.Square(load_button.x_pos, load_button.y_pos,
                                load_button.width, load_button.height,
                                pg, BUTTON_COLOUR, HOVER_BUTTON_COLOUR,
                                "Save Tour", BUTTON_TEXT_COLOUR, BUTTON_FONT)

# Game text under the chessboard
under_board_text = Components.Square(OFFSET[0], OFFSET[1] + BOARD_SIZE[1],
                                     BOARD_SIZE[0], 1.5 * BOARD_SIZE[1] // 8,
                                     pg, BACKGROUND_COLOUR, None, "", TEXT_COLOUR, TEXT_FONT)

# Area to display "Help"
component_title_text = "Board & Components"
usage_title_text = "How To Use"
save_load_title_text = "Saving and Loading tours"
f = open("help_components.txt", "r")
component_desc_text = f.read()
f.close()
f = open("help_how_to_use.txt", "r")
usage_desc_text = f.read()
f.close()
f = open("help_save_load.txt", "r")
save_load_desc_text = f.read()
f.close()
help_display_area = Components.Square((x_axis // 100) * 5, (y_axis // 100) * 5,
                                      (x_axis // 100) * 92, (y_axis // 100) * 95,
                                      pg, (0, 0, 0))
help_title_area = Components.Square(help_display_area.x_pos, help_display_area.y_pos,
                                    help_display_area.width, help_display_area.height // 10,
                                    pg, (0, 0, 0), None,
                                    "Help", (255, 255, 255), BOLD_TEXT_FONT)
help_exit_button = Components.Square(help_title_area.x_pos+help_title_area.width-(help_title_area.width // 20), help_title_area.y_pos,
                                     help_title_area.width // 20, help_title_area.height,
                                     pg, (0, 0, 0), HOVER_BUTTON_COLOUR,
                                     "X", (255, 255, 255), TEXT_FONT)
help_page_num_area = Components.Square(help_display_area.x_pos, help_display_area.y_pos+help_display_area.height-(help_display_area.height//10),
                                       help_display_area.width, help_display_area.height // 10,
                                       pg, (0, 0, 0), None,
                                       "Page 1/3", (255, 255, 255), TEXT_FONT)
help_prev_page_button = Components.Square(help_page_num_area.x_pos, help_page_num_area.y_pos,
                                          help_page_num_area.width // 20, help_page_num_area.height,
                                          pg, (0, 0, 0), HOVER_BUTTON_COLOUR,
                                          "<", (255, 255, 255), TEXT_FONT)
help_next_page_button = Components.Square(help_page_num_area.x_pos+help_page_num_area.width-(help_page_num_area.width // 20), help_page_num_area.y_pos,
                                          help_page_num_area.width // 20, help_page_num_area.height,
                                          pg, (0, 0, 0), HOVER_BUTTON_COLOUR,
                                          ">", (255, 255, 255), TEXT_FONT)
component_title_area = Components.Square(help_display_area.x_pos, help_title_area.y_pos+help_title_area.height,
                                         help_display_area.width, (y_axis // 100) * 5,
                                         pg, (0, 0, 0), None,
                                         component_title_text, (255, 255, 255), BOLD_TEXT_FONT)
component_desc_area = Components.Square(help_display_area.x_pos, component_title_area.y_pos+component_title_area.height,
                                        help_display_area.width, (y_axis // 100) * 40,
                                        pg, (0, 0, 0), None,
                                        component_desc_text, (255, 255, 255), TEXT_FONT)
usage_title_area = Components.Square(help_display_area.x_pos, help_title_area.y_pos+help_title_area.height,
                                     help_display_area.width, (y_axis // 100) * 5,
                                     pg, (0, 0, 0), None,
                                     usage_title_text, (255, 255, 255), BOLD_TEXT_FONT)
usage_desc_area = Components.Square(help_display_area.x_pos, usage_title_area.y_pos+usage_title_area.height,
                                    help_display_area.width, (y_axis // 100) * 45,
                                    pg, (0, 0, 0), None,
                                    usage_desc_text, (255, 255, 255), TEXT_FONT)
save_load_title_area = Components.Square(help_display_area.x_pos, help_title_area.y_pos+help_title_area.height,
                                         help_display_area.width, (y_axis // 100) * 5,
                                         pg, (0, 0, 0), None,
                                         save_load_title_text, (255, 255, 255), BOLD_TEXT_FONT)
save_load_desc_area = Components.Square(help_display_area.x_pos, save_load_title_area.y_pos+save_load_title_area.height,
                                        help_display_area.width, (y_axis // 100) * 50,
                                        pg, (0, 0, 0), None,
                                        save_load_desc_text, (255, 255, 255), TEXT_FONT)


def display_title():
    pg.draw.rect(SCREEN, title_text.colour, title_text.rect)
    SCREEN.blit(title_text.text_render, title_text.text_rect)


# https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame
def display_multiline_text(surface, text, pos, font, colour):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    word_width, word_height = 0, 0
    x_offset = 10
    x, y = pos[0] + x_offset, pos[1]
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, colour)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0] + x_offset  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space + x_offset
        x = pos[0] + x_offset  # Reset the x.
        y += word_height  # Start on new row.


def update_below_board_text(text, extra_text=None):
    """
    Used to update the text box below the board.
    :param text: The string to be displayed underneath the board
    :param extra_text: Extra info to be displayed below text
    :return:
    """
    global under_board_text
    under_board_line_1_text = TEXT_FONT.render(text, True, under_board_text.text_colour)
    under_board_line_1_text_rect = under_board_line_1_text.get_rect(
        center=(under_board_text.x_pos + (under_board_text.width // 2),
                under_board_text.y_pos + (under_board_text.height // 5))
    )
    pg.draw.rect(SCREEN, under_board_text.colour, under_board_text.rect)
    SCREEN.blit(under_board_line_1_text, under_board_line_1_text_rect)
    if extra_text is not None:
        under_board_line_2_text = TEXT_FONT.render(extra_text, True, under_board_text.text_colour)
        under_board_line_2_text_rect = under_board_line_2_text.get_rect(
            center=(under_board_text.x_pos + (under_board_text.width // 2),
                    under_board_text.y_pos + (under_board_text.height // 2))
        )
        SCREEN.blit(under_board_line_2_text, under_board_line_2_text_rect)


def serialize_ndarray(obj):
    """Used to convert ndarray objects to a list to be stored into JSON
    :param obj: Any object
    return A list
    """
    if isinstance(obj, np.ndarray):
        return obj.tolist()

    raise TypeError("Type %s is not serializable" % type(obj))


class Knight:
    def __init__(self):
        """
            Tuple of moves (x, y) that can be done by the knight. Tuple because it will not be changed in any way.
            x = horizontal movement. POSITIVE value moves knight to the RIGHT while NEGATIVE value moves it to the LEFT
            y = vertical movement. POSITIVE value moves knight DOWN while NEGATIVE value moves knight UP
        """
        self.knight_moves = ((2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1))
        self.knight_placed = False  # Whether a knight has been placed on the board
        self.knight_initial_pos = None  # The starting position of the knight of the tour sequence.
        self.knight_pos = None  # Current position of the Knight on the board.
        self.knight_step = 1  # Current step number of the Knight
        self.move_log = []  # Contains the squares traversed and next move to use
        self.possible_moves = []
        self.total_steps = 0  # Total number of moves the knight has made
        self.knight_img = pg.image.load("./img/knight_piece.png")  # Image of the Knight on the Board
        self.step_font = None


class Board:
    def __init__(self, row_dimension=8, col_dimension=8):
        self.knight = Knight() # Every board has a Knight
        self.board_size = BOARD_SIZE  # Size of board
        self.sq_colours = [pg.Color("white"), pg.Color("grey")]  # Colours of the board's squares
        self.row_dimension = row_dimension  # Number of rows of the board
        self.col_dimension = col_dimension  # Number of columns of the board
        # 2D array representation of board
        self.graph = np.negative(np.ones([row_dimension, col_dimension], dtype=int))
        # 2D array to store number of times Knight traversed each square
        self.board_moves = np.zeros([row_dimension, col_dimension], dtype=int)
        # Width and height of each square on the board
        self.sq_x_length = BOARD_SIZE[0] // col_dimension
        self.sq_y_length = BOARD_SIZE[1] // row_dimension
        # Fonts
        self.moves_font = pg.font.SysFont("Arial", self.sq_x_length // 4)
        self.knight.step_font = pg.font.SysFont("Arial", self.sq_x_length // 4)
        # Colour of stamps left by the Knight
        self.stamp_colour = ("red", STAMP_COLOURS[0], MOVE_COLOURS[0])
        self.knight.knight_img = pg.transform.scale(self.knight.knight_img,
                                                    ((self.sq_x_length // 10) * 8, (self.sq_y_length // 10) * 8))

    def draw_board(self):
        """
        Draws the chessboard. Every square is drawn one by one that alternates between one colour and another. A large
        square with the same colour as the background and the same size of the 8 x 8 board is drawn over the old board
        every time to display smaller boards.
        :return:
        """
        # Clean the board area with a large square
        pg.draw.rect(SCREEN, BACKGROUND_COLOUR, pg.Rect(OFFSET[0], OFFSET[1], BOARD_SIZE[0], BOARD_SIZE[1]))
        # Draw chessboard. Top left square is always light color
        for row in range(self.row_dimension):
            for col in range(self.col_dimension):
                # Draw square
                self.draw_square(row, col)

    def draw_knight(self):
        """
        Draws the Knight image on the board.
        :return:
        """
        # Draw knight image
        SCREEN.blit(self.knight.knight_img,
                    pg.Rect((self.knight.knight_pos[1] * self.sq_x_length) + OFFSET[0] + self.sq_x_length // 8,
                            (self.knight.knight_pos[0] * self.sq_y_length) + OFFSET[1] + self.sq_y_length // 8,
                            self.sq_x_length, self.sq_y_length)
                    )

    def check_dimensions_then_draw(self):
        """
        Checks the number of dimensions the board has to scale the dimensions of the squares. If the size of the board
        is smaller than 8 x 8, the size of the squares will not change, merely making the board smaller due to less
        rows or columns. If either dimensions are bigger than 8, the dimensions of the squares will be changed to fit
        all the squares in a 8-by-8-sized looking board.
        :return:
        """
        row = self.row_dimension
        col = self.col_dimension
        # Fixes the size of the board as an 8 x 8 board if dimensions are more than 8
        if self.row_dimension > 8:
            row = 8
        if self.col_dimension > 8:
            col = 8
        # If there are fewer than 8 rows or columns, the board size decreases
        self.board_size = ((y_axis // 10) * col, (y_axis // 10) * row)
        # Scale the square size based on board size and number of rows and columns of the board
        self.sq_x_length = self.board_size[0] // self.col_dimension
        self.sq_y_length = self.board_size[1] // self.row_dimension
        if self.sq_x_length < self.sq_y_length:
            self.knight.step_font = pg.font.SysFont("Arial", self.sq_x_length // 4)
            self.moves_font = pg.font.SysFont("Arial", self.sq_x_length // 4)
        else:
            self.knight.step_font = pg.font.SysFont("Arial", self.sq_y_length // 4)
            self.moves_font = pg.font.SysFont("Arial", self.sq_y_length // 4)
        self.knight.knight_img = pg.image.load("./img/knight_piece.png")
        # Scale dimensions of knight image with board's squares' dimensions
        self.knight.knight_img = pg.transform.scale(self.knight.knight_img,
                                                    ((self.sq_x_length // 10) * 8, (self.sq_y_length // 10) * 8))
        self.draw_board()

    def decrease_row(self):
        """
        Decreases number of rows of board by 1 unless number of rows is less than or equal to 3.
        :return:
        """
        global row_text
        if self.row_dimension <= 3:
            return
        self.row_dimension -= 1
        # Reinitialise the board and board moves
        self.graph = np.negative(np.ones([self.row_dimension, self.col_dimension], dtype=int))
        self.board_moves = np.zeros([self.row_dimension, self.col_dimension], dtype=int)
        self.check_dimensions_then_draw()
        row_text.change_text(f"Rows: {self.row_dimension}")

    def increase_row(self):
        """
        Increases number of rows of board by 1 unless number of rows is greater than or equal to 20.
        :return:
        """
        global row_text
        if self.row_dimension >= 20:
            return
        self.row_dimension += 1
        # Reinitialise the board
        self.graph = np.negative(np.ones([self.row_dimension, self.col_dimension], dtype=int))
        self.board_moves = np.zeros([self.row_dimension, self.col_dimension], dtype=int)
        self.check_dimensions_then_draw()
        row_text.change_text(f"Rows: {self.row_dimension}")

    def decrease_col(self):
        """
        Decreases number of columns of board by 1 unless number of columns is less than or equal to 3.
        :return:
        """
        global col_text
        if self.col_dimension <= 3:
            return
        self.col_dimension -= 1
        # Reinitialise the board
        self.graph = np.negative(np.ones([self.row_dimension, self.col_dimension], dtype=int))
        self.board_moves = np.zeros([self.row_dimension, self.col_dimension], dtype=int)
        self.check_dimensions_then_draw()
        col_text.change_text(f"Columns: {self.col_dimension}")

    def increase_col(self):
        """
        Increases number of columns of board by 1 unless number of columns is greater than or equal to 20.
        :return:
        """
        global col_text
        if self.col_dimension >= 20:
            return
        self.col_dimension += 1
        # Reinitialise the board
        self.graph = np.negative(np.ones([self.row_dimension, self.col_dimension], dtype=int))
        self.board_moves = np.zeros([self.row_dimension, self.col_dimension], dtype=int)
        self.check_dimensions_then_draw()
        col_text.change_text(f"Columns: {self.col_dimension}")

    def draw_square(self, row, col):
        """
        Draws a square of the chessboard.
        :param row: Row number of the square on the board
        :param col: Column number of the square on the board
        """
        # Used to determine colour of square
        color = self.sq_colours[(row + col) % 2]
        # x-axis = Board columns (left to right) , y-axis = Board rows (top to bottom)
        # Draw the starting point of the square
        # Add off set if chessboard not touching the border of window
        pg.draw.rect(SCREEN, color, pg.Rect((col * self.sq_x_length) + OFFSET[0], (row * self.sq_y_length) + OFFSET[1],
                                            self.sq_x_length, self.sq_y_length))

    def draw_numbers(self):
        """
        Draws the numbers on the board. Both the step number of the Knight and the number of times the Knight moves to
        that square
        :return:
        """
        for row in range(self.row_dimension):
            for col in range(self.col_dimension):
                self.draw_knight_step(row, col)
                self.draw_move_number(row, col)

    def draw_knight_step(self, row, col):
        """
        Draws the stamp and step number made by the knight
        :param row: Current row number of Knight on board
        :param col: Current column number of Knight on board
        :return:None
        """
        # Get the highest number in the board, which is also the current step of the Knight.
        furthest_node = self.graph.max()
        # Draw stamp and step number on traversed squares that the Knight is currently not on AND for the last square
        # of a complete tour
        if (self.graph[row][col] != -1 and self.graph[row][col] != furthest_node) \
                or self.graph[row][col] == self.row_dimension * self.col_dimension:
            # Set position of stamp
            stamp = ((col * self.sq_x_length) + OFFSET[0] + self.sq_x_length // 2,
                     (row * self.sq_y_length) + OFFSET[1] + self.sq_y_length // 2)
            # Get step number value from board
            number = self.graph[row][col]
            # Draw the stamp circle
            if self.sq_x_length < self.sq_y_length:
                pg.draw.circle(SCREEN, self.stamp_colour[1], stamp, self.sq_x_length // 4)
            else:
                pg.draw.circle(SCREEN, self.stamp_colour[1], stamp, self.sq_y_length // 4)
            # Draw the number text on the stamp
            number_render = self.knight.step_font.render(f"{number}", True, self.stamp_colour[2])
            number_rect = number_render.get_rect(center=(col*self.sq_x_length + OFFSET[0] + self.sq_x_length // 2,
                                                         row*self.sq_y_length + OFFSET[1] + self.sq_y_length // 2))
            SCREEN.blit(number_render, number_rect)

    def draw_lines(self):
        """
        Draw lines between connecting squares.
        Since a line can only be drawn if there are 2 points to start and end from, move_log requires at least 2
        elements to draw lines.
        :return:
        """
        i = 2
        while i <= len(self.knight.move_log):
            start_point = self.knight.move_log[i - 2]
            line_start_point = ((start_point[1] * self.sq_x_length) + OFFSET[0] + self.sq_x_length // 2,
                                (start_point[0] * self.sq_y_length) + OFFSET[1] + self.sq_y_length // 2)
            end_point = self.knight.move_log[i - 1]
            line_end_point = ((end_point[1] * self.sq_x_length) + OFFSET[0] + self.sq_x_length // 2,
                              (end_point[0] * self.sq_y_length) + OFFSET[1] + self.sq_y_length // 2)
            pg.draw.line(SCREEN, self.stamp_colour[1], line_start_point, line_end_point, 5)
            i += 1

    def draw_move_number(self, row, col):
        """
        Draws the number of times a Knight has move to this square at the top left corner of the square
        :param row: Row number of the board
        :param col: Column number of the board
        :return:
        """
        number = self.board_moves[row][col]
        number_length = len(str(number))
        number_render = self.moves_font.render(f"{number}", True, (0, 0, 0))
        # Keeps the number in the top left corner as much as possible
        if number_length <= 3:
            number_rect = number_render.get_rect(
                center=(col * self.sq_x_length + OFFSET[0] + 2 * (self.sq_x_length // 10),
                        row * self.sq_y_length + OFFSET[1] + 2 * (self.sq_y_length // 10))
            )
        else:
            number_rect = number_render.get_rect(
                center=(col * self.sq_x_length + OFFSET[0] + (2+number_length-3) * (self.sq_x_length // 10),
                        row * self.sq_y_length + OFFSET[1] + 2 * (self.sq_y_length // 10))
            )
        SCREEN.blit(number_render, number_rect)


class HelpState:
    def __init__(self):
        self.curr_page = 1
        self.total_pages = 3
        self.numbered_tour_img = pg.image.load("./img/numbered_tour.png")

    def display_help_state_components(self, mouse_pos):
        """
        Draws the help pop-up
        :return:
        """
        # Displays Help text area
        pg.draw.rect(SCREEN, help_display_area.colour, help_display_area.rect)
        # Displays Help title
        pg.draw.rect(SCREEN, help_title_area.colour, help_title_area.rect)
        SCREEN.blit(help_title_area.text_render, help_title_area.text_rect)
        # Displays the exit button of the help section
        if help_exit_button.x_pos <= mouse_pos[0] <= help_exit_button.x_pos + help_exit_button.width and \
                help_exit_button.y_pos <= mouse_pos[1] <= help_exit_button.y_pos + help_exit_button.height:
            pg.draw.rect(SCREEN, help_exit_button.hover_colour, help_exit_button.rect)
        else:
            pg.draw.rect(SCREEN, help_exit_button.colour, help_exit_button.rect)
        # Displays "X" text of exit button
        SCREEN.blit(help_exit_button.text_render, help_exit_button.text_rect)
        # Displays current page
        if self.curr_page == 1:
            self.display_help_state_1()
        elif self.curr_page == 2:
            self.display_help_state_2()
        elif self.curr_page == 3:
            self.display_help_state_3()
        # Displays page number
        pg.draw.rect(SCREEN, help_page_num_area.colour, help_page_num_area.rect)
        SCREEN.blit(help_page_num_area.text_render, help_page_num_area.text_rect)
        # Displays previous page button
        if help_prev_page_button.x_pos <= mouse_pos[0] <= help_prev_page_button.x_pos+help_prev_page_button.width and \
                help_prev_page_button.y_pos <= mouse_pos[1] <= help_prev_page_button.y_pos+help_prev_page_button.height:
            pg.draw.rect(SCREEN, help_prev_page_button.hover_colour, help_prev_page_button.rect)
        else:
            pg.draw.rect(SCREEN, help_prev_page_button.colour, help_prev_page_button.rect)
        SCREEN.blit(help_prev_page_button.text_render, help_prev_page_button.text_rect)
        # Displays next page button
        if help_next_page_button.x_pos <= mouse_pos[0] <= help_next_page_button.x_pos + help_next_page_button.width and \
                help_next_page_button.y_pos <= mouse_pos[1] <= help_next_page_button.y_pos + help_next_page_button.height:
            pg.draw.rect(SCREEN, help_next_page_button.hover_colour, help_next_page_button.rect)
        else:
            pg.draw.rect(SCREEN, help_next_page_button.colour, help_next_page_button.rect)
        SCREEN.blit(help_next_page_button.text_render, help_next_page_button.text_rect)

    def display_help_state_1(self):
        # Displays "Board & Components" title
        pg.draw.rect(SCREEN, component_title_area.colour, component_title_area.rect)
        SCREEN.blit(component_title_area.text_render, component_title_area.text_rect)
        # Displays "Board & Components" description
        pg.draw.rect(SCREEN, component_desc_area.colour, component_desc_area.rect)
        display_multiline_text(SCREEN, component_desc_text, (component_desc_area.x_pos, component_desc_area.y_pos),
                               component_desc_area.text_font, component_desc_area.text_colour)

        # Displays image
        self.numbered_tour_img = pg.transform.scale(self.numbered_tour_img,
                                                    (component_desc_area.width // 10, component_desc_area.height // 2))
        SCREEN.blit(self.numbered_tour_img,
                    pg.Rect((component_desc_area.x_pos + (component_desc_area.width // 100) * 80),
                            component_desc_area.y_pos,
                            self.numbered_tour_img.get_width(), self.numbered_tour_img.get_height()))

    def display_help_state_2(self):
        # Displays "How To Use" title
        pg.draw.rect(SCREEN, usage_title_area.colour, usage_title_area.rect)
        SCREEN.blit(usage_title_area.text_render, usage_title_area.text_rect)
        # Displays "How To Use" description
        pg.draw.rect(SCREEN, usage_desc_area.colour, usage_desc_area.rect)
        display_multiline_text(SCREEN, usage_desc_text, (usage_desc_area.x_pos, usage_desc_area.y_pos),
                               usage_desc_area.text_font, usage_desc_area.text_colour)

    def display_help_state_3(self):
        # Displays saving and loading title
        pg.draw.rect(SCREEN, save_load_title_area.colour, save_load_title_area.rect)
        SCREEN.blit(save_load_title_area.text_render, save_load_title_area.text_rect)
        # Displays saving and loading description
        display_multiline_text(SCREEN, save_load_desc_text, (save_load_desc_area.x_pos, save_load_desc_area.y_pos),
                               save_load_desc_area.text_font, usage_desc_area.text_colour)


class GameState:
    def __init__(self):
        self.help_state = HelpState()
        # Initialise board array. Board is n x n matrix
        self.board = Board()
        # State of chessboard (start, ready, touring, finish, fail, pause, help)
        self.game_state = "start"
        # Algorithm selection button
        self.algorithm_selection = False
        # Used for counting how many times Warnsdorff fails to find a tour
        self.tour_failures = 0
        self.tour_found = False  # Whether knight tour is found
        self.running = True  # Whether game is running
        self.tour_type = "Backtrack"
        # Whether a step of a Knight's Tour has already been made and display has not been updated
        self.move_done = False
        self.fps = 30
        self.last_frame_tick = 0
        self.board.draw_board()
        self.time_start = datetime.now()
        self.duration = 0
        self.file_loaded = False
        # Display text underneath board
        update_below_board_text(f"{self.tour_type} Algorithm at {self.fps} Frames Per Second (FPS)")

    def reset_game(self):
        self.board.graph = np.negative(np.ones([8, 8], dtype=int))
        self.board.board_moves = np.zeros([8, 8], dtype=int)
        self.board.row_dimension = 8
        self.board.col_dimension = 8
        self.game_state = "start"
        self.algorithm_selection = False
        self.tour_failures = 0
        self.tour_found = False
        self.board.knight.knight_placed = False
        self.board.knight.knight_initial_pos = None
        self.board.knight.knight_pos = None
        self.board.knight.knight_step = 1
        self.board.knight.move_log = []
        self.board.knight.total_steps = 0
        self.board.knight.knight_img = pg.image.load("./img/knight_piece.png")
        self.board.knight.knight_img = pg.transform.scale(self.board.knight.knight_img,
                                                          ((self.board.sq_x_length // 10) * 8,
                                                           (self.board.sq_y_length // 10) * 8))
        self.board.knight.step_font = pg.font.SysFont("Arial", self.board.sq_x_length // 4)
        self.board.board_size = ((y_axis // 10) * 8, (y_axis // 10) * 8)  # Size of board
        self.board.sq_x_length = self.board.board_size[0] // 8
        self.board.sq_y_length = self.board.board_size[0] // 8
        self.time_start = 0.0
        self.duration = 0.0
        self.file_loaded = False
        SCREEN.fill(BACKGROUND_COLOUR)
        self.board.draw_board()
        row_text.change_text("Rows: 8")
        col_text.change_text("Columns: 8")
        start_button.change_text("Start")
        # Display text underneath board
        if self.fps > 60:
            update_below_board_text(f"{self.tour_type} Algorithm at Max Frames Per Second (FPS)")
        else:
            update_below_board_text(f"{self.tour_type} Algorithm at {self.fps} Frames Per Second (FPS)")

    def redo_tour(self):
        self.game_state = "touring"
        self.board.graph = np.negative(np.ones([self.board.row_dimension, self.board.col_dimension], dtype=int))
        self.board.graph[self.board.knight.knight_initial_pos[0]][self.board.knight.knight_initial_pos[1]] = 1
        self.board.knight.knight_step = 1
        self.board.knight.move_log = [
            (self.board.knight.knight_initial_pos[0], self.board.knight.knight_initial_pos[1], 0)]
        self.board.knight.knight_pos = self.board.knight.knight_initial_pos
        self.duration += (datetime.now() - self.time_start).total_seconds()
        self.time_start = datetime.now()
        SCREEN.fill(BACKGROUND_COLOUR)
        self.board.draw_board()
        update_below_board_text("Warnsdorff algorithm failed to find a tour.", f"Retrying No. {self.tour_failures}")

    def redraw_speed(self):
        if self.fps > 60:
            self.redraw_board()
        else:
            if (pg.time.get_ticks() - self.last_frame_tick) > 1000 / self.fps:
                self.redraw_board()

    def redraw_board(self):
        furthest_node = self.board.graph.max()
        # Draw current display of tour
        self.board.draw_board()
        self.board.draw_lines()
        self.board.draw_numbers()

        if furthest_node == self.board.row_dimension * self.board.col_dimension:
            self.board.draw_knight_step(self.board.knight.knight_pos[0], self.board.knight.knight_pos[1])
        else:
            SCREEN.blit(self.board.knight.knight_img,
                        pg.Rect((self.board.knight.knight_pos[1] * self.board.sq_x_length) +
                                OFFSET[0] + self.board.sq_x_length // 8,
                                (self.board.knight.knight_pos[0] * self.board.sq_y_length) +
                                OFFSET[1] + self.board.sq_y_length // 8,
                                self.board.sq_x_length, self.board.sq_y_length)
                        )
        pg.display.update()
        self.last_frame_tick = pg.time.get_ticks()
        self.move_done = False

    def increase_fps(self):
        if self.fps < 10:
            self.fps += 1
        elif self.fps < 30:
            self.fps += 5
        elif self.fps < 60:
            self.fps += 10
        elif self.fps < 70:
            self.fps += 10
        self.check_fps()

    def decrease_fps(self):
        if self.fps > 30:
            self.fps -= 10
        elif self.fps > 10:
            self.fps -= 5
        elif self.fps > 1:
            self.fps -= 1
        self.check_fps()

    def check_fps(self):
        global fps_down_button, fps_up_button, fps_text
        if self.fps == 30:
            fps_down_button.change_text("-5")
            fps_up_button.change_text("+10")
        elif self.fps == 10:
            fps_down_button.change_text("-1")
            fps_up_button.change_text("+5")
        elif 1 < self.fps < 10:
            fps_down_button.change_text("-1")
            fps_up_button.change_text("+1")
        elif 10 < self.fps < 30:
            fps_down_button.change_text("-5")
            fps_up_button.change_text("+5")
        elif 30 < self.fps < 60:
            fps_down_button.change_text("-10")
            fps_up_button.change_text("+10")
        if self.fps > 60:
            fps_text.change_text(f"FPS: MAX")
            fps_down_button.change_text("-10")
            fps_up_button.change_text("+10")
        else:
            fps_text.change_text(f"FPS: {self.fps}")

    def save_tour(self):
        save_file = "save_file.json"
        data = {
            "rows": self.board.row_dimension,
            "cols": self.board.col_dimension,
            "tour_type": self.tour_type,
            "board": self.board.graph,
            "moves": self.board.board_moves,
            "move_log": self.board.knight.move_log,
            "knight_initial_pos": self.board.knight.knight_initial_pos,
            "knight_pos": self.board.knight.knight_pos,
            "duration": self.duration,
            "knight_step": self.board.knight.knight_step,
            "total_steps": self.board.knight.total_steps,
            "fps": self.fps
        }
        json_string = json.dumps(data, default=serialize_ndarray)
        try:
            fo = open(save_file, "w")
            fo.write(json_string)
            fo.close()
            update_below_board_text("Tour saved successfully!")
        except (FileNotFoundError, PermissionError, OSError):
            update_below_board_text("There was a problem saving the tour.")

    def load_tour(self):
        save_file = "save_file.json"
        try:
            fj = open(save_file, "r")
            data = json.load(fj)
            self.board.row_dimension = data["rows"]
            self.board.col_dimension = data["cols"]
            self.tour_type = data["tour_type"]
            self.board.graph = np.asarray(data["board"])
            self.board.board_moves = np.asarray(data["moves"])
            self.board.knight.move_log = data["move_log"]
            self.board.knight.knight_initial_pos = data["knight_initial_pos"]
            self.board.knight.knight_pos = data["knight_pos"]
            self.duration = data["duration"]
            self.board.knight.knight_step = data["knight_step"]
            self.board.knight.total_steps = data["total_steps"]
            self.fps = data["fps"]
            fj.close()
            self.game_state = "pause"
            start_button.change_text("Resume")
            self.file_loaded = True
            algorithms_type_button.change_text(f"[{self.tour_type}]")
            row_text.change_text(f"Rows: {self.board.row_dimension}")
            col_text.change_text(f"Columns: {self.board.col_dimension}")
            if self.fps > 60:
                fps_text.change_text("FPS: MAX")
                update_below_board_text("Tour loaded", f"{self.tour_type} algorithm at Max Frames Per Second (FPS)")
            else:
                fps_text.change_text(f"FPS: {self.fps}")
                update_below_board_text("Tour loaded", f"{self.tour_type} algorithm at {self.fps} Frames Per Second (FPS)")
            self.check_fps()
            self.display_start_state_components(pg.mouse.get_pos())
            self.redraw_board()
        except FileNotFoundError as fe:
            update_below_board_text("No save file detected to load tour.")

    # Checks if user selected the same square twice. If so, remove the knight
    def place_first_knight(self, selected_sq):
        if not (self.game_state == "start" or self.game_state == "ready") or self.file_loaded:
            return
        row = selected_sq[0]
        col = selected_sq[1]
        # If user selected square where knight is already on, remove the knight
        if selected_sq == self.board.knight.knight_pos:
            self.board.draw_square(self.board.knight.knight_pos[0], self.board.knight.knight_pos[1])
            self.board.graph[row][col] = -1
            self.board.board_moves[row][col] = 0
            self.board.knight.knight_placed = False
            self.board.knight.knight_pos = None
            self.board.knight.knight_initial_pos = None
            self.game_state = "start"
            self.board.knight.move_log.pop()
        # If no knight is placed, place the knight
        elif not self.board.knight.knight_placed:
            self.board.knight.knight_placed = True
            self.board.knight.knight_pos = (row, col)
            self.board.knight.knight_initial_pos = (row, col)
            self.board.graph[row][col] = 1
            self.board.board_moves[row][col] = 1
            self.game_state = "ready"
            self.board.draw_knight()
            self.board.knight.move_log.append((row, col, 0))
        # If knight is place and user clicks on a different square, place knight in the new square
        elif self.board.knight.knight_placed:
            self.board.knight.move_log.pop()
            self.board.graph[self.board.knight.knight_pos[0]][self.board.knight.knight_pos[1]] = -1
            self.board.board_moves[self.board.knight.knight_pos[0]][self.board.knight.knight_pos[1]] = 0
            self.board.draw_square(self.board.knight.knight_pos[0], self.board.knight.knight_pos[1])
            self.board.knight.knight_pos = (row, col)
            self.board.knight.knight_initial_pos = (row, col)
            self.board.graph[row][col] = 1
            self.board.board_moves[row][col] = 1
            self.board.knight.move_log.append((row, col, 0))
            self.board.draw_knight()

    def display_components(self):
        mouse_pos = pg.mouse.get_pos()
        # self.display_main_buttons(mouse_pos)
        if self.game_state != "help":
            self.display_main_buttons(mouse_pos)
            if self.game_state == "start":
                self.display_start_state_components(mouse_pos)
            elif self.game_state == "pause":
                self.display_pause_state_components(mouse_pos)
        else:
            self.help_state.display_help_state_components(mouse_pos)
        self.check_events(mouse_pos)
        pg.display.update()

    def display_main_buttons(self, mouse_pos):
        """
        Draws the main buttons that will not be removed.
        :return:
        """
        # Display Start/Pause button
        if start_button.x_pos <= mouse_pos[0] <= start_button.x_pos + start_button.width \
                and start_button.y_pos <= mouse_pos[1] <= start_button.y_pos + start_button.height:
            pg.draw.rect(SCREEN, start_button.hover_colour, start_button.rect)
        else:
            pg.draw.rect(SCREEN, start_button.colour, start_button.rect)
        # Display Start/Pause button text
        SCREEN.blit(start_button.text_render, start_button.text_rect)
        # Display Help button
        if (self.game_state == "start" or self.game_state == "ready") and \
                help_button.x_pos <= mouse_pos[0] <= help_button.x_pos + help_button.width and \
                help_button.y_pos <= mouse_pos[1] <= help_button.y_pos + help_button.height:
            pg.draw.rect(SCREEN, help_button.hover_colour, help_button.rect)
        else:
            pg.draw.rect(SCREEN, help_button.colour, help_button.rect)
        # Display Help button text
        SCREEN.blit(help_button.text_render, help_button.text_rect)
        # Display Colour text
        pg.draw.rect(SCREEN, colour_text.colour, colour_text.rect)
        SCREEN.blit(colour_text.text_render, colour_text.text_rect)
        # Display Colour button
        if colour_button.x_pos <= mouse_pos[0] <= colour_button.x_pos + colour_button.width and \
                colour_button.y_pos <= mouse_pos[1] <= colour_button.y_pos + colour_button.height:
            pg.draw.rect(SCREEN, colour_button.hover_colour, colour_button.rect)
        else:
            pg.draw.rect(SCREEN, colour_button.colour, colour_button.rect)
        # Display Colour button text
        SCREEN.blit(colour_button.text_render, colour_button.text_rect)
        # Display Reset button
        if reset_button.x_pos <= mouse_pos[0] <= reset_button.x_pos + reset_button.width \
                and reset_button.y_pos <= mouse_pos[1] <= reset_button.y_pos + reset_button.height:
            pg.draw.rect(SCREEN, reset_button.hover_colour, reset_button.rect)
        else:
            pg.draw.rect(SCREEN, reset_button.colour, reset_button.rect)
        # Display Reset button text
        SCREEN.blit(reset_button.text_render, reset_button.text_rect)
        # Display Quit button
        if quit_button.x_pos <= mouse_pos[0] <= quit_button.x_pos + quit_button.width \
                and quit_button.y_pos <= mouse_pos[1] <= quit_button.y_pos + quit_button.height:
            pg.draw.rect(SCREEN, quit_button.hover_colour, quit_button.rect)
        else:
            pg.draw.rect(SCREEN, quit_button.colour, quit_button.rect)
        # Display Quit button text
        SCREEN.blit(quit_button.text_render, quit_button.text_rect)
        # Display Algorithms button or the Algorithm selection buttons
        # Reset the area of Algorithms to redraw
        pg.draw.rect(SCREEN, BACKGROUND_COLOUR, algorithms_button.rect)
        pg.draw.rect(SCREEN, BACKGROUND_COLOUR, algorithms_type_button.rect)
        if self.algorithm_selection:
            # Display Backtrack button
            if backtrack_button.x_pos <= mouse_pos[0] <= backtrack_button.x_pos + backtrack_button.width and \
                    backtrack_button.y_pos <= mouse_pos[1] <= backtrack_button.y_pos + backtrack_button.height:
                pg.draw.rect(SCREEN, backtrack_button.hover_colour, backtrack_button.rect)
            else:
                pg.draw.rect(SCREEN, backtrack_button.colour, backtrack_button.rect)
            SCREEN.blit(backtrack_button.text_render, backtrack_button.text_rect)
            # Display Warnsdorff button
            if warnsdorff_button.x_pos <= mouse_pos[0] <= warnsdorff_button.x_pos + warnsdorff_button.width and \
                    warnsdorff_button.y_pos <= mouse_pos[1] <= warnsdorff_button.y_pos + warnsdorff_button.height:
                pg.draw.rect(SCREEN, warnsdorff_button.hover_colour, warnsdorff_button.rect)
            else:
                pg.draw.rect(SCREEN, warnsdorff_button.colour, warnsdorff_button.rect)
            SCREEN.blit(warnsdorff_button.text_render, warnsdorff_button.text_rect)
        else:
            # Display Algorithm button
            if (self.game_state == "start" or self.game_state == "ready") and \
                    algorithms_button.x_pos <= mouse_pos[0] <= algorithms_button.x_pos + algorithms_button.width and \
                    algorithms_button.y_pos <= mouse_pos[1] <= algorithms_type_button.y_pos + algorithms_type_button.height:
                pg.draw.rect(SCREEN, algorithms_button.hover_colour, algorithms_button.rect)
                pg.draw.rect(SCREEN, algorithms_type_button.hover_colour, algorithms_type_button.rect)
            else:
                pg.draw.rect(SCREEN, algorithms_button.colour, algorithms_button.rect)
                pg.draw.rect(SCREEN, algorithms_type_button.colour, algorithms_type_button.rect)
            SCREEN.blit(algorithms_button.text_render, algorithms_button.text_rect)
            SCREEN.blit(algorithms_type_button.text_render, algorithms_type_button.text_rect)
        # Display FPS text
        pg.draw.rect(SCREEN, fps_text.colour, fps_text.rect)
        SCREEN.blit(fps_text.text_render, fps_text.text_rect)
        # Display fps decrease button
        if fps_down_button.x_pos <= mouse_pos[0] <= fps_down_button.x_pos + fps_down_button.width \
                and fps_down_button.y_pos <= mouse_pos[1] <= fps_down_button.y_pos + fps_down_button.height \
                and not self.tour_found:
            pg.draw.rect(SCREEN, fps_down_button.hover_colour, fps_down_button.rect)
        else:
            pg.draw.rect(SCREEN, fps_down_button.colour, fps_down_button.rect)
        SCREEN.blit(fps_down_button.text_render, fps_down_button.text_rect)
        # Display fps increase button
        if fps_up_button.x_pos <= mouse_pos[0] <= fps_up_button.x_pos + fps_up_button.width \
                and fps_up_button.y_pos <= mouse_pos[1] <= fps_up_button.y_pos + fps_up_button.height \
                and not self.tour_found:
            pg.draw.rect(SCREEN, fps_up_button.hover_colour, fps_up_button.rect)
        else:
            pg.draw.rect(SCREEN, fps_up_button.colour, fps_up_button.rect)
        SCREEN.blit(fps_up_button.text_render, fps_up_button.text_rect)
        # Hide Load File button
        pg.draw.rect(SCREEN, BACKGROUND_COLOUR, load_button.rect)

    def display_start_state_components(self, mouse_pos):
        # Display row text
        pg.draw.rect(SCREEN, row_text.colour, row_text.rect)
        SCREEN.blit(row_text.text_render, row_text.text_rect)
        # Display row decrease button
        if (self.game_state == "start" or self.game_state == "ready") and \
                row_down_button.x_pos <= mouse_pos[0] <= row_down_button.x_pos + row_down_button.width and \
                row_down_button.y_pos <= mouse_pos[1] <= row_down_button.y_pos + row_down_button.height:
            pg.draw.rect(SCREEN, row_down_button.hover_colour, row_down_button.rect)
        else:
            pg.draw.rect(SCREEN, row_down_button.colour, row_down_button.rect)
        SCREEN.blit(row_down_button.text_render, row_down_button.text_rect)
        # Display row increase button
        if (self.game_state == "start" or self.game_state == "ready") and \
                row_up_button.x_pos <= mouse_pos[0] <= row_up_button.x_pos + row_up_button.width and \
                row_up_button.y_pos <= mouse_pos[1] <= row_up_button.y_pos + row_up_button.height:
            pg.draw.rect(SCREEN, row_up_button.hover_colour, row_up_button.rect)
        else:
            pg.draw.rect(SCREEN, row_up_button.colour, row_up_button.rect)
        SCREEN.blit(row_up_button.text_render, row_up_button.text_rect)
        # Display column text
        pg.draw.rect(SCREEN, col_text.colour, col_text.rect)
        SCREEN.blit(col_text.text_render, col_text.text_rect)
        # Display column decrease button
        if (self.game_state == "start" or self.game_state == "ready") and \
                col_down_button.x_pos <= mouse_pos[0] <= col_down_button.x_pos + col_down_button.width and \
                col_down_button.y_pos <= mouse_pos[1] <= col_down_button.y_pos + col_down_button.height:
            pg.draw.rect(SCREEN, col_down_button.hover_colour, col_down_button.rect)
        else:
            pg.draw.rect(SCREEN, col_down_button.colour, col_down_button.rect)
        SCREEN.blit(col_down_button.text_render, col_down_button.text_rect)
        # Display column increase button
        if (self.game_state == "start" or self.game_state == "ready") and \
                col_up_button.x_pos <= mouse_pos[0] <= col_up_button.x_pos + col_up_button.width and \
                col_up_button.y_pos <= mouse_pos[1] <= col_up_button.y_pos + col_up_button.height:
            pg.draw.rect(SCREEN, col_up_button.hover_colour, col_up_button.rect)
        else:
            pg.draw.rect(SCREEN, col_up_button.colour, col_up_button.rect)
        SCREEN.blit(col_up_button.text_render, col_up_button.text_rect)
        # Display Load File button
        if load_button.x_pos <= mouse_pos[0] <= load_button.x_pos + load_button.width \
                and load_button.y_pos <= mouse_pos[1] <= load_button.y_pos + load_button.height:
            pg.draw.rect(SCREEN, load_button.hover_colour, load_button.rect)
        else:
            pg.draw.rect(SCREEN, load_button.colour, load_button.rect)
        SCREEN.blit(load_button.text_render, load_button.text_rect)

    def display_pause_state_components(self, mouse_pos):
        if save_button.x_pos <= mouse_pos[0] <= save_button.x_pos + save_button.width \
                and save_button.y_pos <= mouse_pos[1] <= save_button.y_pos + save_button.height:
            pg.draw.rect(SCREEN, save_button.hover_colour, save_button.rect)
        else:
            pg.draw.rect(SCREEN, save_button.colour, save_button.rect)
        SCREEN.blit(save_button.text_render, save_button.text_rect)

    def check_events(self, mouse_pos):
        """
        Checks for keyboard and mouse inputs
        :param mouse_pos:
        :return:
        """
        for event in pg.event.get():
            # Checks if the ESC key is press. If True, exit the application.
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.game_state != "help":
                    self.check_main_event(mouse_pos)
                    if self.game_state == "start":
                        self.check_start_state_event(mouse_pos)
                    elif self.game_state == "ready":
                        self.check_ready_state_event(mouse_pos)
                    elif self.game_state == "touring":
                        self.check_touring_state_event(mouse_pos)
                    elif self.game_state == "pause":
                        self.check_pause_state_event(mouse_pos)
                else:
                    self.check_help_state_event(mouse_pos)

    def check_main_event(self, mouse_pos):
        """
        Checks the mouse click events
        :param mouse_pos: Position of mouse. [x, y]
        :return:
        """
        # Checks if mouse click is on a component
        # On board area
        if OFFSET[0] <= mouse_pos[0] <= OFFSET[0] + self.board.board_size[0] and \
                OFFSET[1] <= mouse_pos[1] <= OFFSET[1] + self.board.board_size[1]:
            row = (mouse_pos[1] - OFFSET[1]) // self.board.sq_y_length
            col = (mouse_pos[0] - OFFSET[0]) // self.board.sq_x_length
            sq_selected = (row, col)
            self.place_first_knight(sq_selected)
        # On Help Button. Displays the text on how to use the application.
        elif self.game_state != "touring" and self.game_state != "pause" and \
                help_button.x_pos <= mouse_pos[0] <= help_button.x_pos + help_button.width and \
                help_button.y_pos <= mouse_pos[1] <= help_button.y_pos + help_button.height:
            self.game_state = "help"
        # On Colour Button.
        elif colour_button.x_pos <= mouse_pos[0] <= colour_button.x_pos + colour_button.width and \
                colour_button.y_pos <= mouse_pos[1] <= colour_button.y_pos + colour_button.height:
            if self.board.stamp_colour[0] == "red":
                self.board.stamp_colour = ("green", STAMP_COLOURS[1], MOVE_COLOURS[1])
                colour_button.change_text("Blue")
            elif self.board.stamp_colour[0] == "green":
                self.board.stamp_colour = ("blue", STAMP_COLOURS[2], MOVE_COLOURS[2])
                colour_button.change_text("Colour Blind")
            elif self.board.stamp_colour[0] == "blue":
                self.board.stamp_colour = ("colour blind", STAMP_COLOURS[3], MOVE_COLOURS[3])
                colour_button.change_text("Red")
            elif self.board.stamp_colour[0] == "colour blind":
                self.board.stamp_colour = ("red", STAMP_COLOURS[0], MOVE_COLOURS[0])
                colour_button.change_text("Green")
            if self.tour_found:
                self.board.draw_board()
                self.board.draw_lines()
                self.board.draw_numbers()
        # On Reset Button. Resets the board
        elif reset_button.x_pos <= mouse_pos[0] <= reset_button.x_pos + reset_button.width \
                and reset_button.y_pos <= mouse_pos[1] <= reset_button.y_pos + reset_button.height:
            self.reset_game()
        # Quit Button. Stops the game
        elif quit_button.x_pos <= mouse_pos[0] <= quit_button.x_pos + quit_button.width \
                and quit_button.y_pos <= mouse_pos[1] <= quit_button.y_pos + quit_button.height:
            self.running = False
        # On Algorithms button.
        elif algorithms_button.x_pos <= mouse_pos[0] <= algorithms_button.x_pos + algorithms_button.width \
                and algorithms_button.y_pos <= mouse_pos[1] <= algorithms_type_button.y_pos + algorithms_type_button.height \
                and (self.game_state == "start" or self.game_state == "ready") and not self.algorithm_selection:
            self.algorithm_selection = True
        # On Backtrack Button. Change the tour finding method to backtracking
        elif backtrack_button.x_pos <= mouse_pos[0] <= backtrack_button.x_pos + backtrack_button.width \
                and backtrack_button.y_pos <= mouse_pos[1] <= backtrack_button.y_pos + backtrack_button.height \
                and (self.game_state == "start" or self.game_state == "ready") and self.algorithm_selection:
            self.tour_type = "Backtrack"
            self.algorithm_selection = False
            algorithms_type_button.change_text(f"[{self.tour_type}]")
            # Display text underneath board
            if self.fps > 60:
                update_below_board_text(f"{self.tour_type} Algorithm at Max Frames Per Second (FPS)")
            else:
                update_below_board_text(f"{self.tour_type} Algorithm at {self.fps} Frames Per Second (FPS)")
        # On Warnsdorff Button. Change the tour finding method to Warnsdorff
        elif warnsdorff_button.x_pos <= mouse_pos[0] <= warnsdorff_button.x_pos + warnsdorff_button.width \
                and warnsdorff_button.y_pos <= mouse_pos[1] <= warnsdorff_button.y_pos + warnsdorff_button.height \
                and (self.game_state == "start" or self.game_state == "ready") and self.algorithm_selection:
            self.tour_type = "Warnsdorff"
            self.algorithm_selection = False
            algorithms_type_button.change_text(f"[{self.tour_type}]")
            # Display text underneath board
            if self.fps > 60:
                update_below_board_text(f"{self.tour_type} Algorithm at Max Frames Per Second (FPS)")
            else:
                update_below_board_text(f"{self.tour_type} Algorithm at {self.fps} Frames Per Second (FPS)")
        # On decrease FPS button.
        elif fps_down_button.x_pos <= mouse_pos[0] <= fps_down_button.x_pos + fps_down_button.width \
                and fps_down_button.y_pos <= mouse_pos[1] <= fps_down_button.y_pos + fps_down_button.height \
                and not self.tour_found:
            self.decrease_fps()
            # Display text underneath board
            if self.fps > 60:
                update_below_board_text(f"{self.tour_type} Algorithm at Max Frames Per Second (FPS)")
            else:
                update_below_board_text(f"{self.tour_type} Algorithm at {self.fps} Frames Per Second (FPS)")
        # On increase FPS button.
        elif fps_up_button.x_pos <= mouse_pos[0] <= fps_up_button.x_pos + fps_up_button.width \
                and fps_down_button.y_pos <= mouse_pos[1] <= fps_up_button.y_pos + fps_up_button.height \
                and not self.tour_found:
            self.increase_fps()
            # Display text underneath board
            if self.fps > 60:
                update_below_board_text(f"{self.tour_type} Algorithm at Max Frames Per Second (FPS)")
            else:
                update_below_board_text(f"{self.tour_type} Algorithm at {self.fps} Frames Per Second (FPS)")

    def check_start_state_event(self, mouse_pos):
        # On decrease row button.
        if row_down_button.x_pos <= mouse_pos[0] <= row_down_button.x_pos + row_down_button.width \
                and row_down_button.y_pos <= mouse_pos[1] <= row_down_button.y_pos + row_down_button.height:
            self.board.decrease_row()
        # On increase row button.
        elif row_up_button.x_pos <= mouse_pos[0] <= row_up_button.x_pos + row_up_button.width \
                and row_up_button.y_pos <= mouse_pos[1] <= row_up_button.y_pos + row_up_button.height:
            self.board.increase_row()
        # On decrease column button.
        elif col_down_button.x_pos <= mouse_pos[0] <= col_down_button.x_pos + col_down_button.width \
                and col_down_button.y_pos <= mouse_pos[1] <= col_down_button.y_pos + col_down_button.height:
            self.board.decrease_col()
        # On increase column button.
        elif col_up_button.x_pos <= mouse_pos[0] <= col_up_button.x_pos + col_up_button.width \
                and col_up_button.y_pos <= mouse_pos[1] <= col_up_button.y_pos + col_up_button.height:
            self.board.increase_col()
        # On Load File button.
        elif load_button.x_pos <= mouse_pos[0] <= load_button.x_pos + load_button.width \
                and load_button.y_pos <= mouse_pos[1] <= load_button.y_pos + load_button.height:
            self.load_tour()

    def check_ready_state_event(self, mouse_pos):
        # On Start Button. To start the tour
        if start_button.x_pos <= mouse_pos[0] <= start_button.x_pos + start_button.width \
                and start_button.y_pos <= mouse_pos[1] <= start_button.y_pos + start_button.height \
                and self.board.knight.knight_placed and not self.tour_found:
            self.game_state = "touring"
            start_button.change_text("Pause")
            self.time_start = datetime.now()

    def check_help_state_event(self, mouse_pos):
        # Displays the exit button of the help section
        if help_exit_button.x_pos <= mouse_pos[0] <= help_exit_button.x_pos + help_exit_button.width and \
                help_exit_button.y_pos <= mouse_pos[1] <= help_exit_button.y_pos + help_exit_button.height:
            self.game_state = "start"
            self.reset_game()
        elif help_prev_page_button.x_pos <= mouse_pos[0] <= help_prev_page_button.x_pos + help_prev_page_button.width and \
                help_prev_page_button.y_pos <= mouse_pos[1] <= help_prev_page_button.y_pos + help_prev_page_button.height:
            self.help_state.curr_page -= 1
            if self.help_state.curr_page < 1:
                self.help_state.curr_page = self.help_state.total_pages
            help_page_num_area.change_text(f"Page {self.help_state.curr_page}/{self.help_state.total_pages}")
        elif help_next_page_button.x_pos <= mouse_pos[0] <= help_next_page_button.x_pos + help_next_page_button.width and \
                help_next_page_button.y_pos <= mouse_pos[1] <= help_next_page_button.y_pos + help_next_page_button.height:
            self.help_state.curr_page += 1
            if self.help_state.curr_page > self.help_state.total_pages:
                self.help_state.curr_page = 1
            help_page_num_area.change_text(f"Page {self.help_state.curr_page}/{self.help_state.total_pages}")

    def check_touring_state_event(self, mouse_pos):
        if start_button.x_pos <= mouse_pos[0] <= start_button.x_pos + start_button.width \
                and start_button.y_pos <= mouse_pos[1] <= start_button.y_pos + start_button.height:
            self.game_state = "pause"
            start_button.change_text("Resume")
            self.duration += (datetime.now() - self.time_start).total_seconds()

    def check_pause_state_event(self, mouse_pos):
        if start_button.x_pos <= mouse_pos[0] <= start_button.x_pos + start_button.width \
                and start_button.y_pos <= mouse_pos[1] <= start_button.y_pos + start_button.height:
            self.game_state = "touring"
            start_button.change_text("Pause")
            self.time_start = datetime.now()
        if save_button.x_pos <= mouse_pos[0] <= save_button.x_pos + save_button.width \
                and save_button.y_pos <= mouse_pos[1] <= save_button.y_pos + save_button.height:
            self.save_tour()

    def is_valid_move(self, x, y):
        """
        A utility function to check if square (x, y) is valid and untraversed on the chessboard
        :param x: Row number of square
        :param y: Column number of square
        """
        if 0 <= x < self.board.row_dimension and 0 <= y < self.board.col_dimension and self.board.graph[x][y] == -1:
            return True
        return False

    def count_empty_squares(self, next_x, next_y):
        """
        Counts number of valid and untraversed squares from square (next_x, next_y)
        :param next_x: Row number of square
        :param next_y: Column number of square
        :return:
        """
        count = 0
        for i in range(8):
            if self.is_valid_move(next_x + self.board.knight.knight_moves[i][0],
                                  next_y + self.board.knight.knight_moves[i][1]):
                count += 1
        return count

    def check_if_closed_tour(self):
        """
        Checks if completed tour is closed. Checks whether first and last square of the tour can be reached by one
        another
        :return:
        """
        if (abs(self.board.knight.knight_initial_pos[0] - self.board.knight.knight_pos[0]) == 2
            and abs(self.board.knight.knight_initial_pos[1] - self.board.knight.knight_pos[1]) == 1) or \
                (abs(self.board.knight.knight_initial_pos[0] - self.board.knight.knight_pos[0]) == 1 and
                 abs(self.board.knight.knight_initial_pos[1] - self.board.knight.knight_pos[1]) == 2):
            return True
        else:
            return False

    def find_tour(self):
        """
        Function chooses the algorithm selected to find the tour.
        :return:
        """
        # First checks whether tour has already been found
        if not self.tour_found:
            # Then checks whether display has been updated
            if not self.move_done:
                if self.board.knight.knight_step < self.board.row_dimension * self.board.col_dimension:
                    # Checks type of algorithm used to find tour
                    if self.tour_type == "Warnsdorff":
                        self.find_tour_warnsdorff()
                    elif self.tour_type == "Backtrack":
                        self.find_tour_backtrack_iterative()
                else:
                    self.tour_found = True
                    self.duration += (datetime.now() - self.time_start).total_seconds()
                    if self.check_if_closed_tour():
                        start_point = self.board.knight.move_log[0]
                        line_start_point = (
                        (start_point[1] * self.board.sq_x_length) + OFFSET[0] + self.board.sq_x_length // 2,
                        (start_point[0] * self.board.sq_y_length) + OFFSET[1] + self.board.sq_y_length // 2)
                        end_point = self.board.knight.move_log[-1]
                        line_end_point = (
                            (end_point[1] * self.board.sq_x_length) + OFFSET[0] + self.board.sq_x_length // 2,
                            (end_point[0] * self.board.sq_y_length) + OFFSET[1] + self.board.sq_y_length // 2
                        )
                        pg.draw.line(SCREEN, "green", line_start_point, line_end_point, 5)
                        self.board.draw_knight_step(self.board.knight.knight_initial_pos[0],
                                                    self.board.knight.knight_initial_pos[1])
                        self.board.draw_knight_step(self.board.knight.knight_pos[0], self.board.knight.knight_pos[1])
                        update_below_board_text(f"Closed Knight's Tour found using {self.tour_type}",
                                                f"({self.board.knight.total_steps} moves in {round(self.duration, 2)} seconds)")
                    else:
                        update_below_board_text(f"Opened Knight's Tour found using {self.tour_type}",
                                                f"({self.board.knight.total_steps} moves in {round(self.duration, 2)} seconds)")

        self.redraw_speed()

    def find_tour_warnsdorff(self):
        """
        An iterative Warnsdorff's Heuristic to solve the knight's tour. This function relies on frame updates to
        perform the loop of every knight tour step.
        :return:
        """
        fewest_empty = 9
        fewest_empty_index = -1

        # To give some randomness when choosing a square. Only useful for next squares with the same number of next
        # valid squares
        random_num = random.randint(0, 1000) % 8
        for i in range(8):
            index = (random_num + i) % 8
            new_x = self.board.knight.knight_pos[0] + self.board.knight.knight_moves[index][0]
            new_y = self.board.knight.knight_pos[1] + self.board.knight.knight_moves[index][1]
            empty_sq_count = self.count_empty_squares(new_x, new_y)
            if self.is_valid_move(new_x, new_y) and empty_sq_count < fewest_empty:
                fewest_empty_index = index
                fewest_empty = empty_sq_count
            if self.is_valid_move(new_x, new_y) and empty_sq_count == fewest_empty:
                possible_move = (new_x, new_y)
                self.board.knight.possible_moves.append(possible_move)

        if fewest_empty_index == -1:
            self.game_state = "fail"
            self.tour_failures += 1
            if self.tour_failures >= 5:
                update_below_board_text("Warnsdorff algorithm failed to find a tour after 5 tries.",
                                        "Stopping the tour")
            return False

        new_x = self.board.knight.knight_pos[0] + self.board.knight.knight_moves[fewest_empty_index][0]
        new_y = self.board.knight.knight_pos[1] + self.board.knight.knight_moves[fewest_empty_index][1]
        self.board.knight.knight_step += 1
        self.board.graph[new_x][new_y] = self.board.knight.knight_step
        self.board.board_moves[new_x][new_y] += 1
        self.board.knight.knight_pos = (new_x, new_y)
        self.board.knight.move_log.append((new_x, new_y))
        self.move_done = True
        self.board.knight.total_steps += 1

    def find_tour_backtrack_iterative(self):
        """
        An iterative backtracking algorithm to solve the knight's tour. This is a brute force method which isn't
        practical as the time complexity is O(8**(N**2)). This function relies on frame updates to perform the loop of
        every knight tour step.

        The steps are as follows
        1.  Get last square of the move log
        2.  Check if there are valid moves to be made by the knight from the square
        3.  If a valid move is found, use the move to move the knight and add the new square to the log. Update the
            previous square with the next move.
        4. If no valid move is found, remove the square from the log
        """
        # move_log stores list of squares traversed by the knight
        # Each square contains (row, column, next index to use of knight_moves list)
        last_used_square = self.board.knight.move_log[-1]
        contains_valid = False
        # Checks if the square has valid moves, if so, move to that new square
        for i in range(last_used_square[2], 8):
            new_x = last_used_square[0] + self.board.knight.knight_moves[i][0]
            new_y = last_used_square[1] + self.board.knight.knight_moves[i][1]
            if self.is_valid_move(new_x, new_y):
                # Update the last square of move_log so that the next knight move to check will be the next one
                self.board.knight.move_log[-1] = (self.board.knight.knight_pos[0],
                                                  self.board.knight.knight_pos[1], i + 1)
                self.board.knight.knight_step += 1
                self.board.graph[new_x][new_y] = self.board.knight.knight_step
                self.board.board_moves[new_x][new_y] += 1
                self.board.knight.knight_pos = (new_x, new_y)
                new_pos = (new_x, new_y, 0)
                self.board.knight.move_log.append(new_pos)
                contains_valid = True
                break
        # If no valid moves can be done, remove square from stack
        if not contains_valid:
            self.board.graph[self.board.knight.knight_pos[0]][self.board.knight.knight_pos[1]] = -1
            self.board.knight.knight_step -= 1
            self.board.knight.move_log.pop()
            if len(self.board.knight.move_log) == 0:
                self.game_state = "fail"
                return
            self.board.knight.knight_pos = (self.board.knight.move_log[-1][0], self.board.knight.move_log[-1][1])
        self.move_done = True
        self.board.knight.total_steps += 1

    def update_frame(self):
        """
        Process flow that determines the next behaviour of the game state before updating display
        :return:
        """
        display_title()
        self.display_components()
        if self.game_state == "touring":
            self.find_tour()
        if self.game_state == "fail" and self.tour_type == "Warnsdorff":
            if self.tour_failures <= 5:
                self.redo_tour()
            else:
                update_below_board_text("Warnsdorff Algorithm failed to find a tour after 5 tries.", "Stopping the tour.")
        if self.game_state == "fail" and self.tour_type == "Backtrack":
            update_below_board_text("Backtrack algorithm failed to find a tour.", "No reason to brute force again.")
        if not self.running:
            pg.quit()
            sys.exit()
        pg.event.pump()


def main():
    chess_state = GameState()
    while True:
        chess_state.update_frame()


if __name__ == "__main__":
    main()
