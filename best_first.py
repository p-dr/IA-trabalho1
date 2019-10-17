from celluloid import Camera
from view import plot_board
import utils as u
from heapq import heappush, heappop


def search(board: list, start: tuple,
           goal: tuple, camera: Camera = None) -> list:
    queue = [(0, [start])]
    u.trapezoidal_dist.values = {start: 0}
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
        for move in u.available_moves(board, path[-1]):
            if move not in processed:
                heappush(queue, (u.trapezoidal_dist(move, goal),
                                 path + [move]))
                board[move[0]][move[1]] = .2

        if camera is not None:
            plot_board(board)
            camera.snap()

        processed.add(curr)
    board[start[0]][start[1]] = u.str2n['#']
    return path
