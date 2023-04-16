# Python3 program to solve Knight Tour problem using Backtracking or Warnsdorff
import sys
import pygame as pg
import numpy as np
import random
from datetime import datetime
import Components

pg.init()

# Colours
BACKGROUND_COLOUR = (180, 241, 255)
BUTTON_COLOUR = (100, 100, 100)  # Default button color
HOVER_BUTTON_COLOUR = (170, 170, 170)  # Color of button when cursor hovers over
BUTTON_TEXT_COLOUR = (255, 255, 255)
TEXT_COLOUR = (0, 0, 0)

# Global variables for display
SCREEN = pg.display.set_mode(size=(0, 0))  # Set game window
SCREEN.fill(BACKGROUND_COLOUR)  # Set background color
x_axis, y_axis = SCREEN.get_size()
BOARD_SIZE = ((y_axis // 10) * 8, (y_axis // 10) * 8)  # Size of board
OFFSET = (50, 50)  # Amount of offset of the board from the border
# SCREEN_SIZE = (900, 600)  # Size of game window
# SCREEN = pg.display.set_mode(SCREEN_SIZE)  # Set game window
BUTTON_FONT = pg.font.SysFont('Arial', 30)  # Font for buttons
TEXT_FONT = pg.font.SysFont('Arial', 25)  # Font for text below the board
BOLD_TEXT_FONT = pg.font.SysFont('Arial', 30, bold=True)

# Play, Reset, and Quit buttons in one group
# Button(x_pos, y_pos, width, height, button_colour, hover_colour, button_text_colour)
start_button = Components.Square((x_axis // 10) * 9, (y_axis // 10) * 2, (x_axis // 100) * 10, y_axis // 20, pg,
                                 BUTTON_COLOUR, HOVER_BUTTON_COLOUR, "Start", BUTTON_TEXT_COLOUR, BUTTON_FONT)
pause_button = Components.Square((x_axis // 10) * 9, (y_axis // 10) * 2, (x_axis // 100) * 10, y_axis // 20, pg,
                                 BUTTON_COLOUR, HOVER_BUTTON_COLOUR, "Pause", BUTTON_TEXT_COLOUR, BUTTON_FONT)
help_button = Components.Square((x_axis // 10) * 9, (y_axis // 10) * 4, (x_axis // 100) * 10, y_axis // 20, pg,
                                BUTTON_COLOUR, HOVER_BUTTON_COLOUR, "Help", BUTTON_TEXT_COLOUR, BUTTON_FONT)
reset_button = Components.Square((x_axis // 10) * 9, (y_axis // 10) * 6, (x_axis // 100) * 10, y_axis // 20, pg,
                                 BUTTON_COLOUR, HOVER_BUTTON_COLOUR, "Reset", BUTTON_TEXT_COLOUR, BUTTON_FONT)
quit_button = Components.Square((x_axis // 10) * 9, (y_axis // 10) * 8, (x_axis // 100) * 10, y_axis // 20, pg,
                                BUTTON_COLOUR, HOVER_BUTTON_COLOUR, "Quit", BUTTON_TEXT_COLOUR, BUTTON_FONT)

# Tour Type, FPS, and Dimension buttons in another group
# Buttons to select Tour Type
backtrack_button = Components.Square((x_axis // 10) * 5.5, (y_axis // 10), (x_axis // 10) * 2, y_axis // 20, pg,
                                     BUTTON_COLOUR, HOVER_BUTTON_COLOUR,
                                     "Backtrack Method", BUTTON_TEXT_COLOUR, BUTTON_FONT)
warnsdorff_button = Components.Square((x_axis // 10) * 5.5, (y_axis // 10) * 3, (x_axis // 10) * 2, y_axis // 20, pg,
                                      BUTTON_COLOUR, HOVER_BUTTON_COLOUR,
                                      "Warnsdoff's Method", BUTTON_TEXT_COLOUR, BUTTON_FONT)
# Buttons to decrease/increase number of rows
row_down_button = Components.Square((x_axis // 10) * 5.5, (y_axis // 10) * 5, (x_axis // 100) * 5, y_axis // 20, pg,
                                    BUTTON_COLOUR, HOVER_BUTTON_COLOUR, "-1", BUTTON_TEXT_COLOUR, BUTTON_FONT)
row_up_button = Components.Square(warnsdorff_button.x_pos + warnsdorff_button.width - (x_axis // 100) * 5,
                                  (y_axis // 10) * 5, (x_axis // 100) * 5, y_axis // 20, pg,
                                  BUTTON_COLOUR, HOVER_BUTTON_COLOUR, "+1", BUTTON_TEXT_COLOUR, BUTTON_FONT)
# Buttons to decrease/increase number of columns
col_down_button = Components.Square((x_axis // 10) * 5.5, (y_axis // 10) * 7, (x_axis // 100) * 5, y_axis // 20, pg,
                                    BUTTON_COLOUR, HOVER_BUTTON_COLOUR, "-1", BUTTON_TEXT_COLOUR, BUTTON_FONT)
col_up_button = Components.Square(warnsdorff_button.x_pos + warnsdorff_button.width - (x_axis // 100) * 5,
                                  (y_axis // 10) * 7, (x_axis // 100) * 5, y_axis // 20, pg,
                                  BUTTON_COLOUR, HOVER_BUTTON_COLOUR, "+1", BUTTON_TEXT_COLOUR, BUTTON_FONT)
# Buttons to decrease/increase FPS
fps_down_button = Components.Square((x_axis // 10) * 5.5, (y_axis // 10) * 9, (x_axis // 100) * 5, y_axis // 20, pg,
                                    BUTTON_COLOUR, HOVER_BUTTON_COLOUR, "-5", BUTTON_TEXT_COLOUR, BUTTON_FONT)
fps_up_button = Components.Square(warnsdorff_button.x_pos + warnsdorff_button.width - (x_axis // 100) * 5,
                                  (y_axis // 10) * 9, (x_axis // 100) * 5, y_axis // 20, pg,
                                  BUTTON_COLOUR, HOVER_BUTTON_COLOUR, "+10", BUTTON_TEXT_COLOUR, BUTTON_FONT)

# Game text under the chessboard
under_board_line_text = Components.Square(50, 50 + BOARD_SIZE[1], BOARD_SIZE[0], 1.5 * BOARD_SIZE[1] // 8, pg,
                                          BACKGROUND_COLOUR, None, "", TEXT_COLOUR, TEXT_FONT)
# Area to display row number text
row_text = Components.Square((x_axis // 10) * 5.5, (y_axis // 10) * 5, (x_axis // 10) * 2, y_axis // 20, pg,
                             BUTTON_COLOUR, None, "Rows", TEXT_COLOUR, BUTTON_FONT)

# Area to display column number text
col_text = Components.Square((x_axis // 10) * 5.5, (y_axis // 10) * 7, (x_axis // 10) * 2, y_axis // 20, pg,
                             BUTTON_COLOUR, None, "Columns", TEXT_COLOUR, BUTTON_FONT)

# Area to display FPS text
fps_text = Components.Square((x_axis // 10) * 5.5, (y_axis // 10) * 9, (x_axis // 10) * 2, y_axis // 20, pg,
                             BUTTON_COLOUR, None, "FPS", TEXT_COLOUR, BUTTON_FONT)

# Area to display "Help"
component_title_text = "Components"
component_desc_text = "-    Algorithms. Choose type of algorithm to find a Knight's Tour. \n" + \
                      "-    Rows. Changes the number of rows in the chessboard. (Minimum rows = 3. Maximum rows = 13.) \n" + \
                      "-    Columns. Changes the number of columns in the chessboard respectively. (Minimum columns = 3. Maximum columns = 13.) \n" + \
                      "-    FPS. Changes the Frames Per Second of when finding the Knight's Tour. Can be changed while algorithm is running. \n" + \
                      "-    Start. Start the Knight's Tour. \n" + \
                      "-    Reset. Reset the state of the application. \n" + \
                      "-    Reset. Reset the state of the application. \n" + \
                      "-    Quit. Exit the application. The ESC key can be pressed to exit the application as well. \n"
usage_title_text = "How To Use"
usage_desc_text = "1.   Click on \"-1\" or \"+1\" of Rows/Columns to decrease or increase the number of rows/columns in the chessboard respectively. \n" + \
                  "2.   Click on a square in the chessboard to place a Knight piece in that square of the board. \n" + \
                  "3.   Click on Algorithms to choose the type of algorithm to be used to find the Knight's Tour. \n" + \
                  "4.   Click on Start to start finding the Knight's Tour. Start button will change to Pause. Click on Pause to pause the Tour \n" + \
                  "    finding. Pause button will change to Start. Click on Start to continue the tour. \n" + \
                  "5.   Application will generate a tour until found or fails after 5 tries. \n" + \
                  "6.   Click on Reset to clean the board. This can be done before or after a tour has been found. This will reset the board, \n" + \
                  "    rows, columns, and algorithm. \n" + \
                  "7.   Click on Quit or press ESC to exit the application."

component_title_area = Components.Square((x_axis // 100) * 5, (y_axis // 100) * 5, (x_axis // 100) * 92,
                                         (y_axis // 100) * 10, pg, (0, 0, 0), None, component_title_text,
                                         (255, 255, 255), BOLD_TEXT_FONT)
component_desc_area = Components.Square((x_axis // 100) * 5, component_title_area.y_pos+component_title_area.height,
                                        (x_axis // 100) * 92, (y_axis // 100) * 30, pg, (0, 0, 0), None, component_desc_text,
                                        (255, 255, 255), TEXT_FONT)
usage_title_area = Components.Square((x_axis // 100) * 5, component_desc_area.y_pos+component_desc_area.height,
                                     (x_axis // 100) * 92, (y_axis // 100) * 10, pg, (0, 0, 0), None, usage_title_text,
                                     (255, 255, 255), BOLD_TEXT_FONT)
usage_desc_area = Components.Square((x_axis // 100) * 5, usage_title_area.y_pos+usage_title_area.height,
                                    (x_axis // 100) * 92, (y_axis // 100) * 35, pg, (0, 0, 0), None, usage_desc_text,
                                    (255, 255, 255), TEXT_FONT)
help_exit_button = Components.Square(component_title_area.x_pos+component_title_area.width-(component_title_area.width // 20),
                                     (y_axis // 100) * 5, component_title_area.width // 20,
                                     (component_title_area.height // 10) * 4, pg,
                                     (0, 0, 0), HOVER_BUTTON_COLOUR, "X", (255, 255, 255), TEXT_FONT)


def multiple_line_text(surface, text, pos, font, colour):
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


# # Chess board data
# DIMENSIONS = 8  # Chessboard Size
# # Size of each square
# SQ_SIZE = BOARD_SIZE[0] // DIMENSIONS
# Coloring of board
BOARD_COLORS = [pg.Color("white"), pg.Color("grey")]

# Set window Title
pg.display.set_caption("Knight Tour")
# Set window Icon
icon = pg.image.load("knight_piece.png")
pg.display.set_icon(icon)
# Create knight piece image
knight_piece = pg.image.load("knight_piece.png")


def update_below_board_text(text, extra_text=None):
    """
    Used to update the text box below the board.
    :param text: The string to be displayed underneath the board
    :param extra_text: Extra info to be displayed below text
    :return:
    """
    global under_board_line_text
    under_board_line_1_text = TEXT_FONT.render(text, True, under_board_line_text.text_colour)
    under_board_line_1_text_rect = under_board_line_1_text.get_rect(
        center=(under_board_line_text.x_pos + (under_board_line_text.width // 2),
                under_board_line_text.y_pos + (under_board_line_text.height // 5))
    )
    pg.draw.rect(SCREEN, under_board_line_text.colour, under_board_line_text.rect)
    SCREEN.blit(under_board_line_1_text, under_board_line_1_text_rect)
    if extra_text is not None:
        under_board_line_2_text = TEXT_FONT.render(extra_text, True, under_board_line_text.text_colour)
        under_board_line_2_text_rect = under_board_line_2_text.get_rect(
            center=(under_board_line_text.x_pos + (under_board_line_text.width // 2),
                    under_board_line_text.y_pos + (under_board_line_text.height // 2))
        )
        SCREEN.blit(under_board_line_2_text, under_board_line_2_text_rect)


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
        self.steps_done = 0
        self.knight_img = pg.image.load("knight_piece.png")
        self.step_font = pg.font.SysFont("Arial", 20)


class Board:
    def __init__(self, knight: Knight, row_dimension=8, col_dimension=8):
        self.knight = knight
        self.board_size = ((y_axis // 10) * row_dimension, (y_axis // 10) * col_dimension)  # Size of board
        self.row_dimension = row_dimension
        self.col_dimension = col_dimension
        self.graph = np.negative(np.ones([row_dimension, col_dimension], dtype=int))
        self.board_moves = np.zeros([row_dimension, col_dimension], dtype=int)
        self.sq_x_length = BOARD_SIZE[0] // col_dimension
        self.sq_y_length = BOARD_SIZE[0] // row_dimension
        self.moves_font = pg.font.SysFont("Arial", 15)

    def draw_board(self):
        # Draw chessboard. Top left square is always light color
        pg.draw.rect(SCREEN, BACKGROUND_COLOUR, pg.Rect(OFFSET[0], OFFSET[1], BOARD_SIZE[0], BOARD_SIZE[1]))
        for row in range(self.row_dimension):
            for col in range(self.col_dimension):
                color = BOARD_COLORS[(row + col) % 2]
                pg.draw.rect(SCREEN, color,
                             # x-axis = column (left to right) , y-axis = row (top to bottom)
                             # Draw the starting point of the square
                             # Add off set if chessboard not touching the border of window
                             pg.Rect((col * self.sq_x_length) + OFFSET[0], (row * self.sq_y_length) + OFFSET[1],
                                     self.sq_x_length, self.sq_y_length))

    def draw_knight(self, width, height):
        self.knight.knight_img = pg.transform.scale(self.knight.knight_img,
                                                    (0.8 * self.sq_x_length, 0.8 * self.sq_y_length))
        SCREEN.blit(self.knight.knight_img,
                    pg.Rect((self.knight.knight_pos[1] * width) + OFFSET[0] + width // 8,
                            (self.knight.knight_pos[0] * height) + OFFSET[1] + height // 8,
                            width, height)
                    )

    def check_dimensions_then_draw(self):
        row = self.row_dimension
        col = self.col_dimension
        if self.row_dimension > 8:
            row = 8
        if self.col_dimension > 8:
            col = 8
        self.board_size = ((y_axis // 10) * row, (y_axis // 10) * col)
        self.sq_x_length = self.board_size[1] // self.col_dimension
        self.sq_y_length = self.board_size[0] // self.row_dimension
        if self.sq_x_length < self.sq_y_length:
            self.knight.step_font = pg.font.SysFont("Arial", self.sq_x_length // 4)
        else:
            self.knight.step_font = pg.font.SysFont("Arial", self.sq_y_length // 4)
        self.knight.knight_img = pg.transform.scale(self.knight.knight_img,
                                                    (self.sq_x_length * 0.8, self.sq_y_length * 0.8))
        self.draw_board()

    def decrease_row(self):
        if self.row_dimension <= 3:
            return
        self.row_dimension -= 1
        self.graph = np.negative(np.ones([self.row_dimension, self.col_dimension], dtype=int))
        self.check_dimensions_then_draw()

    def increase_row(self):
        if self.row_dimension >= 13:
            return
        self.row_dimension += 1
        self.graph = np.negative(np.ones([self.row_dimension, self.col_dimension], dtype=int))
        self.check_dimensions_then_draw()

    def decrease_col(self):
        if self.col_dimension <= 3:
            return
        self.col_dimension -= 1
        self.graph = np.negative(np.ones([self.row_dimension, self.col_dimension], dtype=int))
        self.check_dimensions_then_draw()

    def increase_col(self):
        if self.col_dimension >= 13:
            return
        self.col_dimension += 1
        self.graph = np.negative(np.ones([self.row_dimension, self.col_dimension], dtype=int))
        self.check_dimensions_then_draw()

    def draw_square(self, row, col):
        color = BOARD_COLORS[(row + col) % 2]
        pg.draw.rect(SCREEN, color, pg.Rect((col * self.sq_x_length) + OFFSET[0], (row * self.sq_y_length) + OFFSET[1],
                                            self.sq_x_length, self.sq_y_length))

    def draw_numbers(self):
        for row in range(self.row_dimension):
            for col in range(self.col_dimension):
                self.draw_knight_step(row, col)
                self.draw_move_number(row, col)

    def draw_knight_step(self, row, col):
        """
        This function is responsible for drawing the stamp and step number made by the knight
        :param row: Row number of board
        :param col: Column number of board
        :return:None
        """
        furthest_node = self.graph.max()
        if (self.graph[row][col] != -1 and self.graph[row][col] != furthest_node) \
                or self.graph[row][col] == self.row_dimension * self.col_dimension:
            stamp = ((col * self.sq_x_length) + OFFSET[0] + self.sq_x_length // 2,
                     (row * self.sq_y_length) + OFFSET[1] + self.sq_y_length // 2)
            if self.sq_x_length < self.sq_y_length:
                pg.draw.circle(SCREEN, (51, 255, 51), stamp, self.sq_x_length // 4)
            else:
                pg.draw.circle(SCREEN, (51, 255, 51), stamp, self.sq_y_length // 4)
            number = self.graph[row][col]
            SCREEN.blit(self.knight.step_font.render(f"{number: 03d}", True, (0, 0, 0)),
                        (stamp[0] - self.sq_x_length * 0.15, stamp[1] - self.sq_y_length * 0.13))

    def draw_move_number(self, row, col):
        stamp = ((col * self.sq_x_length) + OFFSET[0] + ((self.sq_x_length // 4) * 3),
                      (row * self.sq_y_length) + OFFSET[1] + ((self.sq_y_length // 4) * 3))
        # number_color = BOARD_COLORS[(row + col + 1) % 2]
        number = self.board_moves[row][col]
        SCREEN.blit(self.moves_font.render(f"{number}", True, (0, 0, 0)),
                    (stamp[0], stamp[1]))


class ChessState:
    def __init__(self, board: Board):
        # Initialise board array. Board is n x n matrix
        self.board = board
        # State of chessboard (start, ready, touring, fail, pause, help)
        self.game_state = "start"
        # What components need to be displayed (buttons, help)
        self.display_state = "buttons"
        # Used for counting how many times Warnsdorff fails to find a tour
        self.tour_failures = 0
        self.tour_found = False  # Whether knight tour is found
        self.running = True  # Whether game is running
        self.tour_type = "Backtrack"
        self.move_done = False
        self.fps = 30
        self.last_frame_tick = 0
        self.board.draw_board()
        self.time_start = datetime.now()
        self.duration = 0
        # Display text underneath board
        update_below_board_text(f"{self.tour_type} Algorithm at {self.fps} Frames Per Second (FPS)")

    def reset_board(self):
        self.board.graph = np.negative(np.ones([8, 8], dtype=int))
        self.board.board_moves = np.zeros([8, 8], dtype=int)
        self.board.row_dimension = 8
        self.board.col_dimension = 8
        self.game_state = "start"
        self.tour_failures = 0
        self.tour_found = False
        self.board.knight.knight_placed = False
        self.board.knight.knight_initial_pos = None
        self.board.knight.knight_pos = None
        self.board.knight.knight_step = 1
        self.board.knight.move_log = []
        self.board.knight.steps_done = 0
        self.board.knight.knight_img = pg.image.load("knight_piece.png")
        self.board.knight.step_font = pg.font.SysFont("Arial", 20)
        self.board.board_size = ((y_axis // 10) * 8, (y_axis // 10) * 8)  # Size of board
        self.board.sq_x_length = self.board.board_size[0] // 8
        self.board.sq_y_length = self.board.board_size[0] // 8
        self.time_start = 0.0
        self.duration = 0.0
        SCREEN.fill(BACKGROUND_COLOUR)
        self.board.draw_board()
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
        update_below_board_text("Warnsdorff algorithm failed to find a tour.", f"Retry No. {self.tour_failures}")

    def redraw_board(self):
        if self.move_done and (pg.time.get_ticks() - self.last_frame_tick) > 1000 / self.fps:
            furthest_node = self.board.graph.max()
            self.board.draw_board()
            self.draw_lines()
            self.board.draw_numbers()

            # print(furthest_node)
            if furthest_node == self.board.row_dimension * self.board.col_dimension:
                # print("Draw Number")
                self.board.draw_knight_step(self.board.knight.knight_pos[0], self.board.knight.knight_pos[1])
            else:
                # print("Draw Knight")
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
        global fps_down_button, fps_up_button
        if self.fps == 30:
            fps_down_button.text = BUTTON_FONT.render("-5", True, fps_down_button.text_colour)
            fps_up_button.text = BUTTON_FONT.render("+10", True, fps_up_button.text_colour)
        elif self.fps == 10:
            fps_down_button.text = BUTTON_FONT.render("-1", True, fps_down_button.text_colour)
            fps_up_button.text = BUTTON_FONT.render("+5", True, fps_down_button.text_colour)
        elif 1 < self.fps < 10:
            fps_down_button.text = BUTTON_FONT.render("-1", True, fps_down_button.text_colour)
            fps_up_button.text = BUTTON_FONT.render("+1", True, fps_up_button.text_colour)
        elif 10 < self.fps < 30:
            fps_down_button.text = BUTTON_FONT.render("-5", True, fps_down_button.text_colour)
            fps_up_button.text = BUTTON_FONT.render("+5", True, fps_up_button.text_colour)
        elif 30 < self.fps < 60:
            fps_down_button.text = BUTTON_FONT.render("-10", True, fps_down_button.text_colour)
            fps_up_button.text = BUTTON_FONT.render("+10", True, fps_up_button.text_colour)

    # Checks if user selected the same square twice. If so, remove the knight
    def place_first_knight(self, selected_sq):
        if not (self.game_state == "start" or self.game_state == "ready"):
            return
        row = selected_sq[0]
        col = selected_sq[1]
        # Checks if user selected the same square twice. If so, remove the knight
        if selected_sq == self.board.knight.knight_pos:
            # print("Same Square")
            self.board.draw_square(self.board.knight.knight_pos[0], self.board.knight.knight_pos[1])
            self.board.graph[row][col] = -1
            self.board.board_moves[row][col] = 0
            self.board.knight.knight_placed = False
            self.board.knight.knight_pos = None
            self.board.knight.knight_initial_pos = None
            self.game_state = "start"
            self.board.knight.move_log.pop()
        elif not self.board.knight.knight_placed:
            self.board.knight.knight_placed = True
            self.board.knight.knight_pos = (row, col)
            self.board.knight.knight_initial_pos = (row, col)
            self.board.graph[row][col] = 1
            self.board.board_moves[row][col] = 1
            self.game_state = "ready"
            self.board.draw_knight(self.board.sq_x_length, self.board.sq_y_length)
            self.board.knight.move_log.append((row, col, 0))
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
            self.board.draw_knight(self.board.sq_x_length, self.board.sq_y_length)

    def draw_lines(self):
        i = 2
        # print("Moves =", self.knight.move_log)
        while i <= len(self.board.knight.move_log):
            start_point = self.board.knight.move_log[i - 2]
            line_start_point = ((start_point[1] * self.board.sq_x_length) + OFFSET[0] + self.board.sq_x_length // 2,
                                (start_point[0] * self.board.sq_y_length) + OFFSET[1] + self.board.sq_y_length // 2)
            end_point = self.board.knight.move_log[i - 1]
            line_end_point = ((end_point[1] * self.board.sq_x_length) + OFFSET[0] + self.board.sq_x_length // 2,
                              (end_point[0] * self.board.sq_y_length) + OFFSET[1] + self.board.sq_y_length // 2)
            pg.draw.line(SCREEN, (0, 255, 0), line_start_point, line_end_point, 5)
            i += 1

    def check_game_event(self, mouse_pos):
        """
        Checks the mouse click events
        :param mouse_pos: Position of mouse. [x, y]
        :return:
        """
        for event in pg.event.get():
            # Checks if the ESC key is press. If True, exit the application.
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.running = False
            # Checks if mouse click is on a component
            elif event.type == pg.MOUSEBUTTONDOWN:
                # On board area
                if OFFSET[0] < mouse_pos[0] < OFFSET[0] + self.board.board_size[0] and \
                        OFFSET[1] < mouse_pos[1] < OFFSET[1] + self.board.board_size[1]:
                    row = (mouse_pos[1] - OFFSET[1]) // self.board.sq_y_length
                    col = (mouse_pos[0] - OFFSET[0]) // self.board.sq_x_length
                    sq_selected = (row, col)
                    self.place_first_knight(sq_selected)
                # On Start Button. To start the tour
                elif start_button.x_pos <= mouse_pos[0] <= start_button.x_pos + start_button.width \
                        and start_button.y_pos <= mouse_pos[1] <= start_button.y_pos + start_button.height \
                        and self.board.knight.knight_placed and not self.tour_found:
                    if self.game_state == "ready":
                        self.game_state = "touring"
                        self.time_start = datetime.now()
                    elif self.game_state == "touring":
                        self.game_state = "pause"
                        self.duration += (datetime.now() - self.time_start).total_seconds()
                    elif self.game_state == "pause":
                        self.game_state = "touring"
                        self.time_start = datetime.now()
                # On Help Button. Displays the text on how to use the application.
                elif self.game_state != "touring" and \
                        help_button.x_pos <= mouse_pos[0] <= help_button.x_pos + help_button.width and \
                        help_button.y_pos <= mouse_pos[1] <= help_button.y_pos + help_button.height:
                    self.game_state = "help"
                # On Reset Button. Resets the board
                elif reset_button.x_pos <= mouse_pos[0] <= reset_button.x_pos + reset_button.width \
                        and reset_button.y_pos <= mouse_pos[1] <= reset_button.y_pos + reset_button.height:
                    self.reset_board()
                # Quit Button. Stops the game
                elif quit_button.x_pos <= mouse_pos[0] <= quit_button.x_pos + quit_button.width \
                        and quit_button.y_pos <= mouse_pos[1] <= quit_button.y_pos + quit_button.height:
                    self.running = False
                # On Backtrack Button. Change the tour finding method to backtracking
                elif backtrack_button.x_pos <= mouse_pos[0] <= backtrack_button.x_pos + backtrack_button.width \
                        and backtrack_button.y_pos <= mouse_pos[1] <= backtrack_button.y_pos + backtrack_button.height \
                        and (self.game_state == "start" or self.game_state == "ready"):
                    self.tour_type = "Backtrack"
                    # Display text underneath board
                    update_below_board_text(f"{self.tour_type} Algorithm at {self.fps} Frames Per Second (FPS)")
                # On Warnsdorff Button. Change the tour finding method to Warnsdorff
                elif warnsdorff_button.x_pos <= mouse_pos[0] <= warnsdorff_button.x_pos + warnsdorff_button.width \
                        and warnsdorff_button.y_pos <= mouse_pos[
                    1] <= warnsdorff_button.y_pos + warnsdorff_button.height \
                        and (self.game_state == "start" or self.game_state == "ready"):
                    self.tour_type = "Warnsdorff"
                    # Display text underneath board
                    update_below_board_text(f"{self.tour_type} Algorithm at {self.fps} Frames Per Second (FPS)")
                # On decrease row button.
                elif row_down_button.x_pos <= mouse_pos[0] <= row_down_button.x_pos + row_down_button.width \
                        and row_down_button.y_pos <= mouse_pos[1] <= row_down_button.y_pos + row_down_button.height \
                        and self.game_state == "start":
                    self.board.decrease_row()
                # On increase row button.
                elif row_up_button.x_pos <= mouse_pos[0] <= row_up_button.x_pos + row_up_button.width \
                        and row_up_button.y_pos <= mouse_pos[1] <= row_up_button.y_pos + row_up_button.height \
                        and self.game_state == "start":
                    self.board.increase_row()
                # On decrease column button.
                elif col_down_button.x_pos <= mouse_pos[0] <= col_down_button.x_pos + col_down_button.width \
                        and col_down_button.y_pos <= mouse_pos[1] <= col_down_button.y_pos + col_down_button.height \
                        and self.game_state == "start":
                    self.board.decrease_col()
                # On increase column button.
                elif col_up_button.x_pos <= mouse_pos[0] <= col_up_button.x_pos + col_up_button.width \
                        and col_up_button.y_pos <= mouse_pos[1] <= col_up_button.y_pos + col_up_button.height \
                        and self.game_state == "start":
                    self.board.increase_col()
                # On decrease FPS button.
                elif fps_down_button.x_pos <= mouse_pos[0] <= fps_down_button.x_pos + fps_down_button.width \
                        and fps_down_button.y_pos <= mouse_pos[1] <= fps_down_button.y_pos + fps_down_button.height:
                    self.decrease_fps()
                    update_below_board_text(f"{self.tour_type} Algorithm at {self.fps} Frames Per Second (FPS)")
                # On increase FPS button.
                elif fps_up_button.x_pos <= mouse_pos[0] <= fps_up_button.x_pos + fps_up_button.width \
                        and fps_down_button.y_pos <= mouse_pos[1] <= fps_up_button.y_pos + fps_up_button.height:
                    self.increase_fps()
                    update_below_board_text(f"{self.tour_type} Algorithm at {self.fps} Frames Per Second (FPS)")

    def display_game_buttons(self):
        """
        Draws the buttons and text
        :return:
        """
        mouse_pos = pg.mouse.get_pos()
        # Display Start/Pause button
        if start_button.x_pos <= mouse_pos[0] <= start_button.x_pos + start_button.width \
                and start_button.y_pos <= mouse_pos[1] <= start_button.y_pos + start_button.height:
            pg.draw.rect(SCREEN, start_button.hover_colour, start_button.rect)
        else:
            pg.draw.rect(SCREEN, start_button.colour, start_button.rect)
        # Display text of Start/Pause button
        if self.game_state == "touring":
            SCREEN.blit(pause_button.text, pause_button.text_rect)
        else:
            SCREEN.blit(start_button.text, start_button.text_rect)
        # Display Help button
        if self.game_state != "touring" and \
                help_button.x_pos <= mouse_pos[0] <= help_button.x_pos + help_button.width and \
                help_button.y_pos <= mouse_pos[1] <= help_button.y_pos + help_button.height:
            pg.draw.rect(SCREEN, help_button.hover_colour, help_button.rect)
        else:
            pg.draw.rect(SCREEN, help_button.colour, help_button.rect)
        SCREEN.blit(help_button.text, help_button.text_rect)
        # Display Reset button
        if reset_button.x_pos <= mouse_pos[0] <= reset_button.x_pos + reset_button.width \
                and reset_button.y_pos <= mouse_pos[1] <= reset_button.y_pos + reset_button.height:
            pg.draw.rect(SCREEN, reset_button.hover_colour, reset_button.rect)
        else:
            pg.draw.rect(SCREEN, reset_button.colour, reset_button.rect)
        SCREEN.blit(reset_button.text, reset_button.text_rect)
        # Display Quit button
        if quit_button.x_pos <= mouse_pos[0] <= quit_button.x_pos + quit_button.width \
                and quit_button.y_pos <= mouse_pos[1] <= quit_button.y_pos + quit_button.height:
            pg.draw.rect(SCREEN, quit_button.hover_colour, quit_button.rect)
        else:
            pg.draw.rect(SCREEN, quit_button.colour, quit_button.rect)
        SCREEN.blit(quit_button.text, quit_button.text_rect)
        # Sets visibility of knight's tour buttons
        if self.tour_type == "Warnsdorff":
            # Display Backtrack button
            if self.game_state != "touring" and \
                    backtrack_button.x_pos <= mouse_pos[0] <= backtrack_button.x_pos + backtrack_button.width and \
                    backtrack_button.y_pos <= mouse_pos[1] <= backtrack_button.y_pos + backtrack_button.height:
                pg.draw.rect(SCREEN, backtrack_button.hover_colour, backtrack_button.rect)
            else:
                pg.draw.rect(SCREEN, backtrack_button.colour, backtrack_button.rect)
            SCREEN.blit(backtrack_button.text, backtrack_button.text_rect)
            # Remove Warnsdorff button
            pg.draw.rect(SCREEN, BACKGROUND_COLOUR, warnsdorff_button.rect)
        elif self.tour_type == "Backtrack":
            # Display Warnsdorff button
            if self.game_state != "touring" and \
                    warnsdorff_button.x_pos <= mouse_pos[0] <= warnsdorff_button.x_pos + warnsdorff_button.width and \
                    warnsdorff_button.y_pos <= mouse_pos[1] <= warnsdorff_button.y_pos + warnsdorff_button.height:
                pg.draw.rect(SCREEN, warnsdorff_button.hover_colour, warnsdorff_button.rect)
            else:
                pg.draw.rect(SCREEN, warnsdorff_button.colour, warnsdorff_button.rect)
            SCREEN.blit(warnsdorff_button.text, warnsdorff_button.text_rect)
            # Remove Backtrack button
            pg.draw.rect(SCREEN, BACKGROUND_COLOUR, backtrack_button.rect)
        # Display row decrease button
        if self.game_state != "touring" and \
                row_down_button.x_pos <= mouse_pos[0] <= row_down_button.x_pos + row_down_button.width and \
                row_down_button.y_pos <= mouse_pos[1] <= row_down_button.y_pos + row_down_button.height:
            pg.draw.rect(SCREEN, row_down_button.hover_colour, row_down_button.rect)
        else:
            pg.draw.rect(SCREEN, row_down_button.colour, row_down_button.rect)
        SCREEN.blit(row_down_button.text, row_down_button.text_rect)
        # Display row increase button
        if self.game_state != "touring" and \
                row_up_button.x_pos <= mouse_pos[0] <= row_up_button.x_pos + row_up_button.width and \
                row_up_button.y_pos <= mouse_pos[1] <= row_up_button.y_pos + row_up_button.height:
            pg.draw.rect(SCREEN, row_up_button.hover_colour, row_up_button.rect)
        else:
            pg.draw.rect(SCREEN, row_up_button.colour, row_up_button.rect)
        SCREEN.blit(row_up_button.text, row_up_button.text_rect)
        # Display row text
        SCREEN.blit(row_text.text, row_text.text_rect)
        # Display column decrease button
        if self.game_state != "touring" and \
                col_down_button.x_pos <= mouse_pos[0] <= col_down_button.x_pos + col_down_button.width and \
                col_down_button.y_pos <= mouse_pos[1] <= col_down_button.y_pos + col_down_button.height:
            pg.draw.rect(SCREEN, col_down_button.hover_colour, col_down_button.rect)
        else:
            pg.draw.rect(SCREEN, col_down_button.colour, col_down_button.rect)
        SCREEN.blit(col_down_button.text, col_down_button.text_rect)
        # Display column increase button
        if self.game_state != "touring" and \
                col_up_button.x_pos <= mouse_pos[0] <= col_up_button.x_pos + col_up_button.width and \
                col_up_button.y_pos <= mouse_pos[1] <= col_up_button.y_pos + col_up_button.height:
            pg.draw.rect(SCREEN, col_up_button.hover_colour, col_up_button.rect)
        else:
            pg.draw.rect(SCREEN, col_up_button.colour, col_up_button.rect)
        SCREEN.blit(col_up_button.text, col_up_button.text_rect)
        # Display column text
        SCREEN.blit(col_text.text, col_text.text_rect)
        # Display fps decrease button
        if fps_down_button.x_pos <= mouse_pos[0] <= fps_down_button.x_pos + fps_down_button.width \
                and fps_down_button.y_pos <= mouse_pos[1] <= fps_down_button.y_pos + fps_down_button.height:
            pg.draw.rect(SCREEN, fps_down_button.hover_colour, fps_down_button.rect)
        else:
            pg.draw.rect(SCREEN, fps_down_button.colour, fps_down_button.rect)
        SCREEN.blit(fps_down_button.text, fps_down_button.text_rect)
        # Display fps increase button
        if fps_up_button.x_pos <= mouse_pos[0] <= fps_up_button.x_pos + fps_up_button.width \
                and fps_up_button.y_pos <= mouse_pos[1] <= fps_up_button.y_pos + fps_up_button.height:
            pg.draw.rect(SCREEN, fps_up_button.hover_colour, fps_up_button.rect)
        else:
            pg.draw.rect(SCREEN, fps_up_button.colour, fps_up_button.rect)
        SCREEN.blit(fps_up_button.text, fps_up_button.text_rect)
        # Display FPS text
        SCREEN.blit(fps_text.text, fps_text.text_rect)
        self.check_game_event(mouse_pos)
        pg.display.update()

    def check_help_event(self, mouse_pos):
        for event in pg.event.get():
            # Checks if the ESC key is press. If True, exit the application.
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if help_exit_button.x_pos <= mouse_pos[0] <= help_exit_button.x_pos + help_exit_button.width and \
                        help_exit_button.y_pos <= mouse_pos[1] <= help_exit_button.y_pos + help_exit_button.height:
                    self.game_state = "start"
                    self.reset_board()

    def display_help(self):
        mouse_pos = pg.mouse.get_pos()
        pg.draw.rect(SCREEN, component_title_area.colour, component_title_area.rect)
        SCREEN.blit(component_title_area.text, component_title_area.text_rect)
        if help_exit_button.x_pos <= mouse_pos[0] <= help_exit_button.x_pos + help_exit_button.width and \
                help_exit_button.y_pos <= mouse_pos[1] <= help_exit_button.y_pos + help_exit_button.height:
            pg.draw.rect(SCREEN, help_exit_button.hover_colour, help_exit_button.rect)
        else:
            pg.draw.rect(SCREEN, help_exit_button.colour, help_exit_button.rect)
        SCREEN.blit(help_exit_button.text, help_exit_button.text_rect)
        pg.draw.rect(SCREEN, component_desc_area.colour, component_desc_area.rect)
        multiple_line_text(SCREEN, component_desc_text, (component_desc_area.x_pos, component_desc_area.y_pos),
                           component_desc_area.text_font, component_desc_area.text_colour)
        pg.draw.rect(SCREEN, usage_title_area.colour, usage_title_area.rect)
        SCREEN.blit(usage_title_area.text, usage_title_area.text_rect)
        pg.draw.rect(SCREEN, usage_desc_area.colour, usage_desc_area.rect)
        multiple_line_text(SCREEN, usage_desc_text, (usage_desc_area.x_pos, usage_desc_area.y_pos),
                           usage_desc_area.text_font, usage_desc_area.text_colour)
        self.check_help_event(mouse_pos)
        pg.display.update()

    def is_valid_move(self, x, y):
        """
            A utility function to check if i,j are valid indexes
            for N*N chessboard
            :param x: row number of square
            :param y: column number of square
        """
        if 0 <= x < self.board.row_dimension and 0 <= y < self.board.col_dimension and self.board.graph[x][y] == -1:
            return True
        return False

    def count_empty_squares(self, next_x, next_y):
        count = 0
        for i in range(8):
            if self.is_valid_move(next_x + self.board.knight.knight_moves[i][0],
                                  next_y + self.board.knight.knight_moves[i][1]):
                count += 1
        return count

    def check_if_closed_tour(self):
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
                        update_below_board_text(f"Closed Knight's Tour found using {self.tour_type}",
                                                f"({self.board.knight.steps_done} moves in {round(self.duration, 2)} seconds)")
                    else:
                        update_below_board_text(f"Opened Knight's Tour found using {self.tour_type}",
                                                f"({self.board.knight.steps_done} moves in {round(self.duration, 2)} seconds)")

        self.redraw_board()

    def find_tour_warnsdorff(self):
        """
        This function uses Warnsdorff's Heuristic to solve the knight's tour.
        :return:
        """
        most_empty = 9
        most_empty_index = -1

        # To give some randomness when choosing a square. Only useful for next squares with the same number of next
        # valid squares
        random_num = random.randint(0, 1000) % 8
        for i in range(8):
            index = (random_num + i) % 8
            new_x = self.board.knight.knight_pos[0] + self.board.knight.knight_moves[index][0]
            new_y = self.board.knight.knight_pos[1] + self.board.knight.knight_moves[index][1]
            empty_sq_count = self.count_empty_squares(new_x, new_y)
            if self.is_valid_move(new_x, new_y) and empty_sq_count < most_empty:
                most_empty_index = index
                most_empty = empty_sq_count
            if self.is_valid_move(new_x, new_y) and empty_sq_count == most_empty:
                possible_move = (new_x, new_y)
                self.board.knight.possible_moves.append(possible_move)

        if most_empty_index == -1:
            self.game_state = "fail"
            self.tour_failures += 1
            if self.tour_failures >= 5:
                update_below_board_text("Warnsdorff algorithm failed to find a tour after 5 tries.",
                                        "Stopping the tour")
            return False

        new_x = self.board.knight.knight_pos[0] + self.board.knight.knight_moves[most_empty_index][0]
        new_y = self.board.knight.knight_pos[1] + self.board.knight.knight_moves[most_empty_index][1]
        self.board.knight.knight_step += 1
        self.board.graph[new_x][new_y] = self.board.knight.knight_step
        self.board.board_moves[new_x][new_y] += 1
        self.board.knight.knight_pos = (new_x, new_y)
        self.board.knight.move_log.append((new_x, new_y))
        self.move_done = True
        self.board.knight.steps_done += 1

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
        last_used_square = self.board.knight.move_log[-1]
        contains_valid = False
        # Checks if the square has valid moves, if so, move to that new square
        for i in range(last_used_square[2], 8):
            new_x = last_used_square[0] + self.board.knight.knight_moves[i][0]
            new_y = last_used_square[1] + self.board.knight.knight_moves[i][1]
            if self.is_valid_move(new_x, new_y):
                # Update the last square of move_log so that the next knight move to check will be the next one
                # self.board.draw_square(self.knight.knight_pos[0], self.knight.knight_pos[1])
                # self.draw_line()
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
        self.board.knight.steps_done += 1

    def update_frame(self):
        """
        Process flow that determines the next behaviour of the game state before updating display
        :return:
        """
        if self.game_state == "touring":
            self.find_tour()
        if self.game_state == "fail" and self.tour_type == "Warnsdorff":
            if self.tour_failures <= 5:
                self.redo_tour()
        if self.game_state == "fail" and self.tour_type == "Backtrack":
            update_below_board_text("Backtrack algorithm failed to find a tour.", "No reason to brute force again.")
        if self.game_state == "pause":
            pass
        if not self.running:
            # stop = timeit.default_timer()
            # print('Time: ', stop - start, "seconds")
            # print(movement, "Iterations")
            pg.quit()
            sys.exit()
        if self.game_state == "help":
            self.display_help()
        else:
            self.display_game_buttons()
        pg.event.pump()


def main():
    knight = Knight()
    board = Board(knight)
    chess_state = ChessState(board)
    while True:
        chess_state.update_frame()


if __name__ == "__main__":
    main()
