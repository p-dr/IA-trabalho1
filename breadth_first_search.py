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
    processed.add(origin)

    while len(visited) != 0:
        pos = visited.popleft()
        if pos == target:
            return calc_path(parents)
        # marca como visitado
        board[pos[0]][pos[1]] = .4
        for move in available_moves(board, pos):
            if move not in processed:
                # marca como tocado
                board[move[0]][move[1]] = .2
                visited.append(move)
                processed.add(move)
                parents[move] = pos

    return None
