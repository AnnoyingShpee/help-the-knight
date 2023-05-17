from datetime import datetime
from random import randint
import numpy as np


class Simulations:
    def __init__(self, row_dimension=8, col_dimension=8, tour_type="Backtrack", sim_type="all", pos_x=None, pos_y=None,
                 total_successful_tours=1, save_tours=True, save_time=True, save_open_close=False,
                 save_structured=False):
        self.sim_type = sim_type
        x, y = pos_x, pos_y
        if sim_type == "random":
            x, y = randint(0, row_dimension - 1), randint(0, col_dimension - 1)
        elif sim_type == "all":
            x, y = 0, 0
        elif sim_type == "specific":
            if pos_x is None or pos_y is None:
                x, y = randint(0, row_dimension - 1), randint(0, col_dimension - 1)
            else:
                x, y = pos_x, pos_y
        self.knight_moves = ((2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1))
        self.knight_initial_pos = (x, y)
        self.knight_pos = (x, y)
        self.row_dimension = row_dimension
        self.col_dimension = col_dimension
        self.total_squares = row_dimension * col_dimension
        self.graph = np.negative(np.ones([row_dimension, col_dimension], dtype=int))
        self.moves = np.zeros([row_dimension, col_dimension], dtype=int)
        self.graph[x][y] = 1
        self.moves[x][y] = 1
        self.move_log = [(x, y, 0)]
        self.tour_type = tour_type
        self.state = "touring"  # touring, fail, finished
        self.tour_found = False
        self.knight_step = 1
        self.successful_tours = 0
        self.total_successful_tours = total_successful_tours
        self.save_tours = save_tours
        self.save_time = save_time
        self.save_open_close = save_open_close
        self.save_structured = save_structured
        self.time_start = datetime.now()
        self.duration = 0
        self.total_steps = 1

        self.tours_path = None
        self.moves_path = None
        self.time_path = None

        self.closed_tours_path = None
        self.opened_tours_path = None
        self.structured_tours_path = None
        self.unstructured_tours_path = None

        self.closed_structured_tours_path = None
        self.open_structured_tours_path = None
        self.closed_unstructured_tours_path = None
        self.open_unstructured_tours_path = None

        if self.save_tours:
            self.tours_path = f"Tours/{self.tour_type}/tours_{row_dimension}x{col_dimension}.text"
            self.moves_path = f"Tours/{self.tour_type}/moves_{row_dimension}x{col_dimension}.text"
            try:
                fo = open(self.tours_path, 'w')
                fo.write("--\n")
                fo.close()

                fo = open(self.moves_path, 'w')
                fo.write("--\n")
                fo.close()
            except Exception as e:
                print(e)

        if self.save_time:
            self.time_path = f"Tours/{self.tour_type}/times_{row_dimension}x{col_dimension}.csv"
            try:
                fo = open(self.time_path, 'w')
                fo.write("position_x,position_y,time,steps\n")
                fo.close()
            except Exception as e:
                print(e)

        if self.save_open_close and self.save_structured:
            self.open_structured_tours_path = f"Tours/{self.tour_type}/opened_structured_tours_{row_dimension}x{col_dimension}.txt"
            self.closed_structured_tours_path = f"Tours/{self.tour_type}/closed_structured_tours_{row_dimension}x{col_dimension}.txt"
            self.open_unstructured_tours_path = f"Tours/{self.tour_type}/opened_unstructured_tours_{row_dimension}x{col_dimension}.txt"
            self.closed_unstructured_tours_path = f"Tours/{self.tour_type}/closed_unstructured_tours_{row_dimension}x{col_dimension}.txt"
            try:
                fo = open(self.open_structured_tours_path, 'w')
                fo.write("--\n")
                fo.close()

                fo = open(self.closed_structured_tours_path, 'w')
                fo.write("--\n")
                fo.close()

                fo = open(self.open_unstructured_tours_path, 'w')
                fo.write("--\n")
                fo.close()

                fo = open(self.closed_unstructured_tours_path, 'w')
                fo.write("--\n")
                fo.close()
            except Exception as e:
                print(e)
        elif self.save_open_close:
            self.opened_tours_path = f"Tours/{self.tour_type}/opened_tours_{row_dimension}x{col_dimension}.txt"
            self.closed_tours_path = f"Tours/{self.tour_type}/closed_tours_{row_dimension}x{col_dimension}.txt"
            try:
                fo = open(self.opened_tours_path, 'w')
                fo.write("--\n")
                fo.close()

                fo = open(self.closed_tours_path, 'w')
                fo.write("--\n")
                fo.close()
            except Exception as e:
                print(e)
        elif self.save_structured:
            self.structured_tours_path = f"Tours/{self.tour_type}/structured_tours_{row_dimension}x{col_dimension}.txt"
            self.unstructured_tours_path = f"Tours/{self.tour_type}/unstructured_tours_{row_dimension}x{col_dimension}.txt"
            try:
                fo = open(self.structured_tours_path, 'w')
                fo.write("--\n")
                fo.close()

                fo = open(self.unstructured_tours_path, 'w')
                fo.write("--\n")
                fo.close()
            except Exception as e:
                print(e)

    def reset_board(self):
        self.graph = np.negative(np.ones([self.row_dimension, self.col_dimension], dtype=int))
        self.knight_step = 1
        if self.tour_found:
            self.total_steps = 1
            x, y = 0, 0
            if self.sim_type == "random":
                x = randint(0, self.row_dimension - 1)
                y = randint(0, self.col_dimension - 1)
            elif self.sim_type == "all":
                if self.knight_initial_pos[1] < self.col_dimension - 1:
                    y = self.knight_initial_pos[1] + 1
                    x = self.knight_initial_pos[0]
                else:
                    if self.knight_initial_pos[0] < self.row_dimension - 1:
                        x = self.knight_initial_pos[0] + 1
                        y = 0
                    else:
                        self.state = "finished"
            elif self.sim_type == "specific":
                x, y = self.knight_initial_pos
            self.knight_initial_pos = (x, y)
            self.knight_pos = (x, y)
            self.time_start = datetime.now()
            self.duration = 0
            self.moves = np.zeros([self.row_dimension, self.col_dimension], dtype=int)
            self.moves[self.knight_initial_pos[0]][self.knight_initial_pos[1]] = 1
            self.tour_found = False
        else:
            if self.tour_type == "Warnsdorff":
                self.knight_pos = (self.knight_initial_pos[0], self.knight_initial_pos[1])
                self.moves[self.knight_initial_pos[0]][self.knight_initial_pos[1]] += 1
                self.duration += (datetime.now() - self.time_start).total_seconds()
                self.time_start = datetime.now()
            elif self.tour_type == "Backtrack":
                x, y = 0, 0
                if self.sim_type == "random":
                    x = randint(0, self.row_dimension - 1)
                    y = randint(0, self.col_dimension - 1)
                elif self.sim_type == "all":
                    if self.knight_initial_pos[1] < self.col_dimension - 1:
                        y = self.knight_initial_pos[1] + 1
                        x = self.knight_initial_pos[0]
                    else:
                        if self.knight_initial_pos[0] < self.row_dimension - 1:
                            x = self.knight_initial_pos[0] + 1
                            y = 0
                        else:
                            self.state = "finished"
                elif self.sim_type == "specific":
                    x, y = self.knight_initial_pos
                self.knight_initial_pos = (x, y)
                self.knight_pos = (x, y)
                self.time_start = datetime.now()
                self.duration = 0
                self.moves = np.zeros([self.row_dimension, self.col_dimension], dtype=int)
                self.moves[self.knight_initial_pos[0]][self.knight_initial_pos[1]] = 1
        self.graph[self.knight_initial_pos[0]][self.knight_initial_pos[1]] = 1
        self.move_log = [(self.knight_initial_pos[0], self.knight_initial_pos[1], 0)]

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
        print('----')
        if self.save_tours:
            try:
                file_append = open(self.tours_path, 'a')
                for i in range(self.row_dimension):
                    for j in range(self.col_dimension):
                        item = self.graph[i][j]
                        file_append.write(str(item))
                        file_append.write(' ')
                    file_append.write("\n")
                file_append.write("--\n")
                file_append.close()
            except Exception as ex:
                print(ex)
            try:
                file_append = open(self.moves_path, "a")
                for i in range(self.row_dimension):
                    for j in range(self.col_dimension):
                        item = self.moves[i][j]
                        file_append.write(str(item))
                        file_append.write(' ')
                    file_append.write("\n")
                file_append.write("--\n")
                file_append.close()
            except Exception as ex:
                print(ex)

        if self.save_time:
            try:
                file_append = open(self.time_path, 'a')
                file_append.write(
                    f"{self.knight_initial_pos[0]},{self.knight_initial_pos[1]},{self.duration},{self.total_steps}\n")
                file_append.close()
            except Exception as ex:
                print(ex)

        if self.save_open_close and self.save_structured:
            try:
                if self.check_if_closed_tour() and self.check_if_structured_tour():
                    file_append = open(self.closed_structured_tours_path, 'a')
                    for i in range(self.row_dimension):
                        for j in range(self.col_dimension):
                            item = self.graph[i][j]
                            file_append.write(str(item))
                            file_append.write(' ')
                        file_append.write("\n")
                    file_append.write("--\n")
                    file_append.close()
                elif self.check_if_closed_tour():
                    file_append = open(self.closed_unstructured_tours_path, 'a')
                    for i in range(self.row_dimension):
                        for j in range(self.col_dimension):
                            item = self.graph[i][j]
                            file_append.write(str(item))
                            file_append.write(' ')
                        file_append.write("\n")
                    file_append.write("--\n")
                    file_append.close()
                elif self.check_if_structured_tour():
                    file_append = open(self.open_structured_tours_path, 'a')
                    for i in range(self.row_dimension):
                        for j in range(self.col_dimension):
                            item = self.graph[i][j]
                            file_append.write(str(item))
                            file_append.write(' ')
                        file_append.write("\n")
                    file_append.write("--\n")
                    file_append.close()
                else:
                    file_append = open(self.open_unstructured_tours_path, 'a')
                    for i in range(self.row_dimension):
                        for j in range(self.col_dimension):
                            item = self.graph[i][j]
                            file_append.write(str(item))
                            file_append.write(' ')
                        file_append.write("\n")
                    file_append.write("--\n")
                    file_append.close()
            except Exception as e:
                print(e)
        elif self.save_open_close:
            try:
                if self.check_if_closed_tour():
                    file_append = open(self.closed_tours_path, "a")
                    for i in range(self.row_dimension):
                        for j in range(self.col_dimension):
                            item = self.graph[i][j]
                            file_append.write(str(item))
                            file_append.write(' ')
                        file_append.write("\n")
                    file_append.write("--\n")
                    file_append.close()
                else:
                    file_append = open(self.opened_tours_path, 'a')
                    for i in range(self.row_dimension):
                        for j in range(self.col_dimension):
                            item = self.graph[i][j]
                            file_append.write(str(item))
                            file_append.write(' ')
                        file_append.write("\n")
                    file_append.write("--\n")
                    file_append.close()
            except Exception as e:
                print(e)
        elif self.save_structured:
            try:
                if self.check_if_structured_tour():
                    file_append = open(self.structured_tours_path, "a")
                    for i in range(self.row_dimension):
                        for j in range(self.col_dimension):
                            item = self.graph[i][j]
                            file_append.write(str(item))
                            file_append.write(' ')
                        file_append.write("\n")
                    file_append.write("--\n")
                    file_append.close()
                else:
                    file_append = open(self.unstructured_tours_path, 'a')
                    for i in range(self.row_dimension):
                        for j in range(self.col_dimension):
                            item = self.graph[i][j]
                            file_append.write(str(item))
                            file_append.write(' ')
                        file_append.write("\n")
                    file_append.write("--\n")
                    file_append.close()
            except Exception as e:
                print(e)

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
                x_2 = corner[i + 2][0]
                y_2 = corner[i + 2][1]
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
        if self.sim_type == "random" or self.sim_type == "specific":
            while self.successful_tours < self.total_successful_tours:
                self.time_start = datetime.now()
                if self.tour_type == "Random":
                    print("Random walk tour being made")
                    self.find_tour_random_walk()
                elif self.tour_type == "Backtrack":
                    print("Backtrack tour being made")
                    self.find_tour_backtrack_iterative()
                elif self.tour_type == "Warnsdorff":
                    print("Warnsdorff tour being made")
                    self.find_tour_warnsdorff()
                if self.tour_found:
                    self.duration = (datetime.now() - self.time_start).total_seconds()
                    self.print_tour()
                    self.successful_tours += 1
                self.reset_board()
        elif self.sim_type == "all":
            while self.state == "touring":
                self.time_start = datetime.now()
                if self.tour_type == "Backtrack":
                    print("Backtrack tour being made")
                    self.find_tour_backtrack_iterative()
                elif self.tour_type == "Warnsdorff":
                    print("Warnsdorff tour being made")
                    self.find_tour_warnsdorff()
                if self.tour_found:
                    self.duration = (datetime.now() - self.time_start).total_seconds()
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
            self.total_steps += 1
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
                    print(len(self.move_log))
                    self.tour_found = False
                    return False
                self.knight_pos = (self.move_log[-1][0], self.move_log[-1][1])
        self.tour_found = True
        return True

    def find_tour_warnsdorff(self):
        # To give some randomness when choosing a square. Only useful for next squares with the same number of next
        # valid squares
        while self.knight_step < self.row_dimension * self.col_dimension:
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
                return False

            new_x = self.knight_pos[0] + self.knight_moves[least_empty_index][0]
            new_y = self.knight_pos[1] + self.knight_moves[least_empty_index][1]
            self.knight_step += 1
            self.total_steps += 1
            self.graph[new_x][new_y] = self.knight_step
            self.moves[new_x][new_y] += 1
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
        while self.knight_step < self.row_dimension * self.col_dimension:
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


row_input = 0
col_input = 0
tour_type_input = ""
sim_input = ""
x_input = -1
y_input = -1
total_tours_input = 0
save_tour_input = None
save_time_input = None
save_open_close_input = None
save_structured_input = None

while not 3 <= row_input <= 20:
    try:
        row_input = int(input("Choose number of rows for the chessboard (Min 3, Max 20):"))
        if not 3 <= row_input <= 20:
            print("Input needs to be a positive integer between 3 and 20")
    except Exception as e:
        print("Input needs to be a positive integer between 3 and 20")

while not 3 <= col_input <= 20:
    try:
        col_input = int(input("Choose number of columns for the chessboard (Min 3, Max 20):"))
        if not 3 <= col_input <= 20:
            print("Input needs to be a positive integer between 3 and 20")
    except Exception as e:
        print("Input needs to be a positive integer between 3 and 20")

while tour_type_input != "Backtrack" and tour_type_input != "Warnsdorff":
    tour_type_input = input("Choose type of tour (Backtrack, Warnsdorff): ")
    if tour_type_input != "Backtrack" and tour_type_input != "Warnsdorff":
        print("Input must be Backtrack or Warnsdorff")

while sim_input != "all" and sim_input != "random" and sim_input != "specific":
    sim_input = input("Choose type of simulation \n"
                      "-    all = Find a tour for every square on the board \n"
                      "-    random = Find a number of tours using random squares \n"
                      "-    specific = Find a number of tours using a selected square \n")
    if sim_input != "all" and sim_input != "random" and sim_input != "specific":
        print("Input must be all, random or specific")

if sim_input == "specific":
    print("Simulation selected is", sim_input, ". Selecting a square is required.")
    while not 0 <= x_input <= row_input - 1:
        try:
            x_input = int(input(f"Choose row number of square between 0 and {row_input - 1}: "))
            if not 0 <= x_input <= row_input - 1:
                print(f"Input must be an integer between 0 and {row_input - 1}")
        except:
            print(f"Input must be an integer between 0 and {row_input - 1}")
    while not 0 <= y_input <= col_input - 1:
        print("Simulation selected is", sim_input, ", selecting a square is required.")
        try:
            y_input = int(input(f"Choose row number of square between 0 and {col_input - 1}: "))
            if not 0 <= y_input <= col_input - 1:
                print(f"Input must be an integer between 0 and {col_input - 1}")
        except:
            print(f"Input must be an integer between 0 and {col_input - 1}")
elif sim_input == "all" or sim_input == "random":
    print("Simulation selected is", sim_input, ". No need to select a square.")

if sim_input == "specific" or sim_input == "random":
    print("Simulation selected is", sim_input, ". Input the number of tours to be generated.")
    while total_tours_input <= 0:
        try:
            total_tours_input = int(input(f"Input number of tours to be generated: "))
            if total_tours_input <= 0:
                print("Input must be a positive integer greater than 0")
        except:
            print("Input must be a positive integer greater than 0")
elif sim_input == "all":
    print("Simulation selected is", sim_input, ". No need to input the number of tours to be generated.")

while save_tour_input is None:
    save_tour_input = input("Do you wish to save the tours generated? Yes or No?")
    if save_tour_input.lower() == "yes":
        save_tour_input = True
    elif save_tour_input.lower() == "no":
        save_tour_input = False
    else:
        save_tour_input = None
        print("Please input Yes or No")

while save_time_input is None:
    save_time_input = input("Do you wish to save the time taken to generate tours? Yes or No?")
    if save_time_input.lower() == "yes":
        save_time_input = True
    elif save_time_input.lower() == "no":
        save_time_input = False
    else:
        save_time_input = None
        print("Please input Yes or No")

while save_open_close_input is None:
    save_open_close_input = input("Do you wish to save open and closed tours separately? Yes or No?")
    if save_open_close_input.lower() == "yes":
        save_open_close_input = True
    elif save_open_close_input.lower() == "no":
        save_open_close_input = False
    else:
        save_open_close_input = None
        print("Please input Yes or No")

while save_structured_input is None:
    save_structured_input = input("Do you wish to save the structured and unstructured tours separately? Yes or No?")
    if save_structured_input.lower() == "yes":
        save_structured_input = True
    elif save_structured_input.lower() == "no":
        save_structured_input = False
    else:
        save_structured_input = None
        print("Please input Yes or No")

simulations = Simulations(row_dimension=row_input, col_dimension=col_input, tour_type=tour_type_input, sim_type=sim_input,
                          pos_x=x_input, pos_y=y_input, total_successful_tours=total_tours_input, save_tours=save_tour_input,
                          save_time=save_time_input, save_open_close=save_open_close_input, save_structured=save_structured_input)

# Go through every square on the board
# simulations = Simulations(row_dimension=8, col_dimension=8, tour_type="Backtrack", sim_type="all", pos_x=None, pos_y=None,
#                           total_successful_tours=1, save_tours=True, save_time=True, save_open_close=False,
#                           save_structured=False)
# # Generate a tour on the same square for a number of tours
# simulations = Simulations(row_dimension=8, col_dimension=8, tour_type="Backtrack", pos_x=0, pos_y=0, sim_type="specific",
#                           total_successful_tours=1000, save_tours=True, save_time=True, save_open_close=False, save_structured=False)
# # Generate a tour on random squares for a number of tours
# simulations = Simulations(row_dimension=8, col_dimension=8, tour_type="Backtrack", pos_x=0, pos_y=0, sim_type="random",
#                           total_successful_tours=1000, save_tours=True, save_time=True, save_open_close=False, save_structured=False)
simulations.generate_tours()
