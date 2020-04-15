import numpy as np
import copy


class Queen():
    def __init__(self,filename):
        self.filname = filename
        self.start_state = None

        self.queen_weight = []

    def input_board(self):
        """
        input: filename
        output: a array like matrix
        ex:
        array([[0., 0., 0., 0., 0.],
           [0., 0., 0., 0., 2.],
           [0., 0., 0., 4., 0.],
           [0., 3., 0., 0., 0.],
           [9., 0., 1., 0., 0.]])
        """
        self.start_state = np.genfromtxt(self.filname, delimiter=',')
        self.start_state[np.isnan(self.start_state)] = 0
        board = np.nonzero(self.start_state.T)[1]

        for i in range(len(board)):
            self.queen_weight.append(self.start_state[board[i], i] ** 2)

    def state_to_board(self,state):
        board = np.nonzero(state.T)[1]
        return board.tolist()


    def heuristic_1(self, state):
        """
        H1: The lightest Queen across all pairs of Queens attacking each other.
        ex: min(3,9, 9,1, 3,1, 4,2) = 1**1
        input: state
        ex:
        array([[0., 0., 0., 0., 0.],
           [0., 0., 0., 0., 2.],
           [0., 0., 0., 4., 0.],
           [0., 3., 0., 0., 0.],
           [9., 0., 1., 0., 0.]])
        output: H1 score
        """

        board = np.nonzero(state.T)[1]
        min_attact = []
        for i in range(len(board)):
            for j in range(i + 1, len(board)):
                # check same rows attack
                if board[i] == board[j]:
                    min_attact.append(min(state[board[i], i], state[board[j], j]))
                # check diagonally attack
                offset = j - i
                if board[i] == board[j] - offset or board[i] == board[j] + offset:
                    min_attact.append(min(state[board[i], i], state[board[j], j]))
        if min_attact == []:
            return 0
        else:
            h1 = min(min_attact) ** 2
            return h1


    def heuristic_2(self, state):
        """
        H2: Sum across every pair of attacking Queens the weight of the lightest Queen.
        ex: min(3,9)**2 + min(9,1)**2 + min(3,1)**2 + min(4,2)**2 = 3**2 +1**2 +1**2 +2**2  = 15
        input: state
        output: H2 score
        """
        board = np.nonzero(state.T)[1]
        min_attact = []
        for i in range(len(board)):
            for j in range(i + 1, len(board)):
                # check same rows attack
                if board[i] == board[j]:
                    min_attact.append(min(state[board[i], i], state[board[j], j]))
                # check diagonally attack
                offset = j - i
                if board[i] == board[j] - offset or board[i] == board[j] + offset:
                    min_attact.append(min(state[board[i], i], state[board[j], j]))

        if min_attact == []:
            return 0
        else:
            h2 = sum([i ** 2 for i in min_attact])
            return h2

    def near_state(self, state):
        """
        input: state
        output: a list of all possible neighbours
        """
        board = np.nonzero(state.T)[1]
        neighbours=[]
        for col in range(len(board)):
            for row in range(len(board)):
                if row != board[col]:
                    neighbour = copy.deepcopy(state)
                    neighbour[row, col] = state[board[col], col]
                    neighbour[board[col], col] = 0

                    neighbours.append(neighbour)

        return neighbours

    def near_state_position(self, state):
        """
        input: state
        output: a list of all possible neighbours’ position
        """
        board = np.nonzero(state.T)[1]
        near_states_positions = []

        for col in range(len(board)):
            for row in range(len(board)):
                if row != board[col]:
                    neighbour_position = list(board)
                    neighbour_position[col] = row  # Switch column to empty
                    near_states_positions.append(list(neighbour_position))

        return near_states_positions

    def compute_cost(self, state1, state2):
        """
        input: two states
        output: cost of take this step
        """
        board1 = np.nonzero(state1.T)[1]
        board2 = np.nonzero(state2.T)[1]
        cost =  np.dot(abs(board1 - board2), self.queen_weight)
        return cost


if __name__ == "__main__":
    filename = 'heavy queens board.csv'
    q = Queen(filename)
    q.input_board()

    h1 = q.heuristic_1(q.start_state)
    h2 = q.heuristic_2(q.start_state)
    neighbours = q.near_state(q.start_state)

    print(q.start_state)
    print(h1)
    print(h2)

    print(neighbours[0])
    print(q.compute_cost(q.start_state,neighbours[0]))
