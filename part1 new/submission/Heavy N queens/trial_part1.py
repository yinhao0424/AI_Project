from nq_hillclimbing import hill_climbing
from nq_astar import a_star

import numpy as np
import random
import csv

class generate_board():
    def __init__(self,N):
        self.N =N
        self.board = np.zeros((self.N,self.N))

    def random_board(self):
        for column in range(self.N):
            row = random.randint(0,self.N-1)
            value = [9,3,1,4,2,5,6,8,3,7,4,2,5,1,5,3,1,4,2,5,6,8,3,7,4,2,5,1]
            self.board[row,column] = value[column]

    def write_csv(self):
        self.random_board()
        np.savetxt('data'+str(self.N)+'.csv', self.board, fmt="%d", delimiter=",")
        # wtr = csv.writer(open ('out.csv', 'w'), delimiter=',', lineterminator='\n')
        # for x in self.board : wtr.writerow ([x])

print('---------------------------------------')

for i in range(10):

    gd = generate_board(6)
    gd.write_csv()

    print('trail '+str(i))

    filename = 'heavy queens board.csv'
    astar = a_star(filename, "H2")
    astar.a_star()

    #
    # print('The effective branching factor:')
    # print(astar.effective_branching_factor)
    #
    print("The total cost: ")
    print(astar.total_cost)

    # print('The sequence of moves:')
    # print(astar.sequential_moves[::-1])
    #
    # print('Final state')





print('---------------------------------------')

# success = 0
# time = []
# branch_factor = []
# # 28个
# # value = [9,3,1,4,2,5,6,8,3,7,4,2,5,1,5,3,1,4,2,5,6,8,3,7,4,2,5,1]
# # print(len(value))
# for i in range(10):
#
#     gd = generate_board(5)
#     gd.write_csv()
#
#     print('trail '+str(i))
#
#     filename = 'data5.csv'
#     astar = a_star(filename, "H2")
#     astar.a_star()
#
#
#     print('The effective branching factor:')
#     print(astar.effective_branching_factor)
#
#     print("The total cost: ")
#     print(astar.total_cost)
#
#     print('The sequence of moves:')
#     print(astar.sequential_moves[::-1])
#
#     print('Final state')
#     print(astar.result)
#
#     if astar.result is not None:
#         branch_factor.append(astar.effective_branching_factor)
#         success +=1
#
# print('---------------------------------------')
# print(branch_factor)
# print('success rate: ')
# print(success/10 )
#
# print(sum(branch_factor)/10)

"""
gd = generate_board(18)
gd.write_csv()

for i in range(10):

    gd = generate_board(25)
    gd.write_csv()

    print('trail '+str(i))
    hc = hill_climbing('data25.csv', "H2")
    hc.restarts()
    # print('Start state:')
    # print(hc.start_state)

    print("The cost: ")
    print(hc.cost)

    print("Time to solve the puzzle: ")
    print(hc.during_time)

    print(hc.heuristic_1(hc.current))
    print('restarts '+str(hc.restart))
    if hc.heuristic_1(hc.current) == 0:
        success += 1
        time.append(hc.during_time)
        print('solved')
print('---------------------------------------')
print(time)
print('success rate: ')
print(success/10 )


"""

# for i in range(10):
#
#     hc1 = hill_climbing('data.csv', "H1")
#     hc1.restarts()
#
#     if hc1.heuristic_1(hc1.current)== 0:
#         success_1 += 1
#         print('solved')
#     print(i)
#
# print('____________________________')
# print('done')
# print(success_1)
