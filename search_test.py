from utils import get_start_end, weight, str2n
import best_first as bf
import matplotlib.pyplot as plt
from gen_boards import gen_board
from sys import argv
from time import time as t


def test_search(board, search_func):
    se = get_start_end(board)
    board[se[1][0]][se[1][1]] = 0
    t0 = t()
    path = search_func(board, *se)
    dt = t() - t0
    board[se[1][0]][se[1][1]] = str2n['$']

    if path:
        return {'dt': dt,
                'len': len(path),
                'weight': weight(path),
                'path': path}


if __name__ == '__main__':
    while True:
        board = gen_board(int(argv[1]), int(argv[2]))
        search_res = test_search(board, bf.best_first)

        if search_res:
            path = search_res['path']
            for i, j in path[1:-1]:
                board[i][j] = 1

        print(search_res)
        fig = plt.figure(figsize=(7, 7), frameon=False)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        plt.pcolor(board, cmap='inferno')
        plt.show()
