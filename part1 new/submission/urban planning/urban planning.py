from up_map import Map

import copy
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

        self.T = 2
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

        start = timeit.default_timer()
        while True:
            while self.T > 1:
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
                            self.T = self.T * 10 / 11
            #                         T = T* k/(k+1)
            self.current_time = timeit.default_timer() - start
            self.results.append((self.current_score, -self.current_time, self.current))

        # if not neighbours:
            self.current = self.initial_map()
            self.restart += 1
        #     break

            end = timeit.default_timer()
            if (end - start) > 10:
                break
        self.results.sort()
        self.result = self.results.pop()
        self.during_time = end - start


"""
-Start with k randomly generated states (population) 

-Do until “done”
    Select k2<<k most fit states to be preserved (elitism)
    Remove k3<k weakest states from population (culling)
    Repeat 
        Select two states semi-randomly
            Weight towards states with better fitness
            Think of fitness as opposite of heuristic function
        Combine two states to generates two successors
        Randomly change some bits in the states (mutation)

    Until population is full

"""

class genetic(Map):
    def __init__(self, filename):
        """
        functions: get population; sort and get elitism and culling; crossover; mutation;
        Running whole algorithm

        """
        Map.__init__(self, filename)
        self.get_map()

        self.during_time = 0
        self.time = 0
        self.max_score = None

        self.size = 150
        self.elitism_size = 5
        self.culling_size = 5

        self.population = []
        self.sort_population = []
        self.elitism = []
        self.culling = []
        self.children = []

        self.max_score = None
        self.best_state = None
        self.current_time = None

        self.results = []
        self.result = None

    def initial_population(self):
        for i in range(self.size):
            current_map = self.initial_map()
            self.population.append(current_map)

    def rank_population(self):
        temp = []
        for child in self.population:
            score = self.score(child)
            temp.append((score, child))

        # from small to large
        temp.sort(key=lambda x: x[0])

        for i in temp:
            self.sort_population.append(i[1])

    def get_elitism_culling(self):
        population = copy.deepcopy(self.sort_population)
        for i in range(self.elitism_size):
            self.elitism.append(population.pop())

        for i in range(self.culling_size):
            self.culling.append(self.sort_population.pop(0))

    def check_children(self, state):
        """
        input:
        array([[ 0.,  0.,  0.,  0.],
                [ 0., 12.,  0.,  0.],
                [ 0., 13.,  0.,  0.]])
        output: True/False
        """
        industrial_positions = np.asarray(np.where(state == 12)).T
        commercial_positions = np.asarray(np.where(state == 13)).T
        residential_positions = np.asarray(np.where(state == 14)).T
        if len(industrial_positions) <= self.industrial and len(commercial_positions) <= self.commercial and len(
                residential_positions) <= self.residential:
            return True
        else:
            return False

    def crossover(self):
        """
        need: self.sort_population
        randomly choose two parents, and generate self.chilren
        """
        cutpoint = int(self.column / 2)
        while len(self.children) < self.size - self.elitism_size:
            num1 = np.random.randint(0, len(self.sort_population))
            num2 = np.random.randint(0, len(self.sort_population))
            if num1 != num2:
                parent1 = self.sort_population[num1]
                parent2 = self.sort_population[num2]

                child1 = np.concatenate((parent1[:, cutpoint:], parent2[:, :cutpoint]), axis=1)
                child2 = np.concatenate((parent2[:, cutpoint:], parent1[:, :cutpoint]), axis=1)
                if self.check_children(child1):
                    self.children.append(child1)

                if len(self.children) == self.size - self.elitism_size:
                    break

                if self.check_children(child2):
                    self.children.append(child2)

                if len(self.children) == self.size - self.elitism_size:
                    break

    def mutation(self):
        """
        for n children, it has chance to mutate, return children
        """

        for child in self.children:

            row1 = np.random.randint(0, self.row)
            row2 = np.random.randint(0, self.row)
            column1 = np.random.randint(0, self.column)
            column2 = np.random.randint(0, self.column)
            if self.map_board[row1, column1] != 10 or self.map_board[row1, column1] != 11 or self.map_board[
                row2, column2] != 10 or self.map_board[row2, column2] != 11:
                temp = child[row1, column1]
                child[row1, column1] = child[row2, column2]
                child[row2, column2] = temp

    def genetic_algorithm(self):
        """
        run genetic algorithm
        end state: time over 10 seconds

        """
        self.initial_population()
        start = timeit.default_timer()
        i = 0
        while True:
            print(str(i) + ' generation')
            self.rank_population()
            self.get_elitism_culling()
            self.crossover()

            self.mutation()
            self.children.extend(self.elitism)

            self.best_state = max(self.children, key=lambda child: self.score(child))
            self.max_score = self.score(self.best_state)
            self.current_time = timeit.default_timer() - start
            self.results.append((self.max_score, -self.current_time, self.best_state))

            self.population = self.children

            end = timeit.default_timer()
            i = i + 1
            if (end - start) > 10:
                break
        #         small to large
        self.results.sort()
        self.result = self.results.pop()
        self.during_time = end - start

if __name__ == '__main__':
    # print('Please input filename: ')
    # # filename = str(input())
    # print("Please input HC or GA")
    # algorithm = str(input())
    filename = 'urban_test-1.txt'
    algorithm = 'HC'

    if algorithm == 'GA':
        ga = genetic(filename)
        ga.genetic_algorithm()

        result = ga.result
        print(ga.map_board)
        ga.map_board = ga.map_board.astype(str)

        for row in range(ga.map_board.shape[0]):
            for col in range(ga.map_board.shape[1]):
                if ga.map_board[row, col] == '10':
                    ga.map_board[row, col] = 'X'
                elif ga.map_board[row, col] == '11':
                    ga.map_board[row, col] = 'S'

        for i in range(result[2].shape[0]):
            for j in range(result[2].shape[1]):
                if result[2][i, j] == 12:
                    ga.map_board[i, j] = 'I'
                elif result[2][i, j] == 13:
                    ga.map_board[i, j] = "R"
                elif result[2][i, j] == 14:
                    ga.map_board[i, j] = "C"

        print(ga.map_board)

        output = open("urban planning GA.txt", 'w')
        print("The score for best map is: ", result[0], file=output)
        print("The time that score was first achieved:", -result[1], file=output)
        print("The map of the city:", file=output)
        print(ga.map_board, file=output)
        output.close()
    elif algorithm == 'HC':
        hc = hill_climbing(filename)
        hc.climb()

        result = hc.result
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
    else:
        print('Please pass the correct arguments')
