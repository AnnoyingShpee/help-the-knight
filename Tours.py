from datetime import datetime
from random import randint
import numpy as np


class Tour:
    def __init__(self, row_dimension, col_dimension, x_pos=None, y_pos=None, tour_type="Backtrack"):
        x = x_pos
        y = y_pos
        if x is None:
            x = randint(0, row_dimension-1)
        if y is None:
            y = randint(0, col_dimension-1)
        self.row_dimension = row_dimension
        self.col_dimension = col_dimension
        self.total_squares = row_dimension * col_dimension
        self.graph = np.negative(np.ones([row_dimension, col_dimension], dtype=int))
        self.moves = np.zeros([row_dimension, col_dimension], dtype=int)
        self.knight_moves = ((2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1))
        self.knight_initial_pos = (x, y)
        self.knight_pos = (x, y)
        self.tour_found = False
        self.knight_step = 1
        self.graph[x][y] = self.knight_step
        self.moves[x][y] = 1
        self.tour_type = tour_type
        self.move_log = [(x, y, 0)]
        self.time_start = 0
        self.duration = 0

    def reset_board(self):
        x = randint(0, self.row_dimension-1)
        y = randint(0, self.col_dimension-1)
        self.graph = np.negative(np.ones([self.row_dimension, self.col_dimension], dtype=int))
        self.tour_found = False
        self.knight_initial_pos = (x, y)
        self.knight_pos = (x, y)
        self.knight_step = 1
        self.graph[x][y] = self.knight_step
        self.moves[x][y] = 1

    def print_tour(self):
        print("--Steps--")
        for i in range(self.row_dimension):
            for j in range(self.col_dimension):
                item = self.graph[i][j]
                print(item, end=' ')
            print()
        print("--Moves--")
        for i in range(self.row_dimension):
            for j in range(self.col_dimension):
                item = self.moves[i][j]
                print(item, end=' ')
            print()
        print("Time taken =", self.duration)
        print('----')

        self.tour_found = False

    def check_if_structured_tour(self):
        row_last_square = self.row_dimension - 1
        row_second_last = row_last_square - 1
        row_third_last = row_second_last - 1
        col_last_square = self.col_dimension - 1
        col_second_last = col_last_square - 1
        col_third_last = col_second_last - 1
        # List of squares to be checked [(Row squares), (Col squares)]
        to_be_checked = [
            # Top left corner
            [(0, 1), (0, 2), (2, 0), (1, 0)],
            # Top right corner
            [(0, col_third_last), (0, col_second_last), (1, col_last_square), (2, col_last_square)],
            # Bottom left corner
            [(row_last_square, 1), (row_last_square, 2), (row_third_last, 0), (row_second_last, 0)],
            # Bottom right corner
            [(row_last_square, col_third_last), (row_last_square, col_second_last),
             (row_second_last, col_last_square), (row_third_last, col_last_square)],
        ]
        for corner in to_be_checked:
            for i in range(2):
                x_1 = corner[i][0]
                y_1 = corner[i][1]
                x_2 = corner[i+2][0]
                y_2 = corner[i+2][1]
                if abs(self.graph[x_1][y_1] - self.graph[x_2][y_2]) != 1:
                    print("Not structured")
                    return False

        return True

    def check_if_closed_tour(self):
        if (abs(self.knight_initial_pos[0] - self.knight_pos[0]) == 2
            and abs(self.knight_initial_pos[1] - self.knight_pos[1]) == 1) or \
                (abs(self.knight_initial_pos[0] - self.knight_pos[0]) == 1 and
                 abs(self.knight_initial_pos[1] - self.knight_pos[1]) == 2):
            return True
        else:
            return False

    def generate_tours(self):
        self.time_start = datetime.now()
        if self.tour_type == "Random":
            print("Random walk tour being made")
            self.find_tour_random_walk()
        elif self.tour_type == "Backtrack Iterative":
            print("Backtrack tour being made")
            self.find_tour_backtrack_iterative()
        elif self.tour_type == "Backtrack Recursive":
            print("Recursive Backtrack tour being made")
            self.find_tour_backtrack_recursive()
        elif self.tour_type == "Warnsdorff":
            print("Warnsdorff tour being made")
            self.find_tour_warnsdorff()
        if self.tour_found:
            self.duration += (datetime.now() - self.time_start).total_seconds()
            self.print_tour()
        self.reset_board()

    def count_empty_squares(self, next_x, next_y):
        count = 0
        for i in range(8):
            if self.is_valid_move(next_x + self.knight_moves[i][0], next_y + self.knight_moves[i][1]):
                count += 1
        return count

    def is_valid_move(self, x, y):
        """
            A utility function to check if i,j are valid indexes
            for N*N chessboard
            :param x: row number of square
            :param y: column number of square
        """
        if 0 <= x < self.row_dimension and 0 <= y < self.col_dimension and self.graph[x][y] == -1:
            return True
        return False

    def do_backtrack_step(self):
        if self.knight_step == (self.row_dimension * self.col_dimension):
            return True

        # Try all next moves from the current coordinate x, y
        for i in range(8):
            new_x = self.knight_pos[0] + self.knight_moves[i][0]
            new_y = self.knight_pos[1] + self.knight_moves[i][1]

            if self.is_valid_move(new_x, new_y):
                self.knight_step += 1
                self.graph[new_x][new_y] = self.knight_step
                self.moves[new_x][new_y] += 1
                self.move_log.append((new_x, new_y, 0))
                self.knight_pos = (new_x, new_y)
                if self.do_backtrack_step():
                    return True
        self.graph[self.knight_pos[0]][self.knight_pos[1]] = -1
        self.move_log.pop()
        self.knight_pos = (self.move_log[-1][0], self.move_log[-1][1])
        self.knight_step -= 1
        return False

    def find_tour_backtrack_recursive(self):
        if not self.do_backtrack_step():
            self.print_tour()
            print("Solution does not exist")
        else:
            self.tour_found = True

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
        while self.knight_step < self.row_dimension * self.col_dimension:
            last_used_square = self.move_log[-1]
            contains_valid = False
            # Checks if the square has valid moves, if so, move to that new square
            for i in range(last_used_square[2], 8):
                new_x = last_used_square[0] + self.knight_moves[i][0]
                new_y = last_used_square[1] + self.knight_moves[i][1]
                if self.is_valid_move(new_x, new_y):
                    # Update the last square of move_log so that the next knight move to check will be the next one
                    # self.board.draw_square(self.knight.knight_pos[0], self.knight.knight_pos[1])
                    # self.draw_line()
                    self.move_log[-1] = (self.knight_pos[0], self.knight_pos[1], i + 1)
                    self.knight_step += 1
                    self.graph[new_x][new_y] = self.knight_step
                    self.moves[new_x][new_y] += 1
                    self.knight_pos = (new_x, new_y)
                    new_pos = (new_x, new_y, 0)
                    self.move_log.append(new_pos)
                    contains_valid = True
                    break
            # If no valid moves can be done, remove square from stack
            if not contains_valid:
                self.graph[self.knight_pos[0]][self.knight_pos[1]] = -1
                self.knight_step -= 1
                self.move_log.pop()
                if len(self.move_log) == 0:
                    self.tour_found = False
                    return False
                self.knight_pos = (self.move_log[-1][0], self.move_log[-1][1])
        self.tour_found = True
        return True

    def find_tour_warnsdorff(self):
        # To give some randomness when choosing a square. Only useful for next squares with the same number of next
        # valid squares
        while self.knight_step < self.row_dimension*self.col_dimension:
            least_empty = 9
            least_empty_index = -1
            random_num = randint(0, 1000) % 8
            for i in range(8):
                index = (random_num + i) % 8
                new_x = self.knight_pos[0] + self.knight_moves[index][0]
                new_y = self.knight_pos[1] + self.knight_moves[index][1]
                empty_sq_count = self.count_empty_squares(new_x, new_y)
                if self.is_valid_move(new_x, new_y) and empty_sq_count < least_empty:
                    least_empty_index = index
                    least_empty = empty_sq_count
            if least_empty_index == -1:
                self.tour_found = False
                print("Fail")
                return False

            new_x = self.knight_pos[0] + self.knight_moves[least_empty_index][0]
            new_y = self.knight_pos[1] + self.knight_moves[least_empty_index][1]
            self.knight_step += 1
            self.graph[new_x][new_y] = self.knight_step
            self.knight_pos = (new_x, new_y)

        self.tour_found = True
        return True

    def find_tour_random_walk(self):
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
        # Checks if the square has valid moves, if so, move to that new square
        while self.knight_step < self.row_dimension*self.col_dimension:
            r = randint(0, 7)
            dx, dy = self.knight_moves[r][0], self.knight_moves[r][1]

            new_x, new_y = self.knight_pos[0] + dx, self.knight_pos[1] + dy

            if self.is_valid_move(new_x, new_y):
                self.knight_pos = (new_x, new_y)
                self.knight_step += 1
                self.graph[new_x][new_y] = self.knight_step

            else:
                self.tour_found = False
                print("Fail")
                return False

        self.tour_found = True
        return True

    def find_tour_divide_and_conquer(self):
        return


tours = Tour(8, 8, 7, 0, "Backtrack Iterative")
tours.generate_tours()



