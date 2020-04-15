from up_map import Map
import math
import numpy as np
import random
import timeit

np.set_printoptions(threshold=np.inf)
class hill_climbing(Map):
    """
    input: Map class
    output:
    """

    def __init__(self, filename):
        Map.__init__(self, filename)

        self.get_map()
        self.current = self.initial_map()
        self.current_score = self.score(self.current)
        self.max_score = self.score(self.current)

        self.restart = 0

        self.neighbour = None
        self.during_time = None

        self.start_time = timeit.default_timer()

        self.T = 5
        self.results = []

    def move_zone(self, position, row, column, type):
        value_original = self.map_board[row, column]
        value = self.current[row, column]
        if value_original != 10 and value != 12 and value != 13 and value != 14:
            self.neighbour = self.current.copy()
            self.neighbour[position[0], position[1]] = 0
            self.neighbour[row, column] = type
            return True
        else:
            return False

    def add_zone(self, row, column, type):
        value_original = self.map_board[row, column]
        value = self.current[row, column]
        if value_original != 10 and value != 12 and value != 13 and value != 14:
            self.neighbour = self.current.copy()
            self.neighbour[row, column] = type
            return True
        else:
            return False

    def remove_zone(self, position):

        self.neighbour = self.current.copy()
        self.neighbour[position[0], position[1]] = 0

    def climb(self):

        while timeit.default_timer()-self.start_time<10:
            while self.T > 1 and timeit.default_timer()-self.start_time<8:
                neighbours = []
                i_position = np.asarray(np.where(self.current == 12)).T
                c_position = np.asarray(np.where(self.current == 13)).T
                r_position = np.asarray(np.where(self.current == 14)).T
                for row in range(self.row):
                    for column in range(self.column):
                        #                 industry
                        p = random.random()
                        if p<0.33:
                            if len(i_position) > 0:
                                for i in i_position:
                                    if self.move_zone(i, row, column, 12):
                                        neighbours.append(self.neighbour)

                            if len(i_position) < self.industrial and self.add_zone(row, column, 12):
                                self.add_zone(row, column, 12)
                                neighbours.append(self.neighbour)

                        #                 commercial
                        elif p<0.66:
                            if len(c_position) > 0:
                                for i in c_position:
                                    if self.move_zone(i, row, column, 13):
                                        neighbours.append(self.neighbour)

                            if len(c_position) < self.commercial and self.add_zone(row, column, 13):
                                self.add_zone(row, column, 13)
                                neighbours.append(self.neighbour)
                        else:
                        #                     residential
                            for i in r_position:
                                if self.move_zone(i, row, column, 14):
                                    neighbours.append(self.neighbour)

                            if len(r_position) < self.residential and self.add_zone(row, column, 14):
                                self.add_zone(row, column, 14)
                                neighbours.append(self.neighbour)

                if random.random() < 0.1:
                    for i in i_position:
                        self.remove_zone(i)
                        neighbours.append(self.neighbour)
                    for i in c_position:
                        self.remove_zone(i)
                        neighbours.append(self.neighbour)
                    for i in r_position:
                        self.remove_zone(i)
                        neighbours.append(self.neighbour)

                if neighbours:
                    neighbour = max(neighbours, key=lambda state: self.score(state))


                    if self.score(neighbour) > self.current_score:
                        self.current = neighbour
                        self.current_score = self.score(neighbour)
                    else:
                        neighbour = random.choice(neighbours)
                        if math.exp((self.score(neighbour) - self.current_score) / self.T) > random.uniform(0.0, 1.0):
                            self.current = neighbour
                            self.current_score = self.score(neighbour)
                            self.T = self.T * 0.9
            #                        T = T* k/(k+1)
                end = timeit.default_timer()
                if (end - self.start_time) > 1:
                    break
            self.current_time = timeit.default_timer() - self.start_time
            self.results.append((self.current_score, -self.current_time, self.current))

        # if not neighbours:
            self.current = self.initial_map()
            self.T = 5
            self.restart += 1
        #     break

        self.results.sort()
        self.result = self.results.pop()
        self.during_time = end - self.start_time


if __name__ == '__main__':

    #
    filename = 'urban_test-1.txt'
    hc = hill_climbing(filename)
    hc.climb()

    result = hc.result
    print(result)
    print(hc.during_time)
    hc.map_board = hc.map_board.astype(str)

    for row in range(hc.map_board.shape[0]):
        for col in range(hc.map_board.shape[1]):
            if hc.map_board[row, col] == '10':
                hc.map_board[row, col] = 'X'
            elif hc.map_board[row, col] == '11':
                hc.map_board[row, col] = 'S'

    for i in range(result[2].shape[0]):
        for j in range(result[2].shape[1]):
            if result[2][i, j] == 12:
                hc.map_board[i, j] = 'I'
            elif result[2][i, j] == 13:
                hc.map_board[i, j] = "R"
            elif result[2][i, j] == 14:
                hc.map_board[i, j] = "C"

    print(hc.map_board)

    output = open("urban planning HC.txt", 'w')
    print("The score for best map is: ", result[0], file=output)
    print("The time that score was first achieved:", -result[1], file=output)
    print("The map of the city:", file=output)
    print(hc.map_board, file=output)
    output.close()