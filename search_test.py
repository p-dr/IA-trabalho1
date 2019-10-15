from utils import get_start_end, weight, str2n
from view import show_board
import depth_first_search as dfs
import breadth_first_search as bfs
import best_first as bf
import a_star as a
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


def main():
    while True:
        board = gen_board(int(argv[1]), int(argv[2]))
        search_res = test_search(board, bfs.search)

        if search_res:
            path = search_res['path']
            for i, j in path[1:-1]:
                board[i][j] = 1

        print(search_res)
        show_board(board)


if __name__ == '__main__':
    main()
