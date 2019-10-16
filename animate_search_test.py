from celluloid import Camera
import depth_first_search as dfs
import breadth_first_search as bfs
import best_first as bf
import a_star as a
from gen_boards import gen_board
from utils import get_start_end, weight, str2n, how_many
from view import figure, plot_board
from sys import argv
from time import time as t


fake_eval = {'dfs': dfs, 'bfs': bfs, 'bf': bf, 'a': a}


def test_search(board, search_func, camera, only_stats=False):
    se = get_start_end(board)
    t0 = t()
    path = search_func(board, *se, camera=camera)
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
    board = gen_board(int(argv[1]), int(argv[2]))

    fig = figure()
    camera = Camera(fig)
    search_res = test_search(board, fake_eval[argv[3]].search,
                             camera=camera)

    path = search_res['path']
    if path:
        for i, j in path[1:-1]:
            board[i][j] = 1

    camera.snap()
    animation = camera.animate()
    animation.save('gifs/dfs.gif', writer='imagemagick')
    print(search_res)


if __name__ == '__main__':
    main()
