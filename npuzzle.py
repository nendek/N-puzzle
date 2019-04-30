import sys
import argparse
import re
import time
from PyQt5.QtWidgets import QApplication

from npuzzle_graph import NpuzzleGraph
from npuzzle_visu import Visu_option
from npuzzle_visu import Visu_npuzzle
from npuzzle_algo import a_star

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
                    tmp = line.split("#")
                    tmp = tmp[0]
                    puzzle_valid.append([int(c) for c in tmp.split() if c.isdigit()][:dim])
    if not check_continuity(puzzle_valid):
        raise Exception("parsing")
    ret = []
    for lst in puzzle_valid:
        ret.extend(lst)
    return ret, dim

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
    try:
        with open(f, "r") as f:
            puzzle = f.read()
    except Exception as e:
        print("Error file input")
        return 
    try:
        puzzle, dim = parsing(puzzle)
    except Exception as e:
        if e.__str__() == "parsing":
            print("Error format in your N-puzzle file\n Please enter N-puzzle with size >= 3\n Exemple:\n  #comment\n  3 (size)\n  1 2 3\n  5 6 7\n  8 4 0\n")
        else:
            print(e)
        return

    if visu:
        app = QApplication(sys.argv)
        visu = Visu_option(puzzle, dim)
        visu.show()
        sys.exit(app.exec_())
    else:
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
            "uniform_cost"], help="Choose your cost function [a_star = h + g, greedy_searches = h, uniform_cost = g] (by default a_star is used)")
    args = parser.parse_args()
    n_puzzle(args.puzzle_file, args.heuristic, args.cost, args.visu)
