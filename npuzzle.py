import sys
import argparse
import re
import time
from heapq import heappush, heappop
from PyQt5.QtWidgets import QApplication

from npuzzle_graph import NpuzzleGraph
from npuzzle_state import NpuzzleState
from npuzzle_visu import Visu_option
from npuzzle_visu import Visu_npuzzle

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
            raise Exception("parsing")
        if len(temp) > 0:
            if dim == None:
                dim = int(temp[0])
                if dim < 3:
                    raise Exception("parsing")
                pass
            else:
                if re.match(r"^[ ]*(\d+)([ ]+\d+){" + re.escape(str(dim - 1)) + r"}(([ ]*[#].*$)|$)", line) is None:
                    raise Exception("parsing")
                else:
                    puzzle_valid.append([int(c) for c in line.split() if c.isdigit()][:dim])
    if not check_continuity(puzzle_valid):
        raise Exception("parsing")
    ret = []
    for lst in puzzle_valid:
        ret.extend(lst)
    return ret, dim

def a_star(graph):
    dep = NpuzzleState(graph.puzzle.copy(), graph.len, 0, graph.heuristic(graph.puzzle), None, graph.cost)
    heappush(graph.open, dep)
    graph.open_set[dep.tuple] = dep
    size = graph.len
    time_complexity = 0
    while True:
        time_complexity += 1
        tmp_s_c = len(graph.open) + len(graph.closed)
        if tmp_s_c > graph.size_complexity:
            graph.size_complexity = tmp_s_c
        current = heappop(graph.open)
        del graph.open_set[current.tuple]
        graph.closed.add(current.tuple)
        if current.puzzle == graph.objectif:
            graph.time_complexity = time_complexity
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

def n_puzzle(f, heuristic, cost, visu=False):
    if heuristic == None:
        heuristic = "linear_conflicts"
    if cost == None:
        cost = "a_star"

    with open(f, "r") as f:
        puzzle = f.read()
    try:
        puzzle, dim = parsing(puzzle)
    except Exception as e:
        if e.__str__() == "parsing":
            print("Error format in your N-puzzle file\n Please enter N-puzzle with size >= 3\n Exemple:\n  #comment\n  3 (dimention)\n  1 2 3\n  5 6 7\n  8 4 0\n")
        else:
            print(e)
        return

    if visu:
        app = QApplication(sys.argv)
        visu = Visu_option()
        visu2 = Visu_npuzzle(puzzle, dim)
        sys.exit(app.exec_())
        print("OK")
    else:
        graph = NpuzzleGraph(dim, puzzle, cost, heuristic)
        try:
            graph = NpuzzleGraph(dim, puzzle, cost, heuristic)
        except Exception as e:
            if e.__str__() == "unsolvable":
                print("Error taquin unsolvable")
            elif e.__str__() == "ErrorHeuristic":
                print("Error heuristic don't exist")
            elif e.__str__() == "ErrorCost":
                print("Error cost don't exist")
            else:
                print(e)
            return
        start = time.time()
        res = a_star(graph)
        print_solution(res, graph, time.time() - start)
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("puzzle_file", help="Please enter N-Puzzle file")
    parser.add_argument("-v", "--visu", help="Display window", action="store_true")
    parser.add_argument("--heuristic", type=str, choices=["manhattan", "hamming", \
            "euclidienne", "linear_conflicts"], help="Choose your heuristic (by default Linear conflicts is used)")
    parser.add_argument("--cost", type=str, choices=["a_star", "greedy_searches", \
            "uniform_cost"], help="Choose your cost function (a_start = h + g, greedy_searches = h, uniform_cost = g)")
    args = parser.parse_args()
    n_puzzle(args.puzzle_file, args.heuristic, args.cost, args.visu)
