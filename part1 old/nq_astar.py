from NQueens import Queen
import timeit
import random
import queue
import numpy as np


def state_to_tuple(state):
    return tuple(np.nonzero(state.T)[1])


def a_star(q, filename,Heuristic):
    state = q.input_board(filename)
    start = state_to_tuple(state)

    frontier = []
    frontier.append((0, state))

    come_from = {}
    cost_so_far = {}
    come_from[start] = None
    cost_so_far[start] = 0
    result = None
    start = timeit.default_timer()
    if Heuristic == 'H1':
        while frontier:
            #         sorted(graded, key=lambda x: x[0])
            frontier.sort(key=lambda x: x[0], reverse=True)
            current = frontier.pop()

            if q.heuristic_1(current[-1]) == 0:
                result = current[-1]
                break
            for next in q.near_state(current[-1]):
                new_cost = cost_so_far[state_to_tuple(current[-1])] + q.cost(current[-1], next)

                if state_to_tuple(next) not in cost_so_far:
                    cost_so_far[state_to_tuple(next)] = new_cost

                    priority = new_cost + q.heuristic_1(next)
                    frontier.append((priority, next))

                    come_from[state_to_tuple(next)] = state_to_tuple(current[-1])

            end = timeit.default_timer()

            if (end - start) > 10:
                break
    if Heuristic == 'H2':
        while frontier:
            #         sorted(graded, key=lambda x: x[0])
            frontier.sort(key=lambda x: x[0], reverse=True)
            current = frontier.pop()

            if q.heuristic_2(current[-1]) == 0:
                result = current[-1]
                break
            for next in q.near_state(current[-1]):
                new_cost = cost_so_far[state_to_tuple(current[-1])] + q.cost(current[-1], next)

                if state_to_tuple(next) not in cost_so_far:
                    cost_so_far[state_to_tuple(next)] = new_cost

                    priority = new_cost + q.heuristic_2(next)
                    frontier.append((priority, next))

                    come_from[state_to_tuple(next)] = state_to_tuple(current[-1])

            end = timeit.default_timer()

            if (end - start) > 10:
                break


    end = timeit.default_timer()
    during_time = end - start
    node_expanded = len(cost_so_far)
    return state, node_expanded, during_time, result

if __name__ == "__main__":
    filename = 'heavy queens board.csv'
    q = Queen()
    state, node_expanded, during_time, result = a_star(q, filename,'H1')
    print('start states: ')
    print(state)
    print('end state: ')
    print(result)
    print(during_time)
    print(node_expanded)


