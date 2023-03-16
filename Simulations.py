from datetime import datetime
from random import randint
import numpy as np


class Tour:
    def __init__(self, row_dimension=8, col_dimension=8, tour_type="Backtrack", pos_x=None, pos_y=None,
                 total_successful_tours=1, save_tours=True, save_time=True):
        x, self.x_rand = pos_x if pos_x is not None else randint(0, row_dimension-1), False if pos_x is not None else True
        y, self.y_rand = pos_y if pos_y is not None else randint(0, col_dimension-1), False if pos_y is not None else True
        self.row_dimension = row_dimension
        self.col_dimension = col_dimension
        self.total_squares = row_dimension * col_dimension
        self.graph = np.negative(np.ones([row_dimension, col_dimension], dtype=int))
        self.knight_moves = ((2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1))
        self.knight_initial_pos = (x, y)
        self.knight_pos = (x, y)
        self.tour_found = False
        self.knight_step = 1
        self.successful_tours = 0
        self.total_successful_tours = total_successful_tours
        self.graph[x][y] = self.knight_step
        self.save_tours = save_tours
        self.save_time = save_time
        self.type = tour_type
        self.move_log = [(x, y, 0)]
        self.state = "fail"
        self.closed_structured_tour_path = f"Tours/{self.type}_closed_structured_tours_{row_dimension}_{col_dimension}.txt"
        self.open_structured_tour_path = f"Tours/{self.type}_opened_structured_tours_{row_dimension}_{col_dimension}.txt"
        self.closed_unstructured_tour_path = f"Tours/{self.type}_closed_unstructured_tours_{row_dimension}_{col_dimension}.txt"
        self.open_unstructured_tour_path = f"Tours/{self.type}_opened_unstructured_tours_{row_dimension}_{col_dimension}.txt"
        self.time_start = datetime.now()
        self.duration = 0
        self.time_path = f"Simulations/{self.type}_times.csv"

        if self.save_tours:
            try:
                fo = open(self.open_structured_tour_path, 'w')
                fo.write("--\n")
                fo.close()

                fc = open(self.closed_structured_tour_path, 'w')
                fc.write("--\n")
                fc.close()

                fo = open(self.open_unstructured_tour_path, 'w')
                fo.write("--\n")
                fo.close()

                fc = open(self.closed_unstructured_tour_path, 'w')
                fc.write("--\n")
                fc.close()

            except Exception as e:
                print(e)

        if self.save_time:
            try:
                ft = open(self.time_path, 'w')
                ft.write("position_x,position_y,time\n")
                ft.close()
            except Exception as e:
                print(e)

    def reset_board(self, touring=False):
        self.graph = np.negative(np.ones([self.row_dimension, self.col_dimension], dtype=int))
        self.graph[self.knight_initial_pos[0]][self.knight_initial_pos[1]] = 1
        self.tour_found = False
        self.knight_step = 1
        self.move_log = [(self.knight_initial_pos[0], self.knight_initial_pos[1], 0)]
        if touring:
            self.knight_pos = (self.knight_initial_pos[0], self.knight_initial_pos[1])
            self.duration += (datetime.now() - self.time_start).total_seconds()
            self.time_start = datetime.now()
        else:
            x = randint(0, self.row_dimension - 1) if self.x_rand else self.knight_initial_pos[0]
            y = randint(0, self.col_dimension - 1) if self.y_rand else self.knight_initial_pos[1]
            self.knight_initial_pos = (x, y)
            self.knight_pos = (x, y)
            self.time_start = datetime.now()
            self.duration = 0


    def print_tour(self, tour_file_path, simulation_file_path):
        for i in range(self.row_dimension):
            for j in range(self.col_dimension):
                item = self.graph[i][j]
                print(item, end=' ')
            print()
        print("--")
        if self.save_tours:
            try:
                file_append = open(tour_file_path, 'a')
                for i in range(self.row_dimension):
                    for j in range(self.col_dimension):
                        item = self.graph[i][j]
                        file_append.write(str(item))
                        file_append.write(' ')
                    file_append.write("\n")
                file_append.write("--\n")
                self.tour_found = False

                file_append = open(simulation_file_path, 'a')
                file_append.write(f"{self.knight_initial_pos[0]},{self.knight_initial_pos[1]},{self.duration}\n")
            except Exception as ex:
                print(ex)
        else:
            try:
                file_append = open(simulation_file_path, 'a')
                file_append.write(f"{self.knight_initial_pos[0]},{self.knight_initial_pos[1]},{self.duration}\n")
            except Exception as ex:
                print(ex)

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

    # Count the number of steps in one random tour
    def generate_tours(self):
        while self.successful_tours < self.total_successful_tours:
            self.time_start = datetime.now()
            if self.type == "Random":
                print("Random walk tour being made")
                self.find_tour_random_walk()
            elif self.type == "Backtrack":
                print("Backtrack tour being made")
                self.find_tour_backtrack_iterative()
            elif self.type == "Warnsdorff":
                print("Warnsdorff tour being made")
                self.find_tour_warnsdorff()
            if self.tour_found:
                self.duration = (datetime.now() - self.time_start).total_seconds()
                if self.check_if_structured_tour():
                    if self.check_if_closed_tour():
                        self.print_tour(self.closed_structured_tour_path, self.time_path)
                        self.successful_tours += 1
                    else:
                        self.print_tour(self.open_structured_tour_path, self.time_path)
                        self.successful_tours += 1
                else:
                    if self.check_if_closed_tour():
                        self.print_tour(self.closed_unstructured_tour_path, self.time_path)
                        self.successful_tours += 1
                    else:
                        self.print_tour(self.open_unstructured_tour_path, self.time_path)
                        self.successful_tours += 1
                self.reset_board(touring=False)
            else:
                self.reset_board(touring=True)

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

    def find_tour_divide_and_conquer(self):
        return


tours = Tour(row_dimension=8, col_dimension=8, tour_type="Backtrack",
             pos_x=0, pos_y=0, total_successful_tours=1000, save_tours=False, save_time=True)
tours.generate_tours()








