from heapq import heappush, heappop

from npuzzle_state import NpuzzleState

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
