from NQueens import Queen
import timeit
import numpy as np

class a_star(Queen):
    def __init__(self,filename,heuristic):
        Queen.__init__(self,filename)
        self.input_board()

        self.heuristic = heuristic
        self.frontier = []
        self.come_from = {}
        self.cost_so_far = {}

        self.start_time = timeit.default_timer()
        self.during_time = 0

        self.result = None
        self.sequential_moves = []
        self.node_expand = 0

        self.total_cost = 0
        self.effective_branching_factor = 0


    def state_to_tuple(self,state):
        return tuple(np.nonzero(state.T)[1])


    def a_star(self):

        start = self.state_to_tuple(self.start_state)
        self.frontier.append((0, self.start_state))
        self.cost_so_far[start] = 0


        if self.heuristic == 'H1':
            while self.frontier:
                #         sorted(graded, key=lambda x: x[0])
                # small to large
                self.frontier.sort(key=lambda x: x[0])
                current = self.frontier.pop(0)

                if self.heuristic_1(current[-1]) == 0:
                    self.result = current[-1]
                    break
                for next in self.near_state(current[-1]):
                    new_cost = self.cost_so_far[self.state_to_tuple((current[-1]))] + self.compute_cost(current[-1], next)

                    if self.state_to_tuple(next) not in self.cost_so_far or new_cost < self.cost_so_far[self.state_to_tuple(next)]:
                        self.cost_so_far[self.state_to_tuple(next)] = new_cost

                        priority = new_cost + self.heuristic_1(next)
                        self.frontier.append((priority, next))

                        self.come_from[self.state_to_tuple(next)] = self.state_to_tuple(current[-1])


                end = timeit.default_timer()

                if (end - self.start_time) > 10:
                    break

            i = 0
            self.sequential_moves.append(self.state_to_tuple(self.result))
            while True:
                if self.sequential_moves[i] not in self.come_from:
                    break
                back = self.come_from[self.sequential_moves[i]]
                i += 1
                self.sequential_moves.append(back)

            self.node_expand = len(self.cost_so_far)
            self.effective_branching_factor = self.node_expand**(1/len(self.sequential_moves))
            self.total_cost = self.cost_so_far[self.state_to_tuple(self.result)]

        elif self.heuristic == 'H2':
            while self.frontier:
                #         sorted(graded, key=lambda x: x[0])
                # small to large
                self.frontier.sort(key=lambda x: x[0])
                current = self.frontier.pop(0)

                if self.heuristic_2(current[-1]) == 0:
                    self.result = current[-1]
                    break
                for next in self.near_state(current[-1]):
                    new_cost = self.cost_so_far[self.state_to_tuple((current[-1]))] + self.compute_cost(current[-1], next)

                    if self.state_to_tuple(next) not in self.cost_so_far or new_cost < self.cost_so_far[self.state_to_tuple(next)]:
                        self.cost_so_far[self.state_to_tuple(next)] = new_cost

                        priority = new_cost + self.heuristic_2(next)
                        self.frontier.append((priority, next))

                        self.come_from[self.state_to_tuple(next)] = self.state_to_tuple(current[-1])


                end = timeit.default_timer()

                if (end - self.start_time) > 10:
                    break

            i = 0
            self.sequential_moves.append(self.state_to_tuple(self.result))
            while True:
                if self.sequential_moves[i] not in self.come_from:
                    break
                back = self.come_from[self.sequential_moves[i]]
                i += 1
                self.sequential_moves.append(back)

            self.node_expand = len(self.cost_so_far)
            self.effective_branching_factor = self.node_expand**(1/len(self.sequential_moves))
            self.total_cost = self.cost_so_far[self.state_to_tuple(self.result)]


        end = timeit.default_timer()
        self.during_time = end - self.start_time

        # return state, node_expanded, during_time, result

if __name__ == "__main__":
    """
    output：
    1. start state
    2. the number of nodes expanded
    3. time to solve the puzzle
    4. the effective branching factor
    5. the cost to solve the puzzle
    6. the sequence of moves

    """
    filename = 'heavy queens board.csv'
    astar = a_star(filename,'H2')
    astar.a_star()

    print('Start state:')
    print(astar.start_state)

    print('The number of nodes expanded:')
    print(astar.node_expand)

    print("Time to solve the puzzle: ")
    print(astar.during_time)

    print('The effective branching factor:' )
    print(astar.effective_branching_factor)

    print("The total cost: ")
    print(astar.total_cost)

    print('The sequence of moves:')
    print(astar.sequential_moves[::-1])

    print('Final state')
    print(astar.result)




