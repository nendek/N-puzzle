import argparse
import re

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("puzzle_file", help="Please enter N-Puzzle file")
    args = parser.parse_args()
    f = args.puzzle_file
    f = open(f, "r")
    puzzle = f.read()
    puzzle = puzzle.split('\n')
    puzzle_valid = []
    dim = None
    for line in puzzle:
        if len(line) == 0:
            break
        if line[0] != '#' and not line[0].isdigit():
            print("File format error")
            break
        temp = re.findall(r"^(\d+)", line)
        if len(temp) > 0:
            if dim == None:
                dim = int(temp[0])
                pass
            else:
                print(re.findall(r"^(\d+)([ ]\d+){" + re.escape(str(dim - 1)) + r"}", line))
                if re.match(r"^(\d+)([ ]\d+){" + re.escape(str(dim - 1)) + r"}(([ ][#].*$)|$)", line) is None:
                    print("File format error")
                    break
                    
