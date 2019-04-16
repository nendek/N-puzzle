class NpuzzleGraph():
    def __init__(self, len_puzzle, puzzle, objectif):
        self.len = len_puzzle
        self.puzzle = puzzle
        self.objectif = objectif
        self.simulation = []

    def __str__(self):
        ret = ""
        ret += "len = {}\n".format(self.len)

        ret += "puzzle =\n"
        for i in range(self.len):
            ret += "\t{}\n".format(self.puzzle[i * self.len:(i + 1) * self.len])
        
        ret += "current =\n"
        if len(self.simulation) > 0:
            for i in range(self.len):
                ret += "\t{}\n".format(self.simulation[i * self.len:(i + 1) * self.len])
        else:
            ret += "\tNone\n"
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

    def heuristique_nb_coups(self):
        total = 0
        for index in range(0, len(self.simulation)):
            total += abs(floor(self.objectif.index(self.simulation[index]) % self.len) - floor(index % self.len)) + abs(floor(self.objectif.index(self.simulation[index]) / self.len) - floor(index / self.len))
        return total
    
    def swap(pos1, pos2, lst):
        tmp = lst[pos1]
        lst[pos1] = lst[pos2]
        lst[pos2] = tmp
    
    def move_puzzle(self, direction):
        """
        1 = left
        2 = bot
        3 = right
        4 = up
        """
        if direction == 1:
            swap(self.simulation.index(0), self.simulation.index(0) - 1, self.simulation)
        if direction == 2:
            swap(self.simulation.index(0), self.simulation.index(0) + self.len, self.simulation)
        if direction == 3:
            swap(self.simulation.index(0), self.simulation.index(0) + 1, self.simulation)
        if direction == 4:
            swap(self.simulation.index(0), self.simulation.index(0) - self.len, self.simulation)

    def get_better_next_state(self):
        """
        Pour l'instant cette fonction prend juste le meilleur h pour le prochain coup
        """
        score_left = -1
        score_right = -1
        score_up = -1
        score_bot = -1
        
        index_0 = self.puzzle.index(0)
        # try left move
        if index_0 % self.len != 0:
            self.simulation = self.puzzle.copy()
            move_puzzle(self, 1)
        
        # try bot move
        if floor(index_0 / self.len) != self.len:
            self.simulation = self.puzzle.copy()
            move_puzzle(self, 2)
            
        # try right move
        if index_0 % self.len != self.len:
            self.simulation = self.puzzle.copy()
            move_puzzle(self, 3)
            
        # try up move
        if floor(index_0 / self.len) != 0:
            self.simulation = self.puzzle.copy()
            move_puzzle(self, 4)
    

