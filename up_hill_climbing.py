from up_map import Map
import math
import numpy as np
import random
import timeit


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

        self.neighbour = None

        self.T = 2

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
        x_position = np.asarray(np.where(self.map_board == 10)).T
        s_position = np.asarray(np.where(self.map_board == 11)).T

        scores = []

        while self.T > 1:
            neighbours = []
            i_position = np.asarray(np.where(self.current == 12)).T
            c_position = np.asarray(np.where(self.current == 13)).T
            r_position = np.asarray(np.where(self.current == 14)).T
            for row in range(self.row):
                for column in range(self.column):
                    #                 industry
                    if len(i_position) > 0:
                        for i in i_position:
                            if self.move_zone(i, row, column, 12):
                                neighbours.append(self.neighbour)

                    if len(i_position) < self.industrial and self.add_zone(row, column, 12):
                        self.add_zone(row, column, 12)
                        neighbours.append(self.neighbour)

                    #                 commercial
                    if len(c_position) > 0:
                        for i in c_position:
                            if self.move_zone(i, row, column, 13):
                                neighbours.append(self.neighbour)

                    if len(c_position) < self.commercial and self.add_zone(row, column, 13):
                        self.add_zone(row, column, 13)
                        neighbours.append(self.neighbour)

                    #                     residential
                    for i in r_position:
                        if self.move_zone(i, row, column, 14):
                            neighbours.append(self.neighbour)

                    if len(r_position) < self.residential and self.add_zone(row, column, 14):
                        self.add_zone(row, column, 14)
                        neighbours.append(self.neighbour)

            for i in i_position:
                self.remove_zone(i)
                neighbours.append(self.neighbour)
            for i in c_position:
                self.remove_zone(i)
                neighbours.append(self.neighbour)
            for i in r_position:
                self.remove_zone(i)
                neighbours.append(self.neighbour)

            neighbour = max(neighbours, key=lambda state: self.score(state))
            print(neighbour)

            if self.score(neighbour) > self.current_score:
                self.current = neighbour
                self.current_score = self.score(neighbour)
            else:
                neighbour = random.choice(neighbours)
                if math.exp((self.score(neighbour) - self.current_score) / self.T) > random.uniform(0.0, 1.0):
                    self.current = neighbour
                    self.current_score = self.score(neighbour)
                    self.T = self.T * 10 / 11
            #                     T = T* k/(k+1)
            print(self.current)
        return self.current_score, self.T, self.current

