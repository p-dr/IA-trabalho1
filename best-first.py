from utils import available_moves, get_start


def heuristic(pos, goal):
    a = abs(pos[0] - goal[0])
    b = abs(pos[1] - goal[1])
    d = abs(a-b)
    return 2 ** .5 * min(a, b) + d


def best_first(board, start):
    queue = available_moves(board, start)
