from up_map import Map
from up_hill_climbing import hill_climbing
from up_genetic import genetic

import argparse


if __name__ == '__main__':
    """
       1 for A*, 2 for greedy hill climbing
       'urban 1.txt' HC
       """
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument('algorithm', type=str,help="HC or GA")

    args = parser.parse_args()


    if args.algorithm == 'GA':
        ga = genetic(args.filename)
        ga.genetic_algorithm()

        result = ga.result
        ga.map_board = ga.map_board.astype(str)

        for row in range(ga.map_board.shape[0]):
            for col in range(ga.map_board.shape[1]):
                if ga.map_board[row, col] == '10':
                    ga.map_board[row, col] = 'X'
                elif ga.map_board[row, col] == '11':
                    ga.map_board[row, col] = 'S'

        for i in range(result[2].shape[0]):
            for j in range(result[2].shape[1]):
                if result[2][i, j] == 12:
                    ga.map_board[i, j] = 'I'
                elif result[2][i, j] == 13:
                    ga.map_board[i, j] = "R"
                elif result[2][i, j] == 14:
                    ga.map_board[i, j] = "C"

        print(ga.map_board)

        output = open("urban planning GA.txt", 'w')
        print("The score for best map is: ", result[0], file=output)
        print("The time that score was first achieved:", -result[1], file=output)
        print("The map of the city:", file=output)
        print(ga.map_board, file=output)
        output.close()

    elif args.algorithm == 'HC':
        hc = hill_climbing(args.filename)
        hc.climb()

        result = hc.result
        hc.map_board = hc.map_board.astype(str)

        for row in range(hc.map_board.shape[0]):
            for col in range(hc.map_board.shape[1]):
                if hc.map_board[row, col] == '10':
                    hc.map_board[row, col] = 'X'
                elif hc.map_board[row, col] == '11':
                    hc.map_board[row, col] = 'S'

        for i in range(result[2].shape[0]):
            for j in range(result[2].shape[1]):
                if result[2][i, j] == 12:
                    hc.map_board[i, j] = 'I'
                elif result[2][i, j] == 13:
                    hc.map_board[i, j] = "R"
                elif result[2][i, j] == 14:
                    hc.map_board[i, j] = "C"

        print(hc.map_board)

        output = open("urban planning HC.txt", 'w')
        print("The score for best map is: ", result[0], file=output)
        print("The time that score was first achieved:", -result[1], file=output)
        print("The map of the city:", file=output)
        print(hc.map_board, file=output)
        output.close()
    else:
        print('Please pass the correct arguments')
