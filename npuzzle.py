import argparse
import re
import time
from heapq import heappush, heappop
from npuzzle_graph import NpuzzleGraph
from npuzzle_state import NpuzzleState

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
    ret = []
    for lst in puzzle_valid:
        ret.extend(lst)
    return ret, dim




def a_star(graph):
    heappush(graph.open, (NpuzzleState(graph.puzzle.copy(), graph.len, 0, graph.heuristic(graph.puzzle))))
    while True:
        graph.time_complexity += 1
        tmp_s_c = len(graph.open) + len(graph.closed)
        if tmp_s_c > graph.size_complexity:
            graph.size_complexity = tmp_s_c
        if len(graph.open) == 0:
            raise("Unsolvable")
        current = heappop(graph.open)
        graph.closed.add(current.tuple)
        if current.puzzle == graph.objectif:
            return current
        graph.handle_next_state(current)


def print_solution(result, graph, true_time):
    tot = []
    while result:
        tot.insert(0, result)
        result = result.parent
    for elem in tot:
        print(elem)
    print("time complexity =", graph.time_complexity)
    print("size complexity =", graph.size_complexity)
    print("time duration =", true_time)

def n_puzzle(f):
    with open(f, "r") as f:
        puzzle = f.read()
    try:
        puzzle, dim = parsing(puzzle)
    except:
        print("Error")
        return

    graph = NpuzzleGraph(dim, puzzle)
    if graph.is_solvable() == False:
        print("Error taquin unsolvable")
        return
    start = time.time()
    res = a_star(graph)
    print_solution(res, graph, time.time() - start)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("puzzle_file", help="Please enter N-Puzzle file")
    args = parser.parse_args()
    n_puzzle(args.puzzle_file)
