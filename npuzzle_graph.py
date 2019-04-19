import time
from math import floor, sqrt
from heapq import heappush, heappop, heapify
from npuzzle_state import NpuzzleState
from npuzzle_lc import NpuzzleLc
from itertools import permutations

class NpuzzleGraph():
    def __init__(self, len_puzzle, puzzle):
        self.len = len_puzzle
        self.puzzle = puzzle
        self.is_solvable()
        self.range_len_puzzle_cot = range(len_puzzle)
        self.range_len_puzzle = range(len(puzzle))
        self.create_objectif()
        self.open = []
        self.closedq = []
        self.open_set = {}
        self.closed = set()
        self.size_complexity = 0
        self.time_complexity = 0
#        self.heuristic = self.heuristique_manhattan
#        self.heuristic = self.heuristique_euclidienne
        self.heuristic = self.heuristique_linear_conflicts #TODO modified by option
        self.cost = 1                                      #TODO modified by option
        self.create_rows()
        self.create_cols()
        self.create_table_rows()
        self.create_table_cols()
        self.precalc_manhattan()
        self.precalc_euclidienne()
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

    def precalc_euclidienne(self):
        self.euclidienne_cost = {}
        self.euclidienne_cost = {tuile: {pos: sqrt(((pos % self.len) - (self.objectif.index(tuile) % self.len))**2 + (floor(pos / self.len) - floor(self.objectif.index(tuile) / self.len))**2 ) for pos in self.range_len_puzzle} for tuile in self.range_len_puzzle}

    def precalc_manhattan(self):
        self.manhattan_cost = {}
        self.manhattan_cost = {tuile: {pos: abs((pos % self.len) - (self.objectif.index(tuile) % self.len)) + abs(floor(pos / self.len) - floor(self.objectif.index(tuile) / self.len)) for pos in self.range_len_puzzle} for tuile in self.range_len_puzzle}
    
    def create_rows(self):
        self.ref_row = []
        for i in range(self.len):
            self.ref_row.append(self.objectif[(i * self.len):((i + 1) * self.len)])

    def create_cols(self):
        self.ref_col = []
        for i in range(self.len):
            col = []
            for j in range(len(self.objectif)):
                if j % self.len == i:
                    col.append(self.objectif[j])
            self.ref_col.append(col)

    def is_solvable(self):
        nb_swap = 0
        for tiles in self.puzzle:
            if tiles == 0:
                continue
            for index in range(self.puzzle.index(tiles) + 1, len(self.puzzle)):
                if tiles > self.puzzle[index] and self.puzzle[index] != 0:
                    nb_swap += 1

        if self.len % 2 == 1 and nb_swap % 2 == 0:
            if (self.len - 2) % 8 <= 3:
                raise Exception("unsolvable")
        if self.len % 2 == 0:
            if nb_swap % 2 == 1:
                if floor(self.puzzle.index(0) / self.len) % 2 == 1:
                    if (self.len - 2) % 8 <= 3:
                        raise Exception("unsolvable")
        if self.len % 2 == 0:
            if nb_swap % 2 == 0:
                if floor(self.puzzle.index(0) / self.len) % 2 == 0:
                    if (self.len - 2) % 8 <= 3:
                        raise Exception("unsolvable")
        if (self.len - 2) % 8 > 3:
            raise Exception("unsolvable")
        return True

    def create_objectif(self):
        """
        1 = right
        2 = down
        3 = left
        4 = up
        """
        tmp = list(self.range_len_puzzle)
        objectif = ['x' for i in self.range_len_puzzle]
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
            

#        self.objectif = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
        self.objectif = objectif

    def get_lc(self, tile, row, ref_row):
        if tile not in ref_row or tile == 0 or tile == 'x':
            return None
        ret = NpuzzleLc(tile, 0)
        for elem in row:
            if elem in ref_row and elem != 'x' and elem != 0:
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

    def create_table_rows(self):
        dico = {}
        for index in range(len(self.ref_row)):
            perm = permutations(self.ref_row[index])
            # second, calc it with graph.get_linear_sum
            for elem in perm:
                cost = self.get_linear_sum(elem, self.ref_row[index])
                # third: save it
                dico[tuple(elem)] = cost

            for i in range(len(self.ref_row)):
                cp = self.ref_row[index].copy()
                cp[i] = 'x'
                perm = permutations(cp)
                for elem in perm:
                    cost = self.get_linear_sum(elem, cp)
                    dico[tuple(elem)] = cost

        self.dic_row = dico

    def create_table_cols(self):
        dico = {}
        for index in range(len(self.ref_col)):
            perm = permutations(self.ref_col[index])
            # second, calc it with graph.get_linear_sum
            for elem in perm:
                cost = self.get_linear_sum(elem, self.ref_col[index])
                # third: save it
                dico[tuple(elem)] = cost

            for i in range(len(self.ref_col)):
                cp = self.ref_col[index].copy()
                cp[i] = 'x'
                perm = permutations(cp)
                for elem in perm:
                    cost = self.get_linear_sum(elem, cp)
                    dico[tuple(elem)] = cost
        self.dic_col = dico

    def heuristique_linear_conflicts(self, puzzle):
        start_time = time.time()
        m_d = self.heuristique_manhattan(puzzle)
        total_to_add = 0
        lsize = self.len
        dic_row = self.dic_row
        dic_col = self.dic_col
        range_len_puzzle = self.range_len_puzzle
        range_len_puzzle_cot = self.range_len_puzzle_cot
        ref_row = self.ref_row
        ref_col = self.ref_col
        
        for i in range_len_puzzle_cot:
            row = puzzle[(i * lsize):((i + 1) * lsize)]
            if tuple([x if x in ref_row[i] else 'x' for x in row]) in dic_row:
#                print(tuple([x if x in ref_row[i] else 'x' for x in row]), dic_row[tuple([x if x in ref_row[i] else 'x' for x in row])])
                total_to_add += 2 * dic_row[tuple([x if x in ref_row[i] else 'x' for x in row])]
        for i in range_len_puzzle_cot:
            col = []
            for j in range_len_puzzle:
                if j % lsize == i:
                    col.append(puzzle[j])
            if tuple([x if x in ref_col[i] else 'x' for x in col]) in dic_col:
#                print(tuple([x if x in ref_col[i] else 'x' for x in col]),dic_col[tuple([x if x in ref_col[i] else 'x' for x in col])])
                total_to_add += 2 * dic_col[tuple([x if x in ref_col[i] else 'x' for x in col])]
        self.time1 += time.time() - start_time
#        print(total_to_add)
        return m_d + total_to_add

    def heuristique_hamming(self, puzzle):
        total = 0
        objectif = self.objectif
        for index in self.range_len_puzzle:
            if puzzle[index] != objectif[index]:
                total += 1
        return total

    def heuristique_manhattan(self, puzzle):
        total = 0
        manhattan_cost = self.manhattan_cost
        for index in self.range_len_puzzle[1:]:
            total += manhattan_cost[index][puzzle.index(index)]
        return total
    
    def heuristique_euclidienne(self, puzzle):
        total = 0
        euclidienne_cost = self.euclidienne_cost
        for index in self.range_len_puzzle[1:]:
            total += euclidienne_cost[index][puzzle.index(index)]
        return total


    def swap(self, pos1, pos2, lst):
        lst[pos1], lst[pos2] = lst[pos2], lst[pos1]
    
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
        new_state = NpuzzleState(simulation, self.len, state.g + 1, self.heuristic(simulation), state, self.cost)
        new_state.parent = state

        if new_state.tuple in self.open_set.keys():
            old_one = self.open_set[new_state.tuple]
            if new_state.f < old_one.f:
                old_one.f = new_state.f
                old_one.g = new_state.g
                old_one.h = new_state.h
#                heappush(self.open, new_state)
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
