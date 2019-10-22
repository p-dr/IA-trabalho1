from celluloid import Camera
from view import plot_board
import utils as u
from heapq import heappush, heappop


def search(board: list, origin: tuple,
           target: tuple, camera: Camera = None) -> list:
    queue = [(0, [origin])]
    u.trapezoidal_dist.values = {origin: 0}
    processed = {origin}
    path = [None]

    while path[-1] != target:
        if not queue:
            path = None
            break

        path = heappop(queue)[1]
        curr = path[-1]
        if curr not in (origin, target):
            # marca como visitado
            board[curr[0]][curr[1]] = .4

        # Append moves
        for move in u.available_moves(board, path[-1]):
            if move not in processed:
                heappush(queue, (u.trapezoidal_dist(move, target),
                                 path + [move]))
                if move != target:
                    # marca como tocado
                    board[move[0]][move[1]] = .2
                processed.add(move)

        if camera is not None:
            plot_board(board)
            camera.snap()

    board[origin[0]][origin[1]] = u.str2n['#']
    return path
