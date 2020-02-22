
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
        self.temp_score = None
        self.max_score = self.score(self.current)

        self.neighbour = None

        self.T = 4

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

    def remove_zone(self, position):
        if position:
            self.neighbour[position[0], position[1]] = 0
        else:
            return False

    def climb(self):
        x_position = np.asarray(np.where(self.map_board == 10)).T
        s_position = np.asarray(np.where(self.map_board == 11)).T
        i_position = np.asarray(np.where(self.current == 12)).T
        c_position = np.asarray(np.where(self.current == 13)).T
        r_position = np.asarray(np.where(self.current == 14)).T

        neighbours = []
        scores = []

        while self.T > 1:
            for row in range(self.row):
                for column in range(self.column):
                    #                 industry
                    for i in i_position:
                        if self.move_zone(i, row, column, 12) == True:
                            self.current = self.score(self.neighbour)
                            neighbours.append(self.neighbour)

                        elif self.remove_zone(i):
                            self.current = self.score(self.neighbour)
                            neighbours.append(self.neighbour)

                    if len(i_position) < self.industry:
                        self.add_zone(row, column, 12)
                        self.current = self.score(self.neighbour)

                        neighbours.append(self.neighbour)
                        scores.append(self.current)

                    #                 residential
                    for i in c_position:
                        if self.move_zone(i, row, column, 13) == True:
                            self.current = self.score(self.neighbour)
                            neighbours.append(self.neighbour)

                        elif self.remove_zone(i):
                            self.current = self.score(self.neighbour)
                            neighbours.append(self.neighbour)

                    if len(c_position) < self.industry:
                        self.add_zone(row, column, 13)
                        self.current = self.score(self.neighbour)
                        neighbours.append(self.neighbour)

                    #                     commercial
                    for i in r_position:
                        if self.move_zone(i, row, column, 12) == True:
                            self.current = self.score(self.neighbour)
                            neighbours.append(self.neighbour)

                        elif self.remove_zone(i):
                            self.current = self.score(self.neighbour)
                            neighbours.append(self.neighbour)

                    if len(r_position) < self.industry:
                        self.add_zone(row, column, 12)
                        self.current = self.score(self.neighbour)
                        neighbours.append(self.neighbour)

            neighbour = max(neighbours, key=lambda state: self.score(state))

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
        return self.current_score, self.T, self.current

