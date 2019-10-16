from utils import available_moves, str2n
from heapq import heappush, heappop


def heuristic(pos, goal):
    a = abs(pos[0] - goal[0])
    b = abs(pos[1] - goal[1])
    d = abs(a-b)
    return 2 ** .5 * min(a, b) + d


def search(board, start, goal):
    queue = [(0, [start])]
    path = [None]

    while path[-1] != goal:
        if not queue:
            path = None
            break
        # -1 ou 0?
        path = heappop(queue)[1]
        curr = path[-1]
        board[curr[0]][curr[1]] = .4

        # Append moves
        for move in available_moves(board, path[-1]):
            heappush(queue, (heuristic(move, goal), path + [move]))
            board[move[0]][move[1]] = .2

    board[start[0]][start[1]] = str2n['#']
    return path
