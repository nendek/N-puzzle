class NpuzzleLc():
    def __init__(self, tile, nb_conflicts):
        self.tile = tile
        self.nb = nb_conflicts
        self.conflicts = []

    def decrem(self):
        if self.nb != 0:
            self.nb -= 1

    def __lt__(self, other):
        return self.nb > other.nb
