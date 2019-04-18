import time
from math import floor, sqrt
from heapq import heappush, heappop, heapify
from npuzzle_state import NpuzzleState
from npuzzle_lc import NpuzzleLc

class NpuzzleGraph():
    def __init__(self, len_puzzle, puzzle):
        self.len = len_puzzle
        self.puzzle = puzzle
        self.create_objectif()
        self.open = []
        self.closedq = []
        self.open_set = {}
        self.closed = set()
        self.size_complexity = 0
        self.time_complexity = 0
#        self.heuristic = self.heuristique_manhattan
        self.heuristic = self.heuristique_linear_conflicts
        self.time1 = 0
        self.time2 = 0
        self.time3 = 0

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

    def create_objectif(self):
        """
        1 = right
        2 = down
        3 = left
        4 = up
        """
        objectif = ['x' for i in range(len(self.puzzle))]
        tmp = list(range(len(self.puzzle)))
        tmp.append(tmp.pop(0))
        ptr_o = 0
        orientation = 1
        for i in range(0, len(tmp)):
            objectif[ptr_o] = tmp[i]
            if orientation == 1:
                ptr_o += 1
                if ptr_o % self.len == self.len - 1:
                    orientation = 2
                if objectif[ptr_o] != 'x':
                    orientation = 2
                    ptr_o -= 1
                    ptr_o += self.len
            elif orientation == 2:
                ptr_o += self.len
                if floor(ptr_o / self.len) == self.len - 1:
                    orientation = 3
                if objectif[ptr_o] != 'x':
                    orientation = 3
                    ptr_o -= self.len
                    ptr_o -= 1
            elif orientation == 3:
                ptr_o -= 1
                if ptr_o % self.len == 0:
                    orientation = 4
                if objectif[ptr_o] != 'x':
                    orientation = 4
                    ptr_o += 1
                    ptr_o -= self.len
            elif orientation == 4:
                ptr_o -= self.len
                if floor(ptr_o /self.len) == 0:
                    orientation = 1
                if objectif[ptr_o] != 'x':
                    orientation = 1
                    ptr_o += self.len
                    ptr_o += 1
            
        self.objectif = objectif

    def get_lc(self, tile, row, ref_row):
        if tile not in ref_row:
            return None
        ret = NpuzzleLc(tile, 0)
        for elem in row:
            if elem in ref_row:
                if row.index(tile) < row.index(elem):
                    if ref_row.index(tile) > ref_row.index(elem):
                        ret.nb += 1
                        ret.conflicts.append(elem)
                if row.index(tile) > row.index(elem):
                    if ref_row.index(tile) < ref_row.index(elem):
                        ret.nb += 1
                        ret.conflicts.append(elem)
        if ret.nb == 0:
            return None
        return ret
                
    def get_linear_sum(self, line, ref_line):
        total_C = []
        lc = 0
        for elem in line:
            item = self.get_lc(elem, line, ref_line)
            if item:
                heappush(total_C, item)
        while len(total_C):
            popped = heappop(total_C)
            if popped.nb == 0:
                continue
            for elem in popped.conflicts:
                for elem2 in total_C:
                    if elem2.tile == elem:
                        elem2.decrem()
            heapify(total_C)
            lc += 1
        return (lc)

    def heuristique_linear_conflicts(self, puzzle):
        start_time = time.time()
        m_d = self.heuristique_manhattan(puzzle)
        total_to_add = 0

        for i in range(self.len):
            row = puzzle[(i * self.len):((i + 1) * self.len)]
            ref_row = self.objectif[(i * self.len):((i + 1) * self.len)]
            total_to_add += 2 * self.get_linear_sum(row, ref_row)
        for i in range(self.len):
            col = []
            ref_col = []
            for j in range(len(puzzle)):
                if j % self.len == i:
                    col.append(puzzle[j])
                    ref_col.append(self.objectif[j])
            total_to_add += 2 * self.get_linear_sum(col, ref_col)
        self.time1 += time.time() - start_time

        return m_d + total_to_add

    def heuristique_hamming(self, puzzle):
        total = 0
        for index in range(0, len(puzzle)):
            if puzzle[index] != self.objectif[index]:
                total += 1
        return total

    def heuristique_manhattan(self, puzzle):
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

#    def handle_open_close(self, state, simulation):
#        new_state = NpuzzleState(simulation, self.len, state.g + 1, self.heuristic(simulation))
#        new_state.parent = state
#        found = False
#        for i in range(len(self.open)):
#            if new_state.puzzle == self.open[i].puzzle:
#                found = True
#                if new_state.f < self.open[i].f:
#                    self.open.pop(i)
#                    heappush(self.open, new_state)
#                break
#
#        if new_state.tuple in self.closed:
#            found = True
#
#        if found == False:
#            heappush(self.open, new_state)


    def handle_open_close(self, state, simulation):
        new_state = NpuzzleState(simulation, self.len, state.g + 1, self.heuristic(simulation))
        new_state.parent = state

        if new_state.tuple in self.open_set.keys():
            old_one = self.open_set[new_state.tuple]
            if new_state.f < old_one.f:
                old_one.f = new_state.f
                old_one.g = new_state.g
                old_one.h = new_state.h
                start_time = time.time()
#                heappush(self.open, new_state)
                self.time2 += time.time() - start_time
        elif new_state.tuple in self.closed:
            pass
        else:
            heappush(self.open, new_state)
            self.open_set[new_state.tuple] = new_state


    def handle_next_state(self, state):
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
    

