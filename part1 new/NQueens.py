# MODELAGEM DO PROBLEMA DE N-RAINHAS
from random import choice
from collections import Counter
from random import randrange


# Generic class of search problems
class SearchProblem:
    #
    # Starts the search (receives the initial parameters)
    def __init__(self, initial=None):
        pass

    # Define o estado inicial
    def initial(self):
        pass

    # Teste de objetivo
    def goal_test(self, state):
        pass

    # Heuristica, utilizada para problemas de maximizacao ou minimizacao
    def heuristic(self, state):
        pass

    # Returns the states accessible from the current state
    def nearStates(self, state):
        pass

    # Retorna uma escolha aleatoria dentre os estados proximos
    def randomNearState(self, state):
        return choice(self.nearStates(state))


# Implementacao do modelo do problema das n-rainhas, sobrescrevendo a classe SearchProblem
class NQueensSearch(SearchProblem):
    # Modelo de um estado
    #
    # State: ([line_queens],
    #        (a, b, c),
    #        (h)
    #
    # Onde:
    # a: guarda o valor da coluna das rainhas
    # b: guarda l-c das rainhas
    # c: guarda l+c das rainhas
    # h: valor da heuristica do estado
    # A verificacao se da para cada rainha do tabuleiro, onde e testado
    # se existe outra rainha ja visitada com os mesmos valores de a,b,c.
    # caso exista, nao e um estado objetivo

    def __init__(self, N):
        self.N = N

    # Estado inicial:
    #   Retorna o estado inicial a partir do size
    def initial(self):
        return list(randrange(self.N) for i in range(self.N))

    # Teste de objetivo:
    #
    # Tests if any row / column / diagonal is populated by more than one queen
    def goal_test(self, state):
        a, b, c = (set() for i in range(3))
        for row, col in enumerate(state):
            if col in a or row - col in b or row + col in c:
                return False
            a.add(col)
            b.add(row - col)
            c.add(row + col)
        return True

    # Heuristica: h
    # Number of pairs of queens attacking each other
    def heuristic(self, state):
        #define a, b, c as counters
        a, b, c = [Counter() for i in range(3)]

        # count how many queens the values ​​have (a, b, c)
        # so that you get for example how many queens has the value of a = 1
        for row, col in enumerate(state):
            a[col] += 1
            b[row - col] += 1
            c[row + col] += 1
        h = 0  # start collisions with 0
        # scans the counting structures (a, b, c) just increasing the collision value
        # case for some value of (a / b / c)> 1 since cnt is done [key] -1
        # divides to remove double counts
        for count in [a, b, c]:
            for key in count:
                h += count[key] * (count[key] - 1) / 2
        return -h

    # Children ou estados vizinhos: children[]
    #   Returns all accessible states from the current one by moving the pieces by column
    def nearStates(self, state):
        near_states = []
        #
        # For each state [column] it checks if the neighboring columns are empty
        for row in range(self.N):
            for col in range(self.N):
                # If different:
                # then the current iteration col is available to move around
                # since state [] stores the value of the columns where the queens are
                if col != state[row]:
                    aux = list(state)
                    aux[row] = col  # Switch column to empty
                    near_states.append(list(aux))  # And include in the list of nearStates
        return near_states

