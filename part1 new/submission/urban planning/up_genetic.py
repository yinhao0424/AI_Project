from up_map import Map
import random
import numpy as np
import copy
import timeit


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

np.set_printoptions(threshold=np.inf)
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
        self.max_score = -100000

        self.size = 400
        self.elitism_size = 10
        self.culling_size = 10

        self.population = []
        self.sort_population = []

        self.parent1 = None
        self.parent2 = None

        self.elitism = []
        self.culling = []
        self.children = []

        self.best_state = None
        self.current_time = None

        self.results = []
        self.scores =[]
        self.result = None

    def initial_population(self):
        for i in range(self.size):
            current_map = self.initial_ga_map()
            if not any(current_map is x for x in self.population):
                self.population.append(current_map)

    def rank_population(self):
        temp = []
        self.scores = []
        for child in self.population:
            score = self.score(child)
            temp.append((score, child))

        # from small to large
        temp.sort(key=lambda x: x[0])

        for i in temp:
            self.sort_population.append(i[1])
            self.scores.append(i[0])


    def get_elitism_culling(self):
        population = copy.deepcopy(self.sort_population)
        for i in range(self.elitism_size):
            self.elitism.append(population.pop())

        for i in range(self.culling_size):
            self.culling.append(self.sort_population.pop(0))
            self.scores.pop(0)


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

    def selection(self):

        scores = np.asarray(self.scores)
        scores_1= scores - min(scores)
        prob = scores_1/sum(scores_1)
        parent_index = np.random.choice(range(len(prob)), 2, p = prob)
        self.parent1 = self.sort_population[parent_index[0]]
        self.parent2 = self.sort_population[parent_index[1]]

    def crossover(self):
        """
        need: self.sort_population
        randomly choose two parents, and generate self.chilren
        """
        cutpoint = int(self.column / 2)
        while len(self.children) < self.size - self.elitism_size:
            # # selection
            # num1 = np.random.randint(0, len(self.sort_population))
            # num2 = np.random.randint(0, len(self.sort_population))
            #
            # if num1 != num2:
            #     parent1 = self.sort_population[num1]
            #     parent2 = self.sort_population[num2]
            self.selection()

            child1 = np.concatenate((self.parent1[:, cutpoint:], self.parent2[:, :cutpoint]), axis=1)
            child2 = np.concatenate((self.parent2[:, cutpoint:], self.parent1[:, :cutpoint]), axis=1)
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
            # print(str(i) + ' generation')
            self.rank_population()

            self.get_elitism_culling()

            self.selection()
            self.crossover()

            self.mutation()
            self.children.extend(self.elitism)

            self.best_state = max(self.children, key=lambda child: self.score(child))

            if self.score(self.best_state) > self.max_score:
                self.max_score = self.score(self.best_state)
                self.current_time = timeit.default_timer() - start
                self.results.append((self.max_score, -self.current_time, self.best_state))

            self.population = self.children
            self.children = []
            end = timeit.default_timer()
            i = i + 1
            if (end - start) > 8:
                break
        #         small to large
        self.results.sort()
        self.result = self.results.pop()
        self.during_time = end - start


if __name__ == '__main__':

    filename = 'urban_test-1.txt'
    ga = genetic(filename)
    ga.genetic_algorithm()


    result = ga.result
    print(result)
    # ga.map_board = ga.map_board.astype(str)
    #
    # for row in range(ga.map_board.shape[0]):
    #     for col in range(ga.map_board.shape[1]):
    #         if ga.map_board[row, col] == '10':
    #             ga.map_board[row, col] = 'X'
    #         elif ga.map_board[row, col] == '11':
    #             ga.map_board[row, col] = 'S'
    #
    # for i in range(result[2].shape[0]):
    #     for j in range(result[2].shape[1]):
    #         if result[2][i, j] == 12:
    #             ga.map_board[i, j] = 'I'
    #         elif result[2][i, j] == 13:
    #             ga.map_board[i, j] = "R"
    #         elif result[2][i, j] == 14:
    #             ga.map_board[i, j] = "C"
    #
    # print(ga.map_board)
    #
    # output = open("urban planning GA.txt", 'w')
    # print("The score for best map is: ", result[0], file=output)
    # print("The time that score was first achieved:", -result[1], file=output)
    # print("The map of the city:", file=output)
    # print(ga.map_board, file=output)
    # output.close()