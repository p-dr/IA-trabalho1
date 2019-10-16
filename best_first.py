from utils import available_moves, str2n, trapezoidal_dist
from heapq import heappush, heappop


def search(board, start, goal):
    queue = [(0, [start])]
    processed = set()
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
            if move not in processed:
                heappush(queue, (trapezoidal_dist(move, goal), path + [move]))
                board[move[0]][move[1]] = .2

        processed.add(curr)
    board[start[0]][start[1]] = str2n['#']
    return path
