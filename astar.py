from NQueens import Queen
import timeit
import random


def a_star(problem, filename,heuristic,sideway_walk=5):
    current = problem.input_board(filename)
    cost = 0
    g = 0
    sideway_walk = 5
    sequential_moves = [current]
    if heuristic =='H1':
        while problem.heuristic_1(current) != 0 and sideway_walk > 0:
            neighbours = problem.near_state(current)
            if not neighbours:
                break
            # find neighbour with min H1+G
            neighbour = min(neighbours, key=lambda state: (problem.heuristic_1(state) + g))
            
            if problem.heuristic_1(neighbour) == problem.heuristic_1(current) and sideway_walk > 0:
                # find neighbour with the same value with current
                neighbour_side = [v for i, v in enumerate(neighbours) if
                                  problem.heuristic_1(v) == problem.heuristic_1(current)]
                neighbour = random.choice(neighbour_side)
                sideway_walk -= 1
                g += neighbour * neighbour * neighbour_side
            if problem.heuristic_1(neighbour) > problem.heuristic_1(current):
                break
            cost += problem.cost(neighbour, current)
            current = neighbour
            sequential_moves.append(current)

    elif heuristic == 'H2':
        while problem.heuristic_2(current) != 0 and sideway_walk > 0:
            neighbours = problem.near_state(current)
            if not neighbours:
                break
            # find neighbour with min H2+G
            neighbour = min(neighbours, key=lambda state: (problem.heuristic_2(state) + g))

            if problem.heuristic_2(neighbour) == problem.heuristic_2(current) and sideway_walk > 0:
                # find neighbour with the same value with current
                neighbour_side = [v for i, v in enumerate(neighbours) if
                                  problem.heuristic_2(v) == problem.heuristic_2(current)]
                neighbour = random.choice(neighbour_side)
                sideway_walk -= 1
                g += neighbour * neighbour * neighbour_side

            if problem.heuristic_2(neighbour) > problem.heuristic_2(current):
                break
            cost += problem.cost(neighbour, current)
            current = neighbour
            sequential_moves.append(current)

    return current, cost, sequential_moves, len(sequential_moves)


if __name__ == "__main__":
    print('filename:')
    filename=str(input())
    print('1 for A*, 2 for hill climbing:')
    algorithm = int(input())
    if algorithm == 1:
        print('H1 or H2:')
        heuristic = str(input())
        problem = Queen()
        state, total_length_node, total_cost, sequential_moves_restart, during_time = random_restart(problem, filename,heuristic)



    # problem = Queen()
    # filename = 'heavy queens board.csv'
    # filename = 'hc_test.csv'
    # state, total_length_node, total_cost, sequential_moves_restart, during_time = random_restart(problem, filename)
    # print(state)
    # print(total_length_node)
    # print(total_cost)
    # print(during_time)
    # print(sequential_moves_restart)