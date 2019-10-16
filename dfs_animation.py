from celluloid import Camera
import matplotlib.pyplot as plt
from view import show_board
from utils import available_moves
from collections import deque


def search(board: list, origin: tuple, target: tuple) -> list:

    def calc_path(parents: dict) -> list:
        """ Retorna o caminho desde a origem até o destino """
        path = [target]
        while path[-1] != origin:
            path.append(parents[path[-1]])
        return path

    fig = show_board(board, show=False)
    camera = Camera(fig)

    visited = deque()
    visited.append(origin)
    parents = {}
    processed = set()

    while len(visited) != 0:
        pos = visited.popleft()
        if pos == target:
            animation = camera.animate()
            animation.save('test.gif', writer='imagemagick')
            return calc_path(parents)

        # Invertido para ir nas diagonais por último.
        for move in available_moves(board, pos)[::-1]:
            # if move not in processed:
            board[move[0]][move[1]] = .2
            visited.appendleft(move)
            parents[move] = pos
        if pos != origin:
            board[pos[0]][pos[1]] = .4
        processed.add(pos)

        show_board(board, fig=fig, show=False)
        camera.snap()


    animation = camera.animate()
    animation.save('test.gif', writer='imagemagick')
    return None
