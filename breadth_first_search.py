from utils import available_moves, get_start_end, insort, str2n
from matplotlib import use
import matplotlib.pyplot as plt

def search(board: list, origin: tuple, target: tuple) -> list:

    def calc_path(parents: dict) -> list:
        """ Retorna o caminho desde a origem até o destino """
        path = [target]
        while path[-1] != origin:
            path.append(parents[path[-1]])
        return path
    
    visited = []
    visited.append(origin)
    parents = {}
    processed = []

    while len(visited) != 0:
        pos = visited.pop(0)
        if pos == target:
            return calc_path(parents)
        for move in available_moves(board, pos):
            if move not in processed:
                board[move[0]][move[1]] = .2
                visited.append(move)            
                parents[move] = pos
        if pos != origin:
            board[pos[0]][pos[1]] = .4
        processed.append(pos)
        fig = plt.figure(figsize=(7, 7), frameon=False)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        plt.pcolor(board, cmap='inferno')
        use('QT5Agg')
        plt.show()

    return None