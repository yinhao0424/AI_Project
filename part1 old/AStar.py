from NQueens import Queen
import heapq
import copy
import time


class Asterisk_algo():

    def __init__(self, state, h_function):
        if h_function == 'H1':
            self.h_function = Queen.heuristic_1
        elif h_function == 'H2':
            self.h_function = Queen.heuristic_2
        self.start_state = state
        self.M, self.N = state.shape
        self.open_list = [(0, 0, self.h_function(self, state), self.encode_state(state))]  # F,G,H,state
        self.parents = {self.encode_state(self.start_state): (0, None)
                        }
        self.close_list = set()
        self.encode_states = {self.encode_state(state): state}
        self.expanded_nodes = 0
        self.solved = False

    def encode_state(self, state):
        res = []
        for col in zip(*state):
            for j in range(len(col)):
                if col[j] != 0:
                    res.append(j)
                    break
        return tuple(res)

    def expand_node(self):
        f, g, h, encoded_state = heapq.heappop(self.open_list)
        state = self.encode_states[encoded_state]
        self.expanded_nodes += 1
        if h == 0:
            self.solved = True
            self.output(encoded_state)
        if encoded_state not in self.close_list:
            for col in range(self.N):
                for row in range(self.N):
                    if row != encoded_state[col]:
                        new_state = copy.deepcopy(state)
                        new_state[row][col], new_state[encoded_state[col]][col] = new_state[encoded_state[col]][
                                                                                      col], \
                                                                                  new_state[row][col]
                        new_encoded_state = self.encode_state(new_state)
                        if new_encoded_state not in self.close_list:
                            self.encode_states[new_encoded_state] = new_state

                            new_g = g + abs(row - encoded_state[col]) * (state[encoded_state[col]][col] ** 2)
                            new_h = self.h_function(self, new_state)
                            new_f = new_g + new_h

                            if new_encoded_state not in self.parents or self.parents[new_encoded_state][0] > new_g:
                                heapq.heappush(self.open_list, (new_f, new_g, new_h, new_encoded_state))
                                self.parents[new_encoded_state] = (new_g, encoded_state)
        self.close_list.add(encoded_state)

    def run(self):
        while (not self.solved) and self.open_list:
            self.expand_node()

    def output(self, final_encoded_state):
        node = final_encoded_state
        final_cost = self.parents[node][0]
        solution_seq = []
        while node:
            cost, next_node = self.parents[node]
            solution_seq.append((cost, node))
            node = next_node
        print("Start_state:")
        print(self.start_state)
        print("Solution sequence:")
        for cost, node in solution_seq[::-1]:
            print(cost, node)
        print("Expanded Nodes: {}".format(self.expanded_nodes))
        print("Length of solution path: {}".format(len(solution_seq)))
        print("final cost {}".format(final_cost))


if __name__ == "__main__":
    problem = Queen()
    print('filename:')
    filename=str(input())
    state = problem.input_board(filename)
    print('1 for A*, 2 for hill climbing:')
    algorithm = int(input())
    if algorithm == 1:
        print('H1 or H2:')
        h_function = str(input())
        state_time = time.time()
        asterisk_algo = Asterisk_algo(state, h_function)
        asterisk_algo.run()
        print("Running time: {} seconds".format(time.time() - state_time))




    # asterisk_algo.load_state()
    # problem = Queen()
    # filename = 'heavy queens board.csv'
    # print(state)
    # print(total_length_node)
    # print(total_cost)
    # print(during_time)
