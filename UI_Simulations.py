# Python3 program to solve Knight Tour problem using Backtracking or Warnsdorff
import sys
import pygame as pg
import numpy as np
import random
from datetime import datetime
import Components


pg.init()

# Global variables for display
SCREEN = pg.display.set_mode(size=(0, 0))  # Set game window
BACKGROUND_COLOUR = (180, 241, 255)
SCREEN.fill(BACKGROUND_COLOUR)  # Set background color
x_axis, y_axis = SCREEN.get_size()
# print(x_axis, y_axis)
BOARD_SIZE = ((y_axis // 10) * 8, (y_axis // 10) * 8)  # Size of board
# print(BOARD_SIZE)
OFFSET = (50, 50)  # Amount of offset of the board from the border
# SCREEN_SIZE = (900, 600)  # Size of game window
# SCREEN = pg.display.set_mode(SCREEN_SIZE)  # Set game window
BUTTON_FONT = pg.font.SysFont('Arial', 30)  # Font for buttons
MOVES_FONT = pg.font.SysFont('Arial', 20)  # Font for numbering the steps
TEXT_FONT = pg.font.SysFont('Arial', 30)  # Font for text
# DEFAULT_CURSOR = pg.mouse.get_cursor()

warnsdorff_time_path = "Simulations/Warnsdorff_ui_times.csv"
backtrack_time_path = "Simulations/Backtrack_ui_times.csv"

# Buttons
button_text_color = (255, 255, 255)
button_color = (100, 100, 100)  # Default button color
hover_button_color = (170, 170, 170)  # Color of button when cursor hovers over
# Play, Reset, and Quit buttons in one group
# Button(x_pos, y_pos, width, height, button_colour, hover_colour, button_text_colour)
start_details = Components.Rectangle((x_axis // 10) * 8, (y_axis // 10) * 2, (x_axis // 100) * 15, y_axis // 20, pg,
                                     button_color, button_text_color, hover_button_color)
reset_details = Components.Rectangle((x_axis // 10) * 8, (y_axis // 10) * 5, (x_axis // 100) * 15, y_axis // 20, pg,
                                     button_color, button_text_color, hover_button_color)
quit_details = Components.Rectangle((x_axis // 10) * 8, (y_axis // 10) * 8, (x_axis // 100) * 15, y_axis // 20, pg,
                                    button_color, button_text_color, hover_button_color)

# Tour Type, FPS, and Dimension buttons in another group
# Buttons to select Tour Type
backtrack_details = Components.Rectangle((x_axis // 10) * 5.5, (y_axis // 10), (x_axis // 10) * 2, y_axis // 20, pg,
                                         button_color, button_text_color, hover_button_color)
warnsdorff_details = Components.Rectangle((x_axis // 10) * 5.5, (y_axis // 10) * 3, (x_axis // 10) * 2, y_axis // 20, pg,
                                          button_color, button_text_color, hover_button_color)
# Buttons to decrease/increase number of rows
row_down_details = Components.Rectangle((x_axis // 10) * 5.5, (y_axis // 10) * 5, (x_axis // 100) * 5, y_axis // 20, pg,
                                        button_color, button_text_color, hover_button_color)
row_up_details = Components.Rectangle(warnsdorff_details.x_pos + warnsdorff_details.width - (x_axis // 100) * 5,
                                      (y_axis // 10) * 5, (x_axis // 100) * 5, y_axis // 20, pg,
                                      button_color, button_text_color, hover_button_color)
# Buttons to decrease/increase number of columns
col_down_details = Components.Rectangle((x_axis // 10) * 5.5, (y_axis // 10) * 7, (x_axis // 100) * 5, y_axis // 20, pg,
                                        button_color, button_text_color, hover_button_color)
col_up_details = Components.Rectangle(warnsdorff_details.x_pos + warnsdorff_details.width - (x_axis // 100) * 5,
                                      (y_axis // 10) * 7, (x_axis // 100) * 5, y_axis // 20, pg,
                                      button_color, button_text_color, hover_button_color)
# Buttons to decrease/increase FPS
fps_down_button = Components.Rectangle((x_axis // 10) * 5.5, (y_axis // 10) * 9, (x_axis // 100) * 5, y_axis // 20, pg,
                                       button_color, button_text_color, hover_button_color)
fps_up_button = Components.Rectangle(warnsdorff_details.x_pos + warnsdorff_details.width - (x_axis // 100) * 5,
                                     (y_axis // 10) * 9, (x_axis // 100) * 5, y_axis // 20, pg,
                                     button_color, button_text_color, hover_button_color)

# Button text color
start_text = BUTTON_FONT.render("Start", True, start_details.text_color)
pause_text = BUTTON_FONT.render("Pause", True, start_details.text_color)
reset_text = BUTTON_FONT.render("Reset", True, reset_details.text_color)
quit_text = BUTTON_FONT.render("Quit", True, quit_details.text_color)
backtrack_text = BUTTON_FONT.render("Backtrack Method", True, backtrack_details.text_color)
warnsdorff_text = BUTTON_FONT.render("Warnsdoff's Method", True, warnsdorff_details.text_color)
row_down_text = BUTTON_FONT.render("-1", True, row_down_details.text_color)
row_up_text = BUTTON_FONT.render("+1", True, row_up_details.text_color)
col_down_text = BUTTON_FONT.render("-1", True, col_down_details.text_color)
col_up_text = BUTTON_FONT.render("+1", True, col_up_details.text_color)
fps_down_text = BUTTON_FONT.render("-5", True, fps_down_button.text_color)
fps_up_text = BUTTON_FONT.render("+10", True, fps_up_button.text_color)

# Center the text in their buttons
start_text_rect = start_text.get_rect(
    center=(start_details.x_pos + (start_details.width // 2),
            start_details.y_pos + (start_details.height // 2))
)
reset_text_rect = reset_text.get_rect(
    center=(reset_details.x_pos + (reset_details.width // 2),
            reset_details.y_pos + (reset_details.height // 2))
)
quit_text_rect = quit_text.get_rect(
    center=(quit_details.x_pos + (quit_details.width // 2),
            quit_details.y_pos + (quit_details.height // 2))
)
backtrack_text_rect = backtrack_text.get_rect(
    center=(backtrack_details.x_pos + (backtrack_details.width // 2),
            backtrack_details.y_pos + (backtrack_details.height // 2))
)
warnsdorff_text_rect = warnsdorff_text.get_rect(
    center=(warnsdorff_details.x_pos + (warnsdorff_details.width // 2),
            warnsdorff_details.y_pos + (warnsdorff_details.height // 2))
)
row_down_text_rect = row_down_text.get_rect(
    center=(row_down_details.x_pos + (row_down_details.width // 2),
            row_down_details.y_pos + (row_down_details.height //2))
)
row_up_text_rect = row_up_text.get_rect(
    center=(row_up_details.x_pos + (row_up_details.width // 2),
            row_up_details.y_pos + (row_up_details.height //2))
)
col_down_text_rect = col_down_text.get_rect(
    center=(col_down_details.x_pos + (col_down_details.width // 2),
            col_down_details.y_pos + (col_down_details.height //2))
)
col_up_text_rect = col_up_text.get_rect(
    center=(col_up_details.x_pos + (col_up_details.width // 2),
            col_up_details.y_pos + (col_up_details.height //2))
)
fps_down_text_rect = fps_down_text.get_rect(
    center=(fps_down_button.x_pos + (fps_down_button.width // 2),
            fps_down_button.y_pos + (fps_down_button.height // 2))
)
fps_up_text_rect = fps_up_text.get_rect(
    center=(fps_up_button.x_pos + (fps_up_button.width // 2),
            fps_up_button.y_pos + (fps_up_button.height // 2))
)

# Game text under the chessboard
text_color = (0, 0, 0)
under_board_text = Components.Rectangle(50, 50 + BOARD_SIZE[1], BOARD_SIZE[0], 1.5 * BOARD_SIZE[1] // 8, pg,
                                        BACKGROUND_COLOUR, text_color)
under_board_rect = under_board_text.rect

# Area to display row number text
row_details = Components.Rectangle((x_axis // 10) * 5.5, (y_axis // 10) * 5, (x_axis // 10) * 2, y_axis // 20, pg,
                                   button_color, text_color)
row_text = BUTTON_FONT.render("Rows", True, row_details.text_color)
row_text_rect = row_text.get_rect(
    center=(row_details.x_pos + (row_details.width // 2),
            row_details.y_pos + (row_details.height // 2))
)

# Area to display column number text
col_details = Components.Rectangle((x_axis // 10) * 5.5, (y_axis // 10) * 7, (x_axis // 10) * 2, y_axis // 20, pg,
                                   button_color, text_color)
col_text = BUTTON_FONT.render("Columns", True, col_details.text_color)
col_text_rect = col_text.get_rect(
    center=(col_details.x_pos + (col_details.width // 2),
            col_details.y_pos + (col_details.height // 2))
)

# Area to display FPS text
fps_details = Components.Rectangle((x_axis // 10) * 5.5, (y_axis // 10) * 9, (x_axis // 10) * 2, y_axis // 20, pg,
                                   button_color, text_color)
fps_text = BUTTON_FONT.render("FPS", True, fps_details.text_color)
fps_text_rect = fps_text.get_rect(
    center=(fps_details.x_pos + (fps_details.width // 2),
            fps_details.y_pos + (fps_details.height // 2))
)

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


# Replaces cursor with a knight image
# knight_cursor = pg.image.load("knight_piece.png")

# class Cell:
#     def __init__(self):
#         self.color = None
#         self.traversed = -1
#         self.refresh = False

def update_below_board_text(text, extra_text=None):
    """
    Used to update the text box below the board.
    :param text: The string to be displayed underneath the board
    :param extra_text: Extra info to be displayed below text
    :return:
    """
    global under_board_text, under_board_rect
    under_board_line_1_text = TEXT_FONT.render(text, True, under_board_line_details.text_color)
    under_board_line_1_text_rect = under_board_line_1_text.get_rect(
        center=(under_board_line_details.x_pos + (under_board_line_details.width // 2),
                under_board_line_details.y_pos + (under_board_line_details.height // 5))
    )
    pg.draw.rect(SCREEN, under_board_line_details.color, under_board_rect)
    SCREEN.blit(under_board_line_1_text, under_board_line_1_text_rect)
    if extra_text is not None:
        under_board_line_2_text = TEXT_FONT.render(extra_text, True, under_board_line_details.text_color)
        under_board_line_2_text_rect = under_board_line_2_text.get_rect(
            center=(under_board_line_details.x_pos + (under_board_line_details.width // 2),
                    under_board_line_details.y_pos + (under_board_line_details.height // 2))
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
        self.move_font_size = pg.font.SysFont("Arial", 20)


class Board:
    def __init__(self, knight: Knight, row_dimension=8, col_dimension=8):
        self.knight = knight
        self.board_size = ((y_axis // 10) * row_dimension, (y_axis // 10) * col_dimension)  # Size of board
        self.row_dimension = row_dimension
        self.col_dimension = col_dimension
        self.graph = np.negative(np.ones([row_dimension, col_dimension], dtype=int))
        self.sq_x_length = BOARD_SIZE[0] // col_dimension
        self.sq_y_length = BOARD_SIZE[0] // row_dimension

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
            self.knight.move_font_size = pg.font.SysFont("Arial", self.sq_x_length // 4)
        else:
            self.knight.move_font_size = pg.font.SysFont("Arial", self.sq_y_length // 4)
        self.knight.knight_img = pg.transform.scale(self.knight.knight_img, (self.sq_x_length*0.8, self.sq_y_length*0.8))
        self.draw_board()

    def decrease_row(self):
        if self.row_dimension <= 3:
            return
        self.row_dimension -= 1
        self.graph = np.negative(np.ones([self.row_dimension, self.col_dimension], dtype=int))
        self.check_dimensions_then_draw()

    def increase_row(self):
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
                self.draw_number(row, col)

    def draw_number(self, row, col):
        """
        This function is responsible for drawing the numbers of the steps made by the knight
        :param row: Row number of board
        :param col: Column number of board
        :return:None
        """
        furthest_node = self.graph.max()
        if (self.graph[row][col] != -1 and self.graph[row][col] != furthest_node) \
                or self.graph[row][col] == self.row_dimension * self.col_dimension:
            stamp = ((col * self.sq_x_length) + OFFSET[0] + self.sq_x_length // 2,
                     (row * self.sq_y_length) + OFFSET[1] + self.sq_y_length // 2)
            # print((row, col), "stamp = ", stamp)
            if self.sq_x_length < self.sq_y_length:
                pg.draw.circle(SCREEN, (255, 0, 0), stamp, self.sq_x_length // 4)
            else:
                pg.draw.circle(SCREEN, (255, 0, 0), stamp, self.sq_y_length // 4)
            number = self.graph[row][col]
            SCREEN.blit(self.knight.move_font_size.render(f"{number: 03d}", True, (0, 0, 0)),
                        (stamp[0] - self.sq_x_length * 0.14, stamp[1] - self.sq_y_length * 0.13))


class ChessState:
    def __init__(self, board: Board):
        # Initialise board array. Board is n x n matrix
        self.board = board
        # State of chessboard (start, ready, touring, fail, pause)
        self.state = "start"
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
        self.tours = 0
        # Display text underneath board
        update_below_board_text(f"{self.tour_type} Algorithm at {self.fps} FPS")

    def reset_board(self):
        self.board.graph = np.negative(np.ones([8, 8], dtype=int))
        self.board.row_dimension = 8
        self.board.col_dimension = 8
        self.state = "start"
        self.tour_failures = 0
        self.tour_found = False
        self.board.knight.knight_placed = False
        self.board.knight.knight_initial_pos = None
        self.board.knight.knight_pos = None
        self.board.knight.knight_step = 1
        self.board.knight.move_log = []
        self.board.knight.steps_done = 0
        self.board.board_size = ((y_axis // 10) * 8, (y_axis // 10) * 8)  # Size of board
        self.board.sq_x_length = BOARD_SIZE[0] // 8
        self.board.sq_y_length = BOARD_SIZE[0] // 8
        self.time_start = 0.0
        self.duration = 0.0
        SCREEN.fill(BACKGROUND_COLOUR)
        self.board.draw_board()
        update_below_board_text(f"{self.tour_type} Algorithm at {self.fps} FPS")

    def redo_tour(self):
        self.state = "touring"
        self.board.graph = np.negative(np.ones([self.board.row_dimension, self.board.col_dimension], dtype=int))
        self.board.graph[self.board.knight.knight_initial_pos[0]][self.board.knight.knight_initial_pos[1]] = 1
        self.board.knight.knight_step = 1
        self.board.knight.move_log = [(self.board.knight.knight_initial_pos[0], self.board.knight.knight_initial_pos[1], 0)]
        self.board.knight.knight_pos = self.board.knight.knight_initial_pos
        self.time_start = datetime.now()
        self.board.knight.steps_done = 0
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
                self.board.draw_number(self.board.knight.knight_pos[0], self.board.knight.knight_pos[1])
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
        global fps_up_text, fps_down_text
        if self.fps < 10:
            self.fps += 1
        elif self.fps < 30:
            self.fps += 5
        elif self.fps < 60:
            self.fps += 10
        self.check_fps()

    def decrease_fps(self):
        global fps_down_text, fps_up_text
        if self.fps > 30:
            self.fps -= 10
        elif self.fps > 10:
            self.fps -= 5
        elif self.fps > 1:
            self.fps -= 1
        self.check_fps()

    def check_fps(self):
        global fps_down_text, fps_up_text
        if self.fps == 30:
            fps_down_text = BUTTON_FONT.render("-5", True, fps_down_button.text_color)
            fps_up_text = BUTTON_FONT.render("+10", True, fps_up_button.text_color)
        elif 10 < self.fps < 30:
            fps_down_text = BUTTON_FONT.render("-5", True, fps_down_button.text_color)
            fps_up_text = BUTTON_FONT.render("+5", True, fps_up_button.text_color)
        elif 1 < self.fps < 10:
            fps_down_text = BUTTON_FONT.render("-1", True, fps_down_button.text_color)
            fps_up_text = BUTTON_FONT.render("+1", True, fps_up_button.text_color)
        elif 30 < self.fps < 60:
            fps_down_text = BUTTON_FONT.render("-10", True, fps_down_button.text_color)
            fps_up_text = BUTTON_FONT.render("+10", True, fps_up_button.text_color)

    # Checks if user selected the same square twice. If so, remove the knight
    def place_first_knight(self, selected_sq):
        if not (self.state == "start" or self.state == "ready"):
            return
        row = selected_sq[0]
        col = selected_sq[1]
        # Checks if user selected the same square twice. If so, remove the knight
        if selected_sq == self.board.knight.knight_pos:
            # print("Same Square")
            self.board.draw_square(self.board.knight.knight_pos[0], self.board.knight.knight_pos[1])
            self.board.graph[row][col] = -1
            self.board.knight.knight_placed = False
            self.board.knight.knight_pos = None
            self.board.knight.knight_initial_pos = None
            self.state = "start"
            self.board.knight.move_log.pop()
        elif not self.board.knight.knight_placed:
            self.board.knight.knight_placed = True
            self.board.knight.knight_pos = (row, col)
            self.board.knight.knight_initial_pos = (row, col)
            self.board.graph[row][col] = 1
            self.state = "ready"
            self.board.draw_knight(self.board.sq_x_length, self.board.sq_y_length)
            self.board.knight.move_log.append((row, col, 0))
        elif self.board.knight.knight_placed:
            self.board.knight.move_log.pop()
            self.board.graph[self.board.knight.knight_pos[0]][self.board.knight.knight_pos[1]] = -1
            self.board.draw_square(self.board.knight.knight_pos[0], self.board.knight.knight_pos[1])
            self.board.knight.knight_pos = (row, col)
            self.board.knight.knight_initial_pos = (row, col)
            self.board.graph[row][col] = 1
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
            pg.draw.line(SCREEN, (255, 0, 0), line_start_point, line_end_point, 5)
            i += 1

    # Handles mouse input
    def check_event(self):
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.tour_type == pg.QUIT or (event.tour_type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.running = False
            # Checks if mouse click is on a component
            elif event.tour_type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                # On board area
                if OFFSET[0] < mouse_pos[0] < OFFSET[0] + self.board.board_size[0] and \
                        OFFSET[1] < mouse_pos[1] < OFFSET[1] + self.board.board_size[1]:
                    row = (mouse_pos[1] - OFFSET[1]) // self.board.sq_y_length
                    col = (mouse_pos[0] - OFFSET[0]) // self.board.sq_x_length
                    sq_selected = (row, col)
                    self.place_first_knight(sq_selected)
                # On Start Button. To start the tour
                elif start_details.x_pos <= mouse_pos[0] <= start_details.x_pos + start_details.width \
                        and start_details.y_pos <= mouse_pos[1] <= start_details.y_pos + start_details.height \
                        and self.board.knight.knight_placed and not self.tour_found:
                    if self.state == "ready":
                        self.state = "touring"
                        self.time_start = datetime.now()
                        try:
                            fo = open(f"Simulations/{self.tour_type}_ui_times.csv", 'w')
                            fo.write("position_x,position_y,time\n")
                            fo.close()
                        except Exception as e:
                            print(e)
                    elif self.state == "touring":
                        self.state = "pause"
                        self.duration += (datetime.now() - self.time_start).total_seconds()
                    elif self.state == "pause":
                        self.state = "touring"
                        self.time_start = datetime.now()
                # On Reset Button. Resets the board
                elif reset_details.x_pos <= mouse_pos[0] <= reset_details.x_pos + reset_details.width \
                        and reset_details.y_pos <= mouse_pos[1] <= reset_details.y_pos + reset_details.height:
                    self.reset_board()
                # Quit Button. Stops the game
                elif quit_details.x_pos <= mouse_pos[0] <= quit_details.x_pos + quit_details.width \
                        and quit_details.y_pos <= mouse_pos[1] <= quit_details.y_pos + quit_details.height:
                    self.running = False
                # On Backtrack Button. Change the tour finding method to backtracking
                elif backtrack_details.x_pos <= mouse_pos[0] <= backtrack_details.x_pos + backtrack_details.width \
                        and backtrack_details.y_pos <= mouse_pos[1] <= backtrack_details.y_pos + backtrack_details.height \
                        and (self.state == "start" or self.state == "ready"):
                    self.tour_type = "Backtrack"
                    # Display text underneath board
                    update_below_board_text(f"{self.tour_type} Algorithm at {self.fps} FPS")
                # On Warnsdorff Button. Change the tour finding method to Warnsdorff
                elif warnsdorff_details.x_pos <= mouse_pos[0] <= warnsdorff_details.x_pos + warnsdorff_details.width \
                        and warnsdorff_details.y_pos <= mouse_pos[1] <= warnsdorff_details.y_pos + warnsdorff_details.height \
                        and (self.state == "start" or self.state == "ready"):
                    self.tour_type = "Warnsdorff"
                    # Display text underneath board
                    update_below_board_text(f"{self.tour_type} Algorithm at {self.fps} FPS")
                # On decrease row button.
                elif row_down_details.x_pos <= mouse_pos[0] <= row_down_details.x_pos + row_down_details.width \
                        and row_down_details.y_pos <= mouse_pos[1] <= row_down_details.y_pos + row_down_details.height \
                        and self.state == "start":
                    self.board.decrease_row()
                # On increase row button.
                elif row_up_details.x_pos <= mouse_pos[0] <= row_up_details.x_pos + row_up_details.width \
                        and row_up_details.y_pos <= mouse_pos[1] <= row_up_details.y_pos + row_up_details.height \
                        and self.state == "start":
                    self.board.increase_row()
                # On decrease column button.
                elif col_down_details.x_pos <= mouse_pos[0] <= col_down_details.x_pos + col_down_details.width \
                        and col_down_details.y_pos <= mouse_pos[1] <= col_down_details.y_pos + col_down_details.height \
                        and self.state == "start":
                    self.board.decrease_col()
                # On increase column button.
                elif col_up_details.x_pos <= mouse_pos[0] <= col_up_details.x_pos + col_up_details.width \
                        and col_up_details.y_pos <= mouse_pos[1] <= col_up_details.y_pos + col_up_details.height \
                        and self.state == "start":
                    self.board.increase_col()
                # On decrease FPS button.
                elif fps_down_button.x_pos <= mouse_pos[0] <= fps_down_button.x_pos + fps_down_button.width \
                        and fps_down_button.y_pos <= mouse_pos[1] <= fps_down_button.y_pos + fps_down_button.height:
                    self.decrease_fps()
                    update_below_board_text(f"{self.tour_type} Algorithm at {self.fps} FPS")
                # On increase FPS button.
                elif fps_up_button.x_pos <= mouse_pos[0] <= fps_up_button.x_pos + fps_up_button.width \
                        and fps_down_button.y_pos <= mouse_pos[1] <= fps_up_button.y_pos + fps_up_button.height:
                    self.increase_fps()
                    update_below_board_text(f"{self.tour_type} Algorithm at {self.fps} FPS")
        self.display_components(mouse_pos)
        pg.display.update()

    def display_components(self, mouse_pos):
        # Draw the buttons and text
        # Display Start/Pause button
        if start_details.x_pos <= mouse_pos[0] <= start_details.x_pos + start_details.width \
                and start_details.y_pos <= mouse_pos[1] <= start_details.y_pos + start_details.height:
            pg.draw.rect(SCREEN, hover_button_color, start_details.rect)
        else:
            pg.draw.rect(SCREEN, button_color, start_details.rect)
        # SCREEN.blit(start_text, (start_details.x_pos + (5*start_details.width//10), start_details.y_pos + 5))
        if self.state == "touring":
            SCREEN.blit(pause_text, start_text_rect)
        else:
            SCREEN.blit(start_text, start_text_rect)
        # Display Reset button
        if reset_details.x_pos <= mouse_pos[0] <= reset_details.x_pos + reset_details.width \
                and reset_details.y_pos <= mouse_pos[1] <= reset_details.y_pos + reset_details.height:
            pg.draw.rect(SCREEN, hover_button_color, reset_details.rect)
        else:
            pg.draw.rect(SCREEN, button_color, reset_details.rect)
        # SCREEN.blit(reset_text, (reset_details.x_pos + (3.5*reset_details.width//10), reset_details.y_pos + 5))
        SCREEN.blit(reset_text, reset_text_rect)
        # Display Quit button
        if quit_details.x_pos <= mouse_pos[0] <= quit_details.x_pos + quit_details.width \
                and quit_details.y_pos <= mouse_pos[1] <= quit_details.y_pos + quit_details.height:
            pg.draw.rect(SCREEN, hover_button_color, quit_details.rect)
        else:
            pg.draw.rect(SCREEN, button_color, quit_details.rect)
        # SCREEN.blit(quit_text, (quit_details.x_pos + (4 * quit_details.width // 10), quit_details.y_pos + 5))
        SCREEN.blit(quit_text, quit_text_rect)
        # Sets visibility of knight's tour buttons
        if self.tour_type == "Warnsdorff":
            # Display Backtrack button
            if backtrack_details.x_pos <= mouse_pos[0] <= backtrack_details.x_pos + backtrack_details.width \
                    and backtrack_details.y_pos <= mouse_pos[1] <= backtrack_details.y_pos + backtrack_details.height:
                pg.draw.rect(SCREEN, hover_button_color, backtrack_details.rect)
            else:
                pg.draw.rect(SCREEN, button_color, backtrack_details.rect)
            SCREEN.blit(backtrack_text, backtrack_text_rect)
            # Remove Warnsdorff button
            pg.draw.rect(SCREEN, BACKGROUND_COLOUR, warnsdorff_details.rect)
        elif self.tour_type == "Backtrack":
            # Display Warnsdorff button
            if warnsdorff_details.x_pos <= mouse_pos[0] <= warnsdorff_details.x_pos + warnsdorff_details.width \
                    and warnsdorff_details.y_pos <= mouse_pos[1] <= warnsdorff_details.y_pos + warnsdorff_details.height:
                pg.draw.rect(SCREEN, hover_button_color, warnsdorff_details.rect)
            else:
                pg.draw.rect(SCREEN, button_color, warnsdorff_details.rect)
            SCREEN.blit(warnsdorff_text, warnsdorff_text_rect)
            # Remove Backtrack button
            pg.draw.rect(SCREEN, BACKGROUND_COLOUR, backtrack_details.rect)
        # Display row decrease button
        if row_down_details.x_pos <= mouse_pos[0] <= row_down_details.x_pos + row_down_details.width \
                and row_down_details.y_pos <= mouse_pos[1] <= row_down_details.y_pos + row_down_details.height:
            pg.draw.rect(SCREEN, hover_button_color, row_down_details.rect)
        else:
            pg.draw.rect(SCREEN, button_color, row_down_details.rect)
        SCREEN.blit(row_down_text, row_down_text_rect)
        # Display row increase button
        if row_up_details.x_pos <= mouse_pos[0] <= row_up_details.x_pos + row_up_details.width \
                and row_up_details.y_pos <= mouse_pos[1] <= row_up_details.y_pos + row_up_details.height:
            pg.draw.rect(SCREEN, hover_button_color, row_up_details.rect)
        else:
            pg.draw.rect(SCREEN, button_color, row_up_details.rect)
        SCREEN.blit(row_up_text, row_up_text_rect)
        # Display row text
        SCREEN.blit(row_text, row_text_rect)
        # Display column decrease button
        if col_down_details.x_pos <= mouse_pos[0] <= col_down_details.x_pos + col_down_details.width \
                and col_down_details.y_pos <= mouse_pos[1] <= col_down_details.y_pos + col_down_details.height:
            pg.draw.rect(SCREEN, hover_button_color, col_down_details.rect)
        else:
            pg.draw.rect(SCREEN, button_color, col_down_details.rect)
        SCREEN.blit(col_down_text, col_down_text_rect)
        # Display column increase button
        if col_up_details.x_pos <= mouse_pos[0] <= col_up_details.x_pos + col_up_details.width \
                and col_up_details.y_pos <= mouse_pos[1] <= col_up_details.y_pos + col_up_details.height:
            pg.draw.rect(SCREEN, hover_button_color, col_up_details.rect)
        else:
            pg.draw.rect(SCREEN, button_color, col_up_details.rect)
        SCREEN.blit(col_up_text, col_up_text_rect)
        # Display column text
        SCREEN.blit(col_text, col_text_rect)
        # Display fps decrease button
        if fps_down_button.x_pos <= mouse_pos[0] <= fps_down_button.x_pos + fps_down_button.width \
                and fps_down_button.y_pos <= mouse_pos[1] <= fps_down_button.y_pos + fps_down_button.height:
            pg.draw.rect(SCREEN, hover_button_color, fps_down_button.rect)
        else:
            pg.draw.rect(SCREEN, button_color, fps_down_button.rect)
        SCREEN.blit(fps_down_text, fps_down_text_rect)
        # Display fps increase button
        if fps_up_button.x_pos <= mouse_pos[0] <= fps_up_button.x_pos + fps_up_button.width \
                and fps_up_button.y_pos <= mouse_pos[1] <= fps_up_button.y_pos + fps_up_button.height:
            pg.draw.rect(SCREEN, hover_button_color, fps_up_button.rect)
        else:
            pg.draw.rect(SCREEN, button_color, fps_up_button.rect)
        SCREEN.blit(fps_up_text, fps_up_text_rect)
        # Display FPS text
        SCREEN.blit(fps_text, fps_text_rect)

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
            if self.is_valid_move(next_x + self.board.knight.knight_moves[i][0], next_y + self.board.knight.knight_moves[i][1]):
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
                    self.tours += 1
                    self.duration += (datetime.now() - self.time_start).total_seconds()
                    if self.check_if_closed_tour():
                        update_below_board_text(f"Closed Knight's Tour found using {self.tour_type}",
                                                f"({self.board.knight.steps_done} moves in {round(self.duration, 2)} seconds)")
                    else:
                        update_below_board_text(f"Opened Knight's Tour found using {self.tour_type}",
                                                f"({self.board.knight.steps_done} moves in {round(self.duration, 2)} seconds)")
                    try:
                        fo = open(f"Simulations/{self.tour_type}_ui_times.csv", 'a')
                        fo.write(f"{self.board.knight.knight_initial_pos[0]},{self.board.knight.knight_initial_pos[1]},{self.duration}\n")
                        fo.close()
                    except Exception as e:
                        print(e)

                    x = self.board.knight.knight_initial_pos[0]
                    y = self.board.knight.knight_initial_pos[1]
                    self.reset_board()
                    self.board.knight.knight_pos = (x, y)
                    self.board.knight.knight_initial_pos = (x, y)
                    self.board.graph[x][y] = 1
                    self.state = "touring"
                    self.tour_found = False
                    self.board.knight.move_log = [(x, y, 0)]
                    self.time_start = datetime.now()
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
            self.state = "fail"
            self.tour_failures += 1
            if self.tour_failures >= 5:
                update_below_board_text("Warnsdorff algorithm failed to find a tour after 5 tries.", "Stopping the tour")
            return False

        new_x = self.board.knight.knight_pos[0] + self.board.knight.knight_moves[most_empty_index][0]
        new_y = self.board.knight.knight_pos[1] + self.board.knight.knight_moves[most_empty_index][1]
        self.board.knight.knight_step += 1
        self.board.graph[new_x][new_y] = self.board.knight.knight_step
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
                self.board.knight.move_log[-1] = (self.board.knight.knight_pos[0], self.board.knight.knight_pos[1], i + 1)
                self.board.knight.knight_step += 1
                self.board.graph[new_x][new_y] = self.board.knight.knight_step
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
                self.state = "fail"
                return
            self.board.knight.knight_pos = (self.board.knight.move_log[-1][0], self.board.knight.move_log[-1][1])
        self.move_done = True
        self.board.knight.steps_done += 1

    def update_frame(self):
        """
        Process flow that determines the next behaviour of the game state before updating display
        :return:
        """
        if self.state == "touring":
            if self.tour_type == "Warnsdorff":
                if self.tours < 100:
                    self.find_tour()
            elif self.tour_type == "Backtrack":
                if self.tours < 2:
                    self.find_tour()
        if self.state == "fail" and self.tour_type == "Warnsdorff":
            if self.tour_failures <= 5:
                self.redo_tour()
        if self.state == "fail" and self.tour_type == "Backtrack":
            update_below_board_text("Backtrack algorithm failed to find a tour.", "No reason to brute force again.")
        if self.state == "pause":
            pass
        if not self.running:
            # stop = timeit.default_timer()
            # print('Time: ', stop - start, "seconds")
            # print(movement, "Iterations")
            pg.quit()
            sys.exit()
        self.check_event()
        pg.event.pump()

    # def print_solution(self):
    #     '''
    #         A utility function to print Chessboard matrix
    #     '''
    #     for i in range(self.dimensions):
    #         for j in range(self.dimensions):
    #             print(self.board[i][j], end=' ')
    #         print()
    #     print()


def main():
    knight = Knight()
    board = Board(knight)
    chess_state = ChessState(board)
    while True:
        chess_state.update_frame()


if __name__ == "__main__":
    main()
