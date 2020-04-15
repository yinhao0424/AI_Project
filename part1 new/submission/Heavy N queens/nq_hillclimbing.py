from NQueens import Queen
import timeit
import random
import copy

class hill_climbing(Queen):
    def __init__(self,filename,heuristic):
        Queen.__init__(self,filename)
        self.input_board()

        self.heuristic = heuristic
        self.sideway_walk = 3
        self.sequential_moves = [self.state_to_board(self.start_state)]
        self.sequential_moves_restart = []

        self.cost = 0
        self.total_cost = 0

        self.expanded_node=0

        self.current = copy.deepcopy(self.start_state)
        self.restart = 0

        self.start_time = timeit.default_timer()
        self.during_time = 0

        self.cost_huristic = []

    def hill_climbing(self):

        if self.heuristic =='H1':
            while self.heuristic_1(self.current) != 0 and self.sideway_walk > 0:
                neighbours = self.near_state(self.current)
                if not neighbours:
                    break
                # find neighbour with min H1
                neighbour = min(neighbours, key=lambda state: self.heuristic_1(state))

                if self.heuristic_1(neighbour) == self.heuristic_1(self.current) and self.sideway_walk > 0:
                    # find neighbour with the same value with current
                    neighbour_side = [v for i, v in enumerate(neighbours) if
                                      self.heuristic_1(v) == self.heuristic_1(self.current)]
                    neighbour = random.choice(neighbour_side)
                    self.sideway_walk -= 1

                if self.heuristic_1(neighbour) > self.heuristic_1(self.current):
                    break

                self.cost += self.compute_cost(neighbour, self.current)
                self.current = neighbour
                self.sequential_moves.append(self.state_to_board(self.current))
                if timeit.default_timer() - self.start_time>10:
                    break
            self.during_time = timeit.default_timer() - self.start_time
            # if self.heuristic_1(self.current) == 0:
            #     print('solved')
            # else:
            #     print('failed')

        elif self.heuristic =='H2':
            while self.heuristic_2(self.current) != 0 and self.sideway_walk > 0:
                neighbours = self.near_state(self.current)
                if not neighbours:
                    break
                # find neighbour with min H1
                neighbour = min(neighbours, key=lambda state: self.heuristic_2(state))

                if self.heuristic_2(neighbour) == self.heuristic_2(self.current) and self.sideway_walk > 0:
                    # find neighbour with the same value with current
                    neighbour_side = [v for i, v in enumerate(neighbours) if
                                      self.heuristic_2(v) == self.heuristic_2(self.current)]
                    neighbour = random.choice(neighbour_side)
                    self.sideway_walk -= 1

                if self.heuristic_2(neighbour) > self.heuristic_2(self.current):
                    break
                    #             test addimissiable
                self.cost_huristic.append((self.state_to_board(neighbour), self.heuristic_2(neighbour),self.compute_cost(neighbour, self.current)))

                self.cost += self.compute_cost(neighbour, self.current)
                self.current = neighbour
                self.sequential_moves.append(self.state_to_board(self.current))

            if self.heuristic_2(self.current) == 0:
                print('solved')
            else:
                print('failed')

    # HC com random restart
    def restarts(self):

        if self.heuristic == 'H1':
            self.hill_climbing()
            self.sequential_moves_restart.extend(self.sequential_moves)
            self.total_cost = self.cost

            while self.heuristic_1(self.current) != 0:
                self.current = copy.deepcopy(self.start_state)
                self.sideway_walk = 3
                self.hill_climbing()
                self.restart += 1
                self.total_cost += self.cost + self.compute_cost(self.start_state,self.current)
                self.sequential_moves_restart.extend(self.sequential_moves)
                end = timeit.default_timer()
                if (end - self.start_time) > 10:
                    break

            self.during_time = timeit.default_timer() - self.start_time
            self.expanded_node = len(self.sequential_moves_restart)

            if self.heuristic_1(self.current) == 0:
                print('solved')
            else:
                print('failed')

        elif self.heuristic == 'H2':
            self.hill_climbing()
            self.sequential_moves_restart.extend(self.sequential_moves)
            self.total_cost = self.cost

            while self.heuristic_2(self.current) != 0:
                self.current = copy.deepcopy(self.start_state)
                self.sideway_walk = 3
                self.hill_climbing()
                self.restart += 1
                self.total_cost += self.cost + self.compute_cost(self.start_state,self.current)
                self.sequential_moves_restart.extend(self.sequential_moves)
                end = timeit.default_timer()
                if (end - self.start_time) > 10:
                    break

            self.during_time = timeit.default_timer() - self.start_time
            self.expanded_node = len(self.sequential_moves_restart)
            if self.heuristic_2(self.current) == 0:
                print('solved')
            else:
                print('failed')


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
    # Test for restart
    # hc = hill_climbing('heavy queens board.csv', "H2")
    # hc.restarts()
    # print('Start state:')
    # print(hc.start_state)
    # print('The number of nodes expanded:')
    # print(hc.expanded_node)
    # print("Time to solve the puzzle: ")
    # print(hc.during_time)
    # print('The effective branching factor:' + str(1))
    # print("The total cost: ")
    # print(hc.total_cost)
    # # print('The sequence of moves with restart:')
    # # print(hc.sequential_moves_restart)
    #
    # print('The number of restarts')
    # print(hc.restart)
    #
    # print('Final state')
    # print(hc.current)


    # Test for hill climbing h2
    hc = hill_climbing('data6.csv', "H2")
    # hc.restarts()',"H1")
    hc.hill_climbing()
    print('Start state:')
    print(hc.start_state)
    print('The number of nodes expanded:')
    print(len(hc.sequential_moves))
    print("The cost: ")
    print(hc.cost)
    print('The sequence of moves:')
    print(hc.sequential_moves)
    # print("Time to solve the puzzle: ")
    # print(hc.during_time)

    print('Final state')
    print(hc.current)
    print(hc.cost_huristic)



    #  Test for hill climbing h1
    # hc = hill_climbing('heavy queens board.csv',"H1")
    # hc.hill_climbing()
    # print('Start state:')
    # print(hc.start_state)
    # print('The number of nodes expanded:')
    # print(len(hc.sequential_moves))
    # print("The cost: ")
    # print(hc.cost)
    # print('The sequence of moves:')
    # print(hc.sequential_moves)
    #
    # print('Final state')
    # print(hc.current)


