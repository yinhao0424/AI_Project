from NQueens import Queen
import timeit
import random


def hill_climbing(problem, filename, sideway_walk=5):
    current = problem.input_board(filename)
    cost = 0
    sideway_walk = 5
    sequential_moves = [current]

    while problem.heuristic_1(current) != 0 and sideway_walk > 0:
        neighbours = problem.near_state(current)
        if not neighbours:
            break
        # find neighbour with min H1
        neighbour = min(neighbours, key=lambda state: problem.heuristic_1(state))

        if problem.heuristic_1(neighbour) == problem.heuristic_1(current) and sideway_walk > 0:
            # find neighbour with the same value with current
            neighbour_side = [v for i, v in enumerate(neighbours) if
                              problem.heuristic_1(v) == problem.heuristic_1(current)]
            neighbour = random.choice(neighbour_side)
            sideway_walk -= 1

        if problem.heuristic_1(neighbour) > problem.heuristic_1(current):
            break
        cost += problem.cost(neighbour, current)
        current = neighbour
        sequential_moves.append(current)

    return current, cost, sequential_moves, len(sequential_moves)


# HC com random restart
def random_restart(problem, filename):
    restart_times = 0
    total_cost = 0
    total_length_node = 0
    sequential_moves_restart = []

    start = timeit.default_timer()
    state = problem.input_board(filename)

    while problem.heuristic_1(state) != 0:

        state, cost, sequential_moves, length_node = hill_climbing(problem, filename)
        total_cost = cost + problem.cost(problem.input_board(filename), state)
        total_length_node += length_node
        restart_times += 1

        sequential_moves_restart.append(sequential_moves)

        end = timeit.default_timer()
        if (end - start) > 10:
            break

    during_time = end - start
    return state, total_length_node, total_cost, sequential_moves_restart, during_time

if __name__ == "__main__":
    problem = Queen()
    filename = 'heavy queens board.csv'
    # filename = 'hc_test.csv'
    state, total_length_node, total_cost, sequential_moves_restart, during_time = random_restart(problem, filename)
    print(state)
    print(total_length_node)
    print(total_cost)
    print(during_time)
    print(sequential_moves_restart)