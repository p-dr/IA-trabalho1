import utils as u
from celluloid import Camera
from view import plot_board
from math import sqrt

sqrt_2 = 1.4

def calc_g(pos1: tuple, pos2: tuple) -> float:
    """ "Peso" para ir da origem até pos2 através de pos1 """
    orthogonal = pos1[0] == pos2[0] or pos1[1] == pos2[1]
    new_g = calc_g.values[pos1] + (1 if orthogonal else sqrt_2)
    return new_g


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
    open_list = {origin: 0}
    closed_list = set()
    parents = {}
    calc_g.values = {origin: 0}
    u.trapezoidal_dist.values = {}
    ###################################

    while open_list:
        pos = min(open_list, key=lambda p: open_list[p])
        del(open_list[pos])
        if pos == target:
            return calc_path(parents)
        if pos != origin:
            # marca como visitado
            board[pos[0]][pos[1]] = .4
        for move in u.available_moves(board, pos):
            if move not in closed_list:
                if move != target:
                    # marca como tocado
                    board[move[0]][move[1]] = .2
                if move in open_list:
                    new_g = calc_g(pos, move)
                    if calc_g.values[move] > new_g:
                        calc_g.values[move] = new_g
                    h = u.trapezoidal_dist.values[move]
                    new_f = new_g + h
                    old_f = open_list[move]
                    if new_f < old_f:
                        open_list[move] = new_f
                        parents[move] = pos
                else:
                    g = calc_g(pos, move)
                    calc_g.values[move] = g
                    h = u.trapezoidal_dist(move, target)
                    f = g + h
                    open_list[move] = f
                    parents[move] = pos
        closed_list.add(pos)

        if camera is not None:
            plot_board(board)
            camera.snap()

    return None
