from up_map import Map
import random
import numpy as np
import copy


class genetic(Map):
    def __init__(self, filename):
        """
        functions: get population; sort and get elitism and culling; crossover; mutation;
        Running whole algorithm

        """
        Map.__init__(self, filename)
        self.get_map()

        self.size = 8
        self.elitism_size = 1
        self.culling_size = 1

        self.population = []
        self.sort_population = []
        self.elitism = []
        self.culling = []
        self.children = []

        self.max_score = None

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
            self.elitism.append(self.sort_population.pop(0))

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
        randomly choose two parents, and generate self.chilren
        """
        cutpoint = int(self.column / 2)
        while True:
            num1 = np.random.randint(0, len(self.sort_population))
            num2 = np.random.randint(0, len(self.sort_population))
            if num1 != num2:
                parent1 = self.sort_population[num1]
                parent2 = self.sort_population[num2]

                child1 = np.concatenate((parent1[:, cutpoint:], parent2[:, :cutpoint]), axis=1)
                child2 = np.concatenate((parent2[:, cutpoint:], parent1[:, :cutpoint]), axis=1)
                if self.check_children(child1):
                    self.children.append(child1)
                    children_size += 1

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

    def ga(self):
        """
        run genetic algorithm

        """
        self.initial_population()


