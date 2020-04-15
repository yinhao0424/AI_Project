
from nq_astar import a_star
from nq_hillclimbing import hill_climbing

import argparse


if __name__ == "__main__":
    """
    1 for A*, 2 for greedy hill climbing
    'heavy queens board.csv' 1 H2
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument('algorithm', type=int)
    parser.add_argument("heuristic", type=str, help="H1 or H2")

    args = parser.parse_args()
    if args.algorithm == 1:
        astar = a_star(args.filename, args.heuristic)
        astar.a_star()

        print('Start state:')
        print(astar.start_state)

        print('The number of nodes expanded:')
        print(astar.node_expand)

        print("Time to solve the puzzle: ")
        print(astar.during_time)

        print('The effective branching factor:')
        print(astar.effective_branching_factor)

        print("The total cost: ")
        print(astar.total_cost)

        print('The sequence of moves:')
        print(astar.sequential_moves[::-1])

        print('Final state')
        print(astar.result)

    elif args.algorithm == 2:
        hc = hill_climbing(args.filename, args.heuristic)
        hc.restarts()
        print('Start state:')
        print(hc.start_state)
        print('The number of nodes expanded:')
        print(hc.expanded_node)
        print("Time to solve the puzzle: ")
        print(hc.during_time)
        print('The effective branching factor:' + str(1))
        print("The total cost: ")
        print(hc.total_cost)
        print('The sequence of moves with restart:')
        print(hc.sequential_moves_restart)

        print('The number of restarts')
        print(hc.restart)

        print('Final state')
        print(hc.current)

