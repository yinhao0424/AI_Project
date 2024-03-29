import numpy as np
import random
import copy


class Map():
    """
    Input: filename
    Output: how many industrial, commercial, residential; Map stored in array
    ex:
    self.map: [['X', '1', '2', '4'], ['3', '4', 'S', '3'], ['6', '0', '2', '3']]
    """

    def __init__(self, filename):
        self.filename = filename

        self.industrial = 0
        self.commercial = 0
        self.residential = 0

        self.real_industrial = 0
        self.real_commercial = 0
        self.real_residential = 0

        self.row = 0
        self.column = 0

        self.map_board = []

        self.toxic_positions = []
        self.scenic_positions = []

    def get_map(self):
        with open(self.filename) as f:
            line = f.read().splitlines()

        self.industrial = int(line[0])
        self.residential = int(line[1])
        self.commercial = int(line[2])

        ## build list of map
        for i in line[3:]:
            self.map_board.append(i.split(','))

        for i in range(len(self.map_board)):
            for j in range(len(self.map_board[0])):

                if self.map_board[i][j] == 'X':
                    self.map_board[i][j] = 10
                    #                     get coordinate of X
                    self.toxic_positions.append([i, j])

                elif self.map_board[i][j] == 'S':
                    self.map_board[i][j] = 11
                    #                    get coordinate of S
                    self.scenic_positions.append([i, j])
                else:
                    self.map_board[i][j] = int(self.map_board[i][j])
        self.map_board = np.array(self.map_board)
        #         self.toxic_positions = np.array(self.toxic_positions)
        #         self.scenic_positions = np.array(self.scenic_positions)

        self.row = self.map_board.shape[0]
        self.column = self.map_board.shape[1]


    def initial_map(self):
        """
        Input: map class
        Output: initial map
        ex:
        array([[ 0.,  0.,  0.,  0.],
           [ 0., 14.,  0.,  0.],
           [ 0.,  0.,  0.,  0.]])
        """

        self.real_industrial = random.randint(0, self.industrial)
        self.real_commercial = random.randint(0, self.commercial)
        self.real_residential = random.randint(0, self.residential)
        total_amount = self.real_industrial + self.real_commercial + self.real_residential

        avaliable_position = []
        initial_map = np.zeros(self.map_board.shape)

        for row in range(self.row):
            for column in range(self.column):
                if self.map_board[row, column] != 10:
                    avaliable_position.append([row, column])

        put_building = random.sample(avaliable_position, total_amount)

        for i in range(self.real_industrial):
            initial_map[put_building[i][0], put_building[i][1]] = 12
        for i in range(self.real_commercial):
            initial_map[put_building[i + self.real_industrial][0], put_building[i + self.real_industrial][1]] = 13
        for i in range(self.real_residential):
            initial_map[
                put_building[i + self.real_industrial + self.real_commercial][0],
                put_building[i + self.real_industrial + self.real_commercial][1]] = 14

        return initial_map

    def initial_ga_map(self):
        """
        Input: map class
        Output: initial map
        ex:
        array([[ 0.,  0.,  0.,  0.],
           [ 0., 14.,  0.,  0.],
           [ 0.,  0.,  0.,  0.]])
        """

        total_amount = self.industrial + self.commercial + self.residential

        avaliable_position = []
        initial_ga_map = np.zeros(self.map_board.shape)

        for row in range(self.row):
            for column in range(self.column):
                if self.map_board[row, column] != 10:
                    avaliable_position.append([row, column])

        put_building = random.sample(avaliable_position, total_amount)

        for i in range(self.industrial):
            initial_ga_map[put_building[i][0], put_building[i][1]] = 12
        for i in range(self.commercial):
            initial_ga_map[put_building[i + self.industrial][0], put_building[i + self.industrial][1]] = 13
        for i in range(self.residential):
            initial_ga_map[
                put_building[i + self.industrial + self.commercial][0],
                put_building[i + self.industrial + self.commercial][1]] = 14

        return initial_ga_map

    def manhattandistance(self,coor1, coor2):
        """
        input:
        coor1: position of point1
        coor2: position of point2
        output:
        manhattandistance
        """

        return abs(coor1[0] - coor2[0]) + abs(coor1[1] - coor2[1])


    def score(self, initial_map):
        """
        input:
        map_start: Map class with original board
        ex:  array([[10,  1,  2,  4],
                   [ 3,  4, 11,  3],
                   [ 6,  0,  2,  3]])
        map: new urban design
        ex:  array([[ 0.,  0.,  0.,  0.],
                   [ 0.,  0.,  0.,  0.],
                   [ 0., 14.,  0.,  0.]])

        output: score of new urban design map
        """
        score = 0

        toxic_positions = copy.deepcopy(self.toxic_positions)
        scenic_positions = copy.deepcopy(self.scenic_positions)

        industrial_positions = np.asarray(np.where(initial_map == 12)).T
        commercial_positions = np.asarray(np.where(initial_map == 13)).T
        residential_positions = np.asarray(np.where(initial_map == 14)).T

        # build cost
        for i in industrial_positions:
            if self.map_board[i[0], i[1]] == 11:
                score -= 1
                scenic_positions.remove([i[0], i[1]])
            else:
                score += -self.map_board[i[0], i[1]] - 2


        for i in commercial_positions:
            if self.map_board[i[0], i[1]] == 11:
                score -= 1
                scenic_positions.remove([i[0], i[1]])
            else:
                score += -self.map_board[i[0], i[1]] - 2

        for i in residential_positions:
            if self.map_board[i[0], i[1]] == 11:
                score -= 1
                scenic_positions.remove([i[0], i[1]])
            else:
                score += -self.map_board[i[0], i[1]] - 2

        # compute benefits from each other
        # Industrial tiles benefit from being near other industry.
        if len(industrial_positions) > 1:
            for i in range(0, len(industrial_positions) - 1):
                for j in range(i + 1, len(industrial_positions)):
                    if self.manhattandistance(industrial_positions[i], industrial_positions[j]) <= 2:
                        score += 2

        # Commercial sites benefit from being near residential tiles.
        for i in commercial_positions:
            for j in residential_positions:
                if self.manhattandistance(i, j) <= 3:
                    score += 4

        # residential sites benefit from being near Commercial tiles.
        for i in residential_positions:
            for j in commercial_positions:
                if self.manhattandistance(i, j) <= 3:
                    score += 4

        # Comercial with Comercial
        if len(commercial_positions) > 1:
            for i in range(0, len(commercial_positions) - 1):
                for j in range(i + 1, len(commercial_positions)):
                    if self.manhattandistance(commercial_positions[i], commercial_positions[j]) <= 2:
                        score -= 4

        # Residential sites do not like being near industrial sites.
        for i in commercial_positions:
            for j in industrial_positions:
                if self.manhattandistance(i, j) <= 3:
                    score -= 5

        # penalty zones close to toxic waste site
        for toxic in toxic_positions:
            for industrial in industrial_positions:
                if self.manhattandistance(toxic, industrial) <= 2:
                    score -= 10
            for commercial in commercial_positions:
                if self.manhattandistance(toxic, commercial) <= 2:
                    score -= 20
            for residential in residential_positions:
                if self.manhattandistance(toxic, residential) <= 2:
                    score -= 20

                    # prize zones close to scenic view
        for scenic in scenic_positions:
            for residential in residential_positions:
                if self.manhattandistance(scenic, residential) <= 2:
                    score += 10

        return score

if __name__ == '__main__':
    map = Map('urban 1.txt')
    map.get_map()
    initial_map = map.initial_map()
    print('starting state')
    print(map.map_board)
    # print('initial urban plannign')
    print(initial_map)
    score = map.score(initial_map)
    print(score)

