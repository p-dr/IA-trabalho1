from celluloid import Camera
from view import plot_board
from collections import deque
import utils as u


def search(board: list, origin: tuple,
           target: tuple, camera: Camera = None) -> list:

    def calc_path(parents: dict) -> list:
        """ Retorna o caminho desde a origem até o destino """
        path = [target]
        while path[-1] != origin:
            path.append(parents[path[-1]])
        return path

    visited = deque()
    visited.append(origin)
    parents = {}
    processed = set()
    processed.add(origin)

    while len(visited) != 0:
        pos = visited.popleft()
        if pos == target:
            return calc_path(parents)
        if pos != origin:
            # marca como visitado
            board[pos[0]][pos[1]] = .4

        # Invertido para ir nas diagonais por último.
        for move in u.available_moves(board, pos)[::-1]:
            if move not in processed:
                if move != target:
                    # marca como tocado
                    board[move[0]][move[1]] = .2
                visited.appendleft(move)
                processed.add(move)
                parents[move] = pos

        if camera is not None:
            plot_board(board)
            camera.snap()

    return None
