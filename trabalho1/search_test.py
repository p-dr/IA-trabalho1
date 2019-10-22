from gen_boards import gen_board
from utils import get_start_end, weight, str2n, how_many, search_algs
from view import show_board
from sys import argv
from time import process_time as t


fake_eval = {k: v for k, v in zip(('dfs', 'bfs', 'bf', 'a'),
                                  search_algs)}


def test_search(board, search_func, only_stats=False):
    se = get_start_end(board)
    t0 = t()
    path = search_func(board, *se)
    dt = t() - t0
    board[se[0][0]][se[0][1]] = str2n['#']
    board[se[1][0]][se[1][1]] = str2n['$']

    ret = {'dt': dt,
           'touched': how_many(board, lambda x: x in (.2, .4, 1)),
           'visited': how_many(board, lambda x: x in (.4, 1)),
           'len': None, 'weight': None, 'path': None}

    if path:
        ret.update(len=len(path), weight=weight(path))
        if not only_stats:
            ret.update(path=path)

    return ret


def main():
    while True:
        board = gen_board(int(argv[1]), int(argv[2]))
        search_res = test_search(board, fake_eval[argv[3]].search)

        path = search_res['path']
        if path:
            for i, j in path[1:-1]:
                board[i][j] = 1

        print(search_res)
        show_board(board)


if __name__ == '__main__':
    main()
