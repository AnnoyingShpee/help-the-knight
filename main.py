# Python3 program to solve Knight Tour problem using Backtracking or Warnsdorff
import sys
import pygame as pg
import numpy as np
import random
import timeit
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
BOARD_FONT = pg.font.SysFont('Arial', 20)  # Font for numbering the steps
TEXT_FONT = pg.font.SysFont('Arial', 30)  # Font for text
# DEFAULT_CURSOR = pg.mouse.get_cursor()
FPS = 60
clock = pg.time.Clock()

# start_button = pg.Rect(600, 50, 230, 40)
# reset_button = pg.Rect(600, 170, 230, 40)
# backtrack_button = pg.Rect(600, 290, 230, 40)
# warnsdorff_button = pg.Rect(600, 410, 230, 40)
# quit_button = pg.Rect(600, 530, 230, 40)

# Buttons
button_text_color = (255, 255, 255)
button_color = (100, 100, 100)  # Default button color
hover_button_color = (170, 170, 170)  # Color of button when cursor hovers over
# Play, Reset, and Quit buttons in one group
# Button(x_pos, y_pos, width, height, button_colour, hover_colour, button_text_colour)
start_details = Components.Square((x_axis // 10) * 8, (y_axis // 10) * 2, (x_axis // 100) * 15, y_axis // 20, pg,
                                  button_color, button_text_color, hover_button_color)
reset_details = Components.Square((x_axis // 10) * 8, (y_axis // 10) * 4, (x_axis // 100) * 15, y_axis // 20, pg,
                                  button_color, button_text_color, hover_button_color)
quit_details = Components.Square((x_axis // 10) * 8, (y_axis // 10) * 6, (x_axis // 100) * 15, y_axis // 20, pg,
                                 button_color, button_text_color, hover_button_color)
# Touring type buttons in another group
backtrack_details = Components.Square((x_axis // 10) * 5.5, (y_axis // 10), (x_axis // 10) * 2, y_axis // 20, pg,
                                      button_color, button_text_color, hover_button_color)
warnsdorff_details = Components.Square((x_axis // 10) * 5.5, (y_axis // 10) * 3, (x_axis // 10) * 2, y_axis // 20, pg,
                                       button_color, button_text_color, hover_button_color)
# Buttons to change FPS
fps_down_details = Components.Square((x_axis // 10) * 5.5, (y_axis // 10) * 7, (x_axis // 100) * 5, y_axis // 20, pg,
                                     button_color, button_text_color, hover_button_color)
# fps_up_details = Components.Square((x_axis // 10) * 6.5, (y_axis // 10) * 7, (x_axis // 100) * 5, y_axis // 20, pg,
#                                    button_color, button_text_color, hover_button_color)
fps_up_details = Components.Square(warnsdorff_details.x_pos+warnsdorff_details.width - (x_axis // 100) * 5,
                                   (y_axis // 10) * 7, (x_axis // 100) * 5, y_axis // 20, pg,
                                   button_color, button_text_color, hover_button_color)

start_button = start_details.rect
reset_button = reset_details.rect
quit_button = quit_details.rect
backtrack_button = backtrack_details.rect
warnsdorff_button = warnsdorff_details.rect
fps_down_button = fps_down_details.rect
fps_up_button = fps_up_details.rect

# Button text color
start_text = BUTTON_FONT.render("Start", True, start_details.text_color)
reset_text = BUTTON_FONT.render("Reset", True, reset_details.text_color)
quit_text = BUTTON_FONT.render("Quit", True, quit_details.text_color)
backtrack_text = BUTTON_FONT.render("Backtrack Method", True, backtrack_details.text_color)
warnsdorff_text = BUTTON_FONT.render("Warnsdoff's Method", True, warnsdorff_details.text_color)
fps_down_text = BUTTON_FONT.render("-5", True, fps_down_details.text_color)
fps_up_text = BUTTON_FONT.render("+10", True, fps_up_details.text_color)

# Center the text in their buttons
start_text_rect = start_text.get_rect(
    center=(start_details.x_pos + (start_details.width//2),
            start_details.y_pos + (start_details.height//2))
)
reset_text_rect = reset_text.get_rect(
    center=(reset_details.x_pos + (reset_details.width//2),
            reset_details.y_pos + (reset_details.height//2))
)
quit_text_rect = quit_text.get_rect(
    center=(quit_details.x_pos + (quit_details.width//2),
            quit_details.y_pos + (quit_details.height//2))
)
backtrack_text_rect = backtrack_text.get_rect(
    center=(backtrack_details.x_pos + (backtrack_details.width//2),
            backtrack_details.y_pos + (backtrack_details.height//2))
)
warnsdorff_text_rect = warnsdorff_text.get_rect(
    center=(warnsdorff_details.x_pos + (warnsdorff_details.width//2),
            warnsdorff_details.y_pos + (warnsdorff_details.height//2))
)
fps_down_text_rect = fps_down_text.get_rect(
    center=(fps_down_details.x_pos + (fps_down_details.width//2),
            fps_down_details.y_pos + (fps_down_details.height//2))
)
fps_up_text_rect = fps_up_text.get_rect(
    center=(fps_up_details.x_pos + (fps_up_details.width//2),
            fps_up_details.y_pos + (fps_up_details.height//2))
)

# Game text under the chessboard
text_color = (0, 0, 0)
under_board_details = Components.Square(50, 50+BOARD_SIZE[1], BOARD_SIZE[0], BOARD_SIZE[1]//8, pg, BACKGROUND_COLOUR, text_color)
under_board_rect = under_board_details.rect
under_board_text = TEXT_FONT.render("Backtrack Method at 30 FPS", True, under_board_details.text_color)
board_text_rect = under_board_text.get_rect(
    center=(under_board_details.x_pos+(under_board_details.width//2),
            under_board_details.y_pos+(under_board_details.height//2))
)
# Area to display FPS text
fps_details = Components.Square((x_axis // 10) * 5.5, (y_axis // 10) * 7, (x_axis // 10) * 2, y_axis // 20, pg,
                                button_color, text_color)
fps_text = BUTTON_FONT.render("FPS", True, fps_details.text_color)
fps_text_rect = fps_text.get_rect(
    center=(fps_details.x_pos+(fps_details.width//2),
            fps_details.y_pos+(fps_details.height//2))
)
# fps_text_rect = fps_text.get_rect(center=(fps_details.x_pos + fps_details.x_pos + ))

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

# class Cell:
#     def __init__(self):
#         self.color = None
#         self.traversed = -1
#         self.refresh = False

class Board:
    def __init__(self, dimension):
        self.dimension = dimension
        self.graph = np.negative(np.ones([dimension, dimension], dtype=int))


    def draw_board(self):
        # Draw chessboard. Top left square is always light color
        for row in range(self.dimension):
            for col in range(self.dimension):
                color = BOARD_COLORS[(row + col) % 2]
                pg.draw.rect(SCREEN, color,
                             # x-axis = column (left to right) , y-axis = row (top to bottom)
                             # Draw the starting point of the square
                             # Add off set if chessboard not touching the border of window
                             # SQ_SIZE means the length and width of the squares
                             pg.Rect((col * SQ_SIZE) + OFFSET[0], (row * SQ_SIZE) + OFFSET[1], SQ_SIZE, SQ_SIZE))

    def draw_square(self, row, col):
        color = BOARD_COLORS[(row + col) % 2]
        pg.draw.rect(SCREEN, color, pg.Rect((col * SQ_SIZE) + OFFSET[0], (row * SQ_SIZE) + OFFSET[1], SQ_SIZE, SQ_SIZE))

    def draw_numbers(self):
        for row in range(self.dimension):
            for col in range(self.dimension):
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
                or self.graph[row][col] == self.dimension ** 2:
            stamp = ((col * SQ_SIZE) + OFFSET[0] + SQ_SIZE//2, (row * SQ_SIZE) + OFFSET[1] + SQ_SIZE//2)
            # print((row, col), "stamp = ", stamp)
            pg.draw.circle(SCREEN, (255, 0, 0), stamp, 30)
            number = self.graph[row][col]
            SCREEN.blit(BOARD_FONT.render(f"{number: 03d}", True, (255, 255, 255)),
                        (stamp[0] - SQ_SIZE*0.14, stamp[1] - SQ_SIZE*0.13))



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
    def __init__(self, board: Board, knight: Knight):
        # Initialise board array. Board is n x n matrix
        self.board = board
        self.knight = knight
        # State of chessboard (start, ready, touring, fail)
        self.state = "start"
        self.tour_found = False  # Whether knight tour is found
        self.running = True  # Whether game is running
        self.warnsdorff = False
        self.move_done = False
        self.fps = 30
        self.last_frame_tick = 0
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

    def redraw_board(self):
        if self.move_done and (pg.time.get_ticks() - self.last_frame_tick) > 1000/self.fps:
            furthest_node = self.board.graph.max()
            self.board.draw_board()
            self.draw_lines()
            self.board.draw_numbers()

            # print(furthest_node)
            if furthest_node == self.board.dimension ** 2:
                # print("Draw Number")
                self.board.draw_number(self.knight.knight_pos[0], self.knight.knight_pos[1])
            else:
                # print("Draw Knight")
                SCREEN.blit(knight_piece,
                            pg.Rect((self.knight.knight_pos[1] * SQ_SIZE) + OFFSET[0] + SQ_SIZE // 8,
                                    (self.knight.knight_pos[0] * SQ_SIZE) + OFFSET[1] + SQ_SIZE // 8,
                                    SQ_SIZE, SQ_SIZE)
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
            fps_down_text = BUTTON_FONT.render("-5", True, fps_down_details.text_color)
            fps_up_text = BUTTON_FONT.render("+10", True, fps_up_details.text_color)
        elif 10 < self.fps < 30:
            fps_down_text = BUTTON_FONT.render("-5", True, fps_down_details.text_color)
            fps_up_text = BUTTON_FONT.render("+5", True, fps_up_details.text_color)
        elif 1 < self.fps < 10:
            fps_down_text = BUTTON_FONT.render("-1", True, fps_down_details.text_color)
            fps_up_text = BUTTON_FONT.render("+1", True, fps_up_details.text_color)
        elif 30 < self.fps < 60:
            fps_down_text = BUTTON_FONT.render("-10", True, fps_down_details.text_color)
            fps_up_text = BUTTON_FONT.render("+10", True, fps_up_details.text_color)

    # Checks if user selected the same square twice. If so, remove the knight
    def place_first_knight(self, selected_sq):
        if self.state == "touring":
            return
        row = selected_sq[0]
        col = selected_sq[1]
        # Checks if user selected the same square twice. If so, remove the knight
        if selected_sq == self.knight.knight_pos:
            # print("Same Square")
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
            self.knight.move_log.pop()
            self.board.graph[self.knight.knight_pos[0]][self.knight.knight_pos[1]] = -1
            self.board.draw_square(self.knight.knight_pos[0], self.knight.knight_pos[1])
            self.knight.knight_pos = (row, col)
            self.knight.knight_initial_pos = (row, col)
            self.board.graph[row][col] = 1
            self.knight.move_log.append((row, col, 0))
            self.knight.draw_knight()

    def update_text(self, text_shown):
        """
        Used to update the text box below the board.
        :param text_component: The component for the text
        :param text_shown: The string to be displayed underneath the board
        :return:
        """
        global under_board_text, under_board_details, under_board_rect
        under_board_text = TEXT_FONT.render(text_shown, True, under_board_details.text_color)
        pg.draw.rect(SCREEN, under_board_details.color, under_board_rect)
        SCREEN.blit(under_board_text, board_text_rect)

    def draw_lines(self):
        i = 2
        # print("Moves =", self.knight.move_log)
        while i <= len(self.knight.move_log):
            start_point = self.knight.move_log[i - 2]
            line_start_point = ((start_point[1] * SQ_SIZE) + OFFSET[0] + SQ_SIZE // 2,
                                (start_point[0] * SQ_SIZE) + OFFSET[1] + SQ_SIZE // 2)
            end_point = self.knight.move_log[i - 1]
            line_end_point = ((end_point[1] * SQ_SIZE) + OFFSET[0] + SQ_SIZE // 2,
                              (end_point[0] * SQ_SIZE) + OFFSET[1] + SQ_SIZE // 2)
            pg.draw.line(SCREEN, (255, 0, 0), line_start_point, line_end_point, 5)
            i += 1

    # Handles mouse input
    def check_event(self):
        mouse_pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.running = False
            # Checks if mouse click is on a component
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                # On board area
                if OFFSET[0] < mouse_pos[0] < OFFSET[0] + BOARD_SIZE[0] and \
                   OFFSET[1] < mouse_pos[1] < OFFSET[1] + BOARD_SIZE[1]:
                    row = (mouse_pos[1] - OFFSET[1]) // SQ_SIZE
                    col = (mouse_pos[0] - OFFSET[0]) // SQ_SIZE
                    sq_selected = (row, col)
                    self.place_first_knight(sq_selected)
                # On Start Button. To start the tour
                elif start_details.x_pos <= mouse_pos[0] <= start_details.x_pos + start_details.width \
                    and start_details.y_pos <= mouse_pos[1] <= start_details.y_pos + start_details.height \
                        and self.knight.knight_placed:
                    self.state = "touring"
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
                        and self.state != "touring":
                    self.warnsdorff = False
                    # pg.draw.rect(SCREEN, BACKGROUND_COLOUR, )
                # On Warnsdorff Button. Change the tour finding method to Warnsdorff
                elif warnsdorff_details.x_pos <= mouse_pos[0] <= warnsdorff_details.x_pos + warnsdorff_details.width \
                    and warnsdorff_details.y_pos <= mouse_pos[1] <= warnsdorff_details.y_pos + warnsdorff_details.height \
                        and self.state != "touring":
                    self.warnsdorff = True
                elif fps_down_details.x_pos <= mouse_pos[0] <= fps_down_details.x_pos + fps_down_details.width \
                        and fps_down_details.y_pos <= mouse_pos[1] <= fps_down_details.y_pos + fps_down_details.height:
                    self.decrease_fps()
                elif fps_up_details.x_pos <= mouse_pos[0] <= fps_up_details.x_pos + fps_up_details.width \
                        and fps_down_details.y_pos <= mouse_pos[1] <= fps_up_details.y_pos + fps_up_details.height:
                    self.increase_fps()

        self.display_components(mouse_pos)
        pg.display.update()

    def display_components(self, mouse_pos):
        global under_board_text
        # Draw the buttons and text
        # Display Start button
        if start_details.x_pos <= mouse_pos[0] <= start_details.x_pos + start_details.width \
                and start_details.y_pos <= mouse_pos[1] <= start_details.y_pos + start_details.height:
            pg.draw.rect(SCREEN, hover_button_color, start_button)
        else:
            pg.draw.rect(SCREEN, button_color, start_button)
        # SCREEN.blit(start_text, (start_details.x_pos + (5*start_details.width//10), start_details.y_pos + 5))
        SCREEN.blit(start_text, start_text_rect)
        # Display Reset button
        if reset_details.x_pos <= mouse_pos[0] <= reset_details.x_pos + reset_details.width \
                and reset_details.y_pos <= mouse_pos[1] <= reset_details.y_pos + reset_details.height:
            pg.draw.rect(SCREEN, hover_button_color, reset_button)
        else:
            pg.draw.rect(SCREEN, button_color, reset_button)
        # SCREEN.blit(reset_text, (reset_details.x_pos + (3.5*reset_details.width//10), reset_details.y_pos + 5))
        SCREEN.blit(reset_text, reset_text_rect)
        # Display Quit button
        if quit_details.x_pos <= mouse_pos[0] <= quit_details.x_pos + quit_details.width \
                and quit_details.y_pos <= mouse_pos[1] <= quit_details.y_pos + quit_details.height:
            pg.draw.rect(SCREEN, hover_button_color, quit_button)
        else:
            pg.draw.rect(SCREEN, button_color, quit_button)
        # SCREEN.blit(quit_text, (quit_details.x_pos + (4 * quit_details.width // 10), quit_details.y_pos + 5))
        SCREEN.blit(quit_text, quit_text_rect)
        # Sets visibility of knight's tour buttons
        if self.warnsdorff:
            # Display Backtrack button
            if backtrack_details.x_pos <= mouse_pos[0] <= backtrack_details.x_pos + backtrack_details.width \
                    and backtrack_details.y_pos <= mouse_pos[1] <= backtrack_details.y_pos + backtrack_details.height:
                pg.draw.rect(SCREEN, hover_button_color, backtrack_button)
            else:
                pg.draw.rect(SCREEN, button_color, backtrack_button)
            SCREEN.blit(backtrack_text, backtrack_text_rect)
            # Remove Warnsdorff button
            pg.draw.rect(SCREEN, BACKGROUND_COLOUR, warnsdorff_button)
        else:
            # Display Warnsdorff button
            if warnsdorff_details.x_pos <= mouse_pos[0] <= warnsdorff_details.x_pos + warnsdorff_details.width \
                    and warnsdorff_details.y_pos <= mouse_pos[1] <= warnsdorff_details.y_pos + warnsdorff_details.height:
                pg.draw.rect(SCREEN, hover_button_color, warnsdorff_button)
            else:
                pg.draw.rect(SCREEN, button_color, warnsdorff_button)
            SCREEN.blit(warnsdorff_text, warnsdorff_text_rect)
            # Remove Backtrack button
            pg.draw.rect(SCREEN, BACKGROUND_COLOUR, backtrack_button)
        # Display fps decrease button
        if fps_down_details.x_pos <= mouse_pos[0] <= fps_down_details.x_pos + fps_down_details.width \
                and fps_down_details.y_pos <= mouse_pos[1] <= fps_down_details.y_pos + fps_down_details.height:
            pg.draw.rect(SCREEN, hover_button_color, fps_down_button)
        else:
            pg.draw.rect(SCREEN, button_color, fps_down_button)
        SCREEN.blit(fps_down_text, fps_down_text_rect)
        # Display fps increase button
        if fps_up_details.x_pos <= mouse_pos[0] <= fps_up_details.x_pos + fps_up_details.width \
                and fps_up_details.y_pos <= mouse_pos[1] <= fps_up_details.y_pos + fps_up_details.height:
            pg.draw.rect(SCREEN, hover_button_color, fps_up_button)
        else:
            pg.draw.rect(SCREEN, button_color, fps_up_button)
        SCREEN.blit(fps_up_text, fps_up_text_rect)
        # Display FPS text
        SCREEN.blit(fps_text, fps_text_rect)
        # Display text underneath board
        if self.warnsdorff:
            self.update_text(f"Warnsdorff's Method at {self.fps} FPS")
        else:
            self.update_text(f"Backtrack Method at {self.fps} FPS")
        pg.draw.rect(SCREEN, under_board_details.color, under_board_rect)
        SCREEN.blit(under_board_text, board_text_rect)

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

    def check_if_closed_tour(self):
        if (abs(self.knight.knight_initial_pos[0] - self.knight.knight_pos[0]) == 2
            and abs(self.knight.knight_initial_pos[1] - self.knight.knight_pos[1]) == 1) or \
                (abs(self.knight.knight_initial_pos[0] - self.knight.knight_pos[0]) == 1 and
                 abs(self.knight.knight_initial_pos[1] - self.knight.knight_pos[1]) == 2):
            return True
        else:
            return False

    # def print_solution(self):
    #     '''
    #         A utility function to print Chessboard matrix
    #     '''
    #     for i in range(self.dimensions):
    #         for j in range(self.dimensions):
    #             print(self.board[i][j], end=' ')
    #         print()
    #     print()

    # def find_tour(self):
    #     """
    #     Function chooses the algorithm selected to find the tour
    #     :return:
    #     """
    #     # First checks whether tour has already been found
    #     if not self.tour_found:
    #         # Checks type of algorithm used to find tour
    #         if self.warnsdorff:
    #             if self.knight.knight_step < 64:
    #                 self.find_tour_warnsdorff()
    #             else:
    #                 self.tour_found = True
    #         else:
    #             if len(self.knight.move_log) == 0:
    #                 self.state = "fail"
    #             if self.knight.knight_step < 64:
    #                 self.find_tour_backtrack_iterative()
    #             else:
    #                 self.tour_found = True
    #     self.redraw_board()

    def find_tour(self):
        """
        Function chooses the algorithm selected to find the tour
        :return:
        """
        # First checks whether tour has already been found
        if not self.tour_found:
            if not self.move_done:
                # Checks type of algorithm used to find tour
                if self.warnsdorff:
                    if self.knight.knight_step < 64:
                        self.find_tour_warnsdorff()
                    else:
                        self.tour_found = True
                else:
                    if len(self.knight.move_log) == 0:
                        self.state = "fail"
                    if self.knight.knight_step < 64:
                        self.find_tour_backtrack_iterative()
                    else:
                        self.tour_found = True
        else:
            if self.check_if_closed_tour():
                self.update_text("Closed Knight's Tour found.")
            else:
                self.update_text("Open Knight's Tour found.")


        self.redraw_board()


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
        self.move_done = True

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
                # self.board.draw_square(self.knight.knight_pos[0], self.knight.knight_pos[1])
                # self.draw_line()
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
        self.move_done = True

    def update_frame(self):
        """
        Process flow that determines the next behaviour of the game state before updating display
        :return:
        """
        if self.state == "touring":
            self.find_tour()
        if self.state == "fail":
            self.redo_tour()
        if not self.running:
            # stop = timeit.default_timer()
            # print('Time: ', stop - start, "seconds")
            # print(movement, "Iterations")
            pg.quit()
            sys.exit()
        self.check_event()
        pg.event.pump()


def main():
    board = Board(DIMENSIONS)
    knight = Knight()
    chess_state = ChessState(board, knight)
    while True:
        # clock.tick(FPS)  # Determines the frames per second of game
        chess_state.update_frame()


if __name__ == "__main__":
    # start = timeit.default_timer()
    # chess_state = ChessState(8)
    # chess_state.find_tour()
    start = timeit.default_timer()
    main()
    # stop = timeit.default_timer()
    # print('Time: ', stop - start)
