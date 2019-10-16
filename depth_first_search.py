from utils import available_moves
from collections import deque


def search(board: list, origin: tuple, target: tuple) -> list:

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

    while len(visited) != 0:
        pos = visited.popleft()
        if pos == target:
            return calc_path(parents)
        if pos != origin:
            # visitado
            board[pos[0]][pos[1]] = .4

        # Invertido para ir nas diagonais por último.
        for move in available_moves(board, pos)[::-1]:
            if move not in processed:
                # tocado
                board[move[0]][move[1]] = .2
                visited.appendleft(move)
                parents[move] = pos
        processed.add(pos)

    return None
