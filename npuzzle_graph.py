from math import floor
from heapq import heappush, heappop
from npuzzle_state import NpuzzleState

class NpuzzleGraph():
    def __init__(self, len_puzzle, puzzle, objectif):
        self.len = len_puzzle
        self.puzzle = puzzle
        self.objectif = objectif
        self.closed = set()
        self.open = []
        self.size_complexity = 0
        self.time_complexity = 0

    def __str__(self):
        ret = ""
        ret += "len = {}\n".format(self.len)

        ret += "puzzle =\n"
        for i in range(self.len):
            ret += "\t{}\n".format(self.puzzle[i * self.len:(i + 1) * self.len])
        
        ret += "objectif =\n"
        for i in range(self.len):
            ret += "\t{}\n".format(self.objectif[i * self.len:(i + 1) * self.len])

        return ret

    def is_solvable(self):
        nb_swap = 0
        copy = self.puzzle.copy()
        while copy != self.objectif:
            nb_swap += 1
            for i in range(len(copy)):
                if copy[i] != self.objectif[i]:
                    self.swap(i, copy.index(self.objectif[i]), copy)
                    break
        if nb_swap % 2 == 0:
            return True
        return False

    def heuristique_placement(self):
        total = 0
        for index in range(0, len(self.simulation)):
            if self.simulation[index] != self.objectif[index]:
                total += 1
        return total

    def heuristique_nb_coups(self, puzzle):
        total = 0
        for index in range(0, len(puzzle)):
            total += abs(floor(self.objectif.index(puzzle[index]) % self.len) - floor(index % self.len)) + abs(floor(self.objectif.index(puzzle[index]) / self.len) - floor(index / self.len))
        return total
    
    def swap(self, pos1, pos2, lst):
        tmp = lst[pos1]
        lst[pos1] = lst[pos2]
        lst[pos2] = tmp
    
    def move_puzzle(self, direction, simulation):
        """
        1 = left
        2 = bot
        3 = right
        4 = up
        """
        if direction == 1:
            self.swap(simulation.index(0), simulation.index(0) - 1, simulation)
        if direction == 2:
            self.swap(simulation.index(0), simulation.index(0) + self.len, simulation)
        if direction == 3:
            self.swap(simulation.index(0), simulation.index(0) + 1, simulation)
        if direction == 4:
            self.swap(simulation.index(0), simulation.index(0) - self.len, simulation)

    def handle_open_close(self, state, simulation):
        new_state = NpuzzleState(simulation, self.len, state.g + 1, self.heuristique_nb_coups(simulation))
        new_state.parent = state
        found = False
        for i in range(len(self.open)):
            if new_state.puzzle == self.open[i].puzzle:
                found = True
                if new_state.f < self.open[i].f:
                    self.open.pop(i)
                    heappush(self.open, new_state)
                break

        if new_state.tuple in self.closed:
            found = True

        if found == False:
            heappush(self.open, new_state)


    def handle_next_state(self, state):
        """
        Pour l'instant cette fonction prend juste le meilleur h pour le prochain coup
        """
        
        index_0 = state.puzzle.index(0)
        # try left move
        if index_0 % self.len != 0:
            simulation = state.puzzle.copy()
            self.move_puzzle(1, simulation)
            self.handle_open_close(state, simulation)
        
        # try bot move
        if floor(index_0 / self.len) != self.len - 1:
            simulation = state.puzzle.copy()
            self.move_puzzle(2, simulation)
            self.handle_open_close(state, simulation)
            
        # try right move
        if index_0 % self.len != self.len - 1:
            simulation = state.puzzle.copy()
            self.move_puzzle(3, simulation)
            self.handle_open_close(state, simulation)
            
        # try up move
        if floor(index_0 / self.len) != 0:
            simulation = state.puzzle.copy()
            self.move_puzzle(4, simulation)
            self.handle_open_close(state, simulation)
    

