from random import randint
import numpy as np

open_tour_file_path = "open_structured_tours.txt"
closed_tour_file_path = "closed_structured_tours.txt"

try:
    fo = open(open_tour_file_path, 'w')
    fo.write("--\n")
    fo.close()

    fc = open(closed_tour_file_path, 'w')
    fc.write("--\n")
    fc.close()
except Exception as e:
    print(e)

class RandomWalk:
    def __init__(self, dimension):
        x = randint(0, 7)
        y = randint(0, 7)
        self.dimension = dimension
        self.total_squares = dimension**2
        self.graph = np.negative(np.ones([dimension, dimension], dtype=int))
        self.knight_moves = ((2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1))
        self.knight_initial_pos = (x, y)
        self.knight_pos = (x, y)
        self.tour_found = False
        self.move_done = False
        self.knight_step = 1
        self.successful_tours = 0
        self.graph[x][y] = self.knight_step

    def reset_board(self):
        x = randint(0, 7)
        y = randint(0, 7)
        self.graph = np.negative(np.ones([self.dimension, self.dimension], dtype=int))
        # self.state = "start"
        self.tour_found = False
        self.knight_initial_pos = None
        self.knight_pos = None
        self.knight_step = 1

    def print_tour(self, file_path):
        try:
            file_append = open(file_path, 'a')
            for i in range(self.dimension):
                for j in range(self.dimension):
                    item = self.graph[i][j] + ' '
                    print(self.graph[i][j], end=' ')
                    file_append.write(item)
                print()
                file_append.write("\n")
            print()
            print("--")
            file_append.write("\n")
            file_append.write("--\n")
            self.tour_found = False
        except Exception as ex:
            print(ex)

    def check_tour_type(self):
        x_to_be_checked, y_to_be_checked = [0, 1, 6, 7], [0, 1, 6, 7]
        return

    # Count the number of steps in one random tour
    def generate_random_tours(self):
        while self.successful_tours < 100:
            self.find_tour()
            if self.tour_found:
                self.print_tour(self.check_tour_type())

    def is_valid_move(self, x, y):
        """
            A utility function to check if i,j are valid indexes
            for N*N chessboard
            :param x: row number of square
            :param y: column number of square
        """
        if 0 <= x < self.dimension and 0 <= y < self.dimension and self.graph[x][y] == -1:
            return True
        return False

    def find_tour(self):
        """
        Function chooses the algorithm selected to find the tour
        :return:
        """
        # First checks whether tour has already been found
        if not self.tour_found:
            if self.knight_step < 64:
                self.find_tour_random_walk()
            else:
                self.tour_found = True

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
        # move_log stores list of squares traversed by the knight
        # Each square contains (row, column, next index to use of knight_moves list)
        contains_valid = False
        # Checks if the square has valid moves, if so, move to that new square

        r = randint(0, 7)
        dx, dy = self.knight_moves[r][0], self.knight_moves[r][1]

        new_x, new_y = self.knight_pos[0] + dx, self.knight_pos[1] + dy

        if self.is_valid_move(new_x, new_y):
            self.knight_pos = (new_x, new_y)
            self.knight_step += 1
            self.graph[new_x][new_y] = self.knight_step

        self.move_done = True


new_random_walk = RandomWalk(8)
new_random_walk.generate_random_tours()






