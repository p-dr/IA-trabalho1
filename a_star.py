import utils as u
from celluloid import Camera
from view import plot_board
from math import sqrt
from heapq import heappop, heappush, heapify

sqrt_2 = 1.4

def calc_g(pos1: tuple, pos2: tuple) -> float:
    """ "Peso" para ir da origem até pos2 através de pos1 """
    ortogonal = pos1[0] == pos2[0] or pos1[1] == pos2[1]
    new_g = calc_g.values[pos1] + (1 if ortogonal else sqrt_2)
    if pos2 not in calc_g.values or calc_g.values[pos2] > new_g:
        calc_g.values[pos2] = new_g
    return new_g


def calc_f(pos1: tuple, pos2: tuple, target: tuple) -> float:
    return calc_g(pos1, pos2) + u.trapezoidal_dist(pos2, target)


def search(board: list, origin: tuple,
           target: tuple, camera: Camera = None) -> list:
    """ Executa o algoritmo A* no tabuleiro da origem ao destino """
    def calc_path(parents: dict) -> list:
        """ Retorna o caminho desde destino até a origem """
        path = [target]
        while path[-1] != origin:
            path.append(parents[path[-1]])
        return path

    ######## inicializações ###########
    open_list = []
    heappush(open_list, [0, origin])
    closed_list = set()
    parents = {}
    calc_g.values = {origin: 0}
    u.trapezoidal_dist.values = {}
    ###################################

    while open_list:
        pos = heappop(open_list)[1]
        if pos == target:
            return calc_path(parents)
        if pos != origin:
            # marca como visitado
            board[pos[0]][pos[1]] = .4
        for move in u.available_moves(board, pos):
            if move not in closed_list:
                if move != target:
                    # marca como visitado
                    board[move[0]][move[1]] = .2
                f = calc_f(pos, move, target)
                try:
                    # i = posição de move em open_list
                    i = next(i for (i,p) in enumerate(open_list) if p[1] == move)
                    old_f = open_list[i][0]
                    if f < old_f:
                        open_list[i][0] = f
                        heapify(open_list)
                        parents[move] = pos
                except StopIteration:
                    # move não está em open_list
                    heappush(open_list, [f, move])
                    parents[move] = pos
        closed_list.add(pos)

        if camera is not None:
            plot_board(board)
            camera.snap()

    return None
