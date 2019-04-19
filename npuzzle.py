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
        temp2 = re.findall(r"^[ ]*[#]", line)
        temp = re.findall(r"^[ ]*(\d+)", line)
        if len(temp2) <= 0 and len(temp) <= 0:
            raise("FormatError")
        if len(temp) > 0:
            if dim == None:
                dim = int(temp[0])
                pass
            else:
                if re.match(r"^[ ]*(\d+)([ ]+\d+){" + re.escape(str(dim - 1)) + r"}(([ ]*[#].*$)|$)", line) is None:
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
    dep = NpuzzleState(graph.puzzle.copy(), graph.len, 0, graph.heuristic(graph.puzzle), None, graph.cost)
    heappush(graph.open, dep)
    graph.open_set[dep.tuple] = dep
    size = graph.len
    while True:
        graph.time_complexity += 1
#        print(graph.time_complexity)
#        if graph.time_complexity >= 40000:
#            return current
        tmp_s_c = len(graph.open) + len(graph.closed)
        if tmp_s_c > graph.size_complexity:
            graph.size_complexity = tmp_s_c
        current = heappop(graph.open)
        del graph.open_set[current.tuple]
        graph.closed.add(current.tuple)
        if current.puzzle == graph.objectif:
            return current
        graph.handle_next_state(current, size)


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
    print("time to bench 1 =", graph.time1)
    print("percentage = {:2.2f}%".format((graph.time1 / true_time) * 100))
    print("time to bench 2 =", graph.time2)
#    print("time to bench 2 =", graph.time2)

def n_puzzle(f):
    with open(f, "r") as f:
        puzzle = f.read()
    try:
        puzzle, dim = parsing(puzzle)
    except:
        print("Error")
        return

    try:
        graph = NpuzzleGraph(dim, puzzle)
    except Exception as e:
        if e.__str__() == "unsolvable":
            print("Error taquin unsolvable")
        else:
            print(e)
        return
    start = time.time()
    res = a_star(graph)
    print_solution(res, graph, time.time() - start)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("puzzle_file", help="Please enter N-Puzzle file")
    args = parser.parse_args()
    n_puzzle(args.puzzle_file)
