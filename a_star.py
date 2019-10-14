from math import sqrt
from utils import available_moves
from heapq import heappop, heappush, heapify

def calc_g(pos1: tuple, pos2: tuple) -> float:
    """ "Peso" para ir da origem até pos2 através de pos1 """
    dist = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    calc_g.values[pos2] =  calc_g.values[pos1] + (1 if dist == 1 else sqrt(2))
    return calc_g.values[pos2]

def calc_h(pos: tuple, target: tuple) -> float:
    """ Distância euclidiana de pos a target """
    #TODO memoization
    dx = target[0] - pos[0]
    dy = target[1] - pos[1]
    return sqrt(dx**2 + dy**2)

def calc_f(pos1: tuple, pos2: tuple, target: tuple) -> float:
    return calc_g(pos1, pos2) + calc_h(pos2, target)

def search(board: list, origin: tuple, target: tuple) -> list:
    """ Executa o algoritmo A* no tabuleiro da origem ao destino """
    def calc_path(parents: dict) -> list:
        """ Retorna o caminho desde a origem até o destino """
        path = [target]
        while path[-1] != origin:
            path.append(parents[path[-1]])
        return path

    ######## inicializações ###########
    open_list = []
    heappush(open_list, [0, origin])
    closed_list = []
    parents = {}
    calc_g.values = {origin: 0}
    ###################################

    while len(open_list) != 0:
        pos = heappop(open_list)[1]
        if pos == target:
            return calc_path(parents)
        closed_list.append(pos)
        children = available_moves(board, pos)
        for c in children:
            if c not in closed_list:
                f = calc_f(pos, c, target)
                try:
                    # i = posição de c em open_list
                    i = [l[1] for l in open_list].index(c)
                    old_f = open_list[i][0]
                    if f < old_f:
                        open_list[i][0] = f
                        heapify(open_list)
                        parents[c] = pos
                except ValueError:
                    # c não está em open_list
                    heappush(open_list, [f, c])
                    parents[c] = pos

    return None
