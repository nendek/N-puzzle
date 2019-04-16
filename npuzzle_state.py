class NpuzzleState():
    def __init__(self, puzzle, len_puzzle, g, h):
        self.puzzle = puzzle
        self.f = h + g
        self.g = g
        self.h = h
        self.tuple = tuple(puzzle)
        self.len = len_puzzle
        self.parent = None
    
    def __str__(self):
        ret = ""
        ret += "f(x) = {}\n".format(self.f)
        ret += "g(x) = {}\n".format(self.g)
        ret += "h(x) = {}\n".format(self.h)
        ret += "puzzle =\n"
        for i in range(self.len):
            ret += "\t{}\n".format(self.puzzle[i * self.len:(i + 1) * self.len])
        
        return ret

    def __lt__(self, other):
        if self.f != other.f:
            return self.f < other.f

        if self.h != other.h:
            return self.h < other.h

        return self.g < other.g

