import sys
import pygame as pg
import numpy as np
import random
import json
import ctypes
from ctypes import windll
from datetime import datetime

sys
random
json
ctypes
windll
datetime
BOARD_SIZE = ((y_axis // 10) * 8, (y_axis // 10) * 8)  # Size of board
OFFSET = (y_axis // 15, y_axis // 15)  # Amount of offset of the board from the border


class Knight:
    def __init__(self):
        self.knight_moves = ((2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1))
        self.knight_placed = False
        self.knight_initial_pos = None
        self.knight_pos = None
        self.knight_step = 1
        self.move_log = []
        self.total_steps = 0
        self.step_font = None


class Board:
    def __init__(self, row_dimension=8, col_dimension=8):
        self.knight = Knight()
        self.board_size = BOARD_SIZE
        self.sq_colours = [pg.Color("white"), pg.Color("grey")]
        self.row_dimension = row_dimension
        self.col_dimension = col_dimension
        self.graph = np.negative(np.ones([row_dimension, col_dimension], dtype=int))
        self.board_moves = np.zeros([row_dimension, col_dimension], dtype=int)
        self.sq_x_length = BOARD_SIZE[0] // col_dimension
        self.sq_y_length = BOARD_SIZE[1] // row_dimension


