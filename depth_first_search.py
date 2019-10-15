from utils import available_moves


def search(board: list, origin: tuple, target: tuple) -> list:

    def calc_path(parents: dict) -> list:
        """ Retorna o caminho desde a origem até o destino """
        path = [target]
        while path[-1] != origin:
            path.append(parents[path[-1]])
        return path

    visited = [origin]
    parents = {}
    processed = []

    while len(visited) != 0:
        pos = visited.pop(0)
        if pos == target:
            return calc_path(parents)
        for move in available_moves(board, pos):
            # if move not in processed:
            board[move[0]][move[1]] = .2
            visited.insert(0, move)
            parents[move] = pos
        if pos != origin:
            board[pos[0]][pos[1]] = .4
        processed.append(pos)

    return None
