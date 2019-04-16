from math import floor

class NpuzzleGraph():
    def __init__(self, len_puzzle, puzzle, objectif):
        self.len = len_puzzle
        self.puzzle = puzzle
        self.objectif = objectif
#        self.simulation = []
        self.closed = set()
        self.open = []

    def __str__(self):
        ret = ""
        ret += "len = {}\n".format(self.len)

        ret += "puzzle =\n"
        for i in range(self.len):
            ret += "\t{}\n".format(self.puzzle[i * self.len:(i + 1) * self.len])
        
#        ret += "current =\n"
#        if len(self.simulation) > 0:
#            for i in range(self.len):
#                ret += "\t{}\n".format(self.simulation[i * self.len:(i + 1) * self.len])
#        else:
#            ret += "\tNone\n"

        ret += "objectif =\n"
        for i in range(self.len):
            ret += "\t{}\n".format(self.objectif[i * self.len:(i + 1) * self.len])

        return ret

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

    def handle_next_state(self, state):
        """
        Pour l'instant cette fonction prend juste le meilleur h pour le prochain coup
        """
        
        index_0 = self.puzzle.index(0)
        # try left move
        if index_0 % self.len != 0:
            simulation = state.puzzle.copy()
            self.move_puzzle(1, simulation)
            print(simulation)
        
        # try bot move
        if floor(index_0 / self.len) != self.len:
            simulation = self.puzzle.copy()
            self.move_puzzle(2, simulation)
            print(simulation)
            
        # try right move
        if index_0 % self.len != self.len:
            simulation = self.puzzle.copy()
            self.move_puzzle(3, simulation)
            print(simulation)
            
        # try up move
        if floor(index_0 / self.len) != 0:
            simulation = self.puzzle.copy()
            self.move_puzzle(4, simulation)
            print(simulation)
    

