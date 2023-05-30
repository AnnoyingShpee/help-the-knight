import sys
import pygame as pg
import numpy as np
import random
import json
import ctypes
from ctypes import windll
from datetime import datetime


class Knight:
    def __init__(self):
        self.knight_moves = ((2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1))
        self.knight_initial_pos = None  # The first square that the knight starts on.
        self.knight_pos = None  # The current square that the knight is on.
        self.knight_step = 1  # The furthest step of the knight's tour the knight is on.
        self.move_log = []  # An array storing the squares that the knight has traversed
        self.total_steps = 0  # Total number of times a Knight has moved


class Board:
    # The default size of a chessboard is 8 x 8
    def __init__(self, row_dimension=8, col_dimension=8):
        self.knight = Knight()  # Every board requires a Knight for a knight's tour
        self.row_dimension = row_dimension  # Number of rows in the board
        self.col_dimension = col_dimension  # Number of columns in the board
        # 2D array representation of board
        self.graph = np.zeros([row_dimension, col_dimension], dtype=int)
        # 2D array to store number of times Knight traversed each square
        self.board_moves = np.zeros([row_dimension, col_dimension], dtype=int)



graph = np.zeros([8, 8], dtype=int)

print(graph)


class Rectangle:
    def __init__(self, x_pos, y_pos, width, height, pg, colour=(180, 241, 255), hover_colour=None,
                 text=None, text_colour=None, text_font=None):
        self.x_pos = x_pos  # x-axis position of the top left corner of rectangle
        self.y_pos = y_pos  # y-axis position of the top left corner of rectangle
        self.width = width  # Width of rectangle
        self.height = height  # Height of rectangle
        self.colour = colour  # Colour of rectangle
        self.hover_colour = hover_colour  # Colour of rectangle when mouse hovers over it
        self.text_colour = text_colour  # Colour of text inside rectangle
        self.rect = pg.Rect(x_pos, y_pos, width, height)  # Create Pygame Rect object
        self.text = text  # Text string inside of rectangle
        self.text_font = None  # Font of text. Uses Pygame's SysFont function
        self.text_render = None  # Rendered text object
        self.text_rect = None  # Text Rect object
        # Initialise the Text Rect object if there contains text to be displayed
        if text is not None:
            self.text_font = text_font
            self.text_render = text_font.render(text, True, text_colour)
            # Centers the text in the middle of the Rectangle
            self.text_rect = self.text_render.get_rect(center=(x_pos + (width // 2), y_pos + (height // 2)))

    def change_text(self, text):
        self.text = text
        self.text_render = self.text_font.render(self.text, True, self.text_colour)
        self.text_rect = self.text_render.get_rect(
            center=(self.x_pos + (self.width // 2), self.y_pos + (self.height // 2))
        )

