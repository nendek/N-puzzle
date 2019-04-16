import argparse
import re

def check_continuity(tab):
    res = []
    for lst in tab:
        res.extend(lst)
    res.sort()
    if res != list(range(len(res))):
        return False
    return True

def parsing(puzzle):
    puzzle = puzzle.split('\n')
    puzzle_valid = []
    dim = None
    for line in puzzle:
        if len(line) == 0:
            break
        if line[0] != '#' and not line[0].isdigit():
            raise("FormatError")
        temp = re.findall(r"^(\d+)", line)
        if len(temp) > 0:
            if dim == None:
                dim = int(temp[0])
                pass
            else:
                if re.match(r"^(\d+)([ ]\d+){" + re.escape(str(dim - 1)) + r"}(([ ][#].*$)|$)", line) is None:
                    raise("FormatError")
                else:
                    puzzle_valid.append([int(c) for c in line.split() if c.isdigit()][:dim])
    if not check_continuity(puzzle_valid):
        raise("FormatError")
    return puzzle_valid


def n_puzzle(f):
    with open(f, "r") as f:
        puzzle = f.read()
    try:
        puzzle = parsing(puzzle)
    except:
        print("Error")
        return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("puzzle_file", help="Please enter N-Puzzle file")
    args = parser.parse_args()
    n_puzzle(args.puzzle_file)
