import numpy as np
import copy


class Queen():

    def input_board(self, filename):
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
        state = np.genfromtxt(filename, delimiter=',')
        state[np.isnan(state)] = 0
        return state

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
        near_states = []

        for col in range(len(board)):
            for row in range(len(board)):
                if row != board[col]:
                    neighbour = copy.deepcopy(state)
                    neighbour[row, col] = state[board[col], col]
                    neighbour[board[col], col] = 0

                    near_states.append(neighbour)

        return near_states


if __name__ == "__main__":
    q = Queen()
    state = q.input_board('heavy queens board.csv')
    h1 = q.heuristic_1(state)
    h2 = q.heuristic_2(state)
    near_states = q.near_state(state)
    print(state)
    print(h1)
    print(h2)
    print(near_states[0])
