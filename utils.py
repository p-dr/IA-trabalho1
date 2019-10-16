# Valores iguais ou menores que 1 são considerados 0.
str2n = {'-': 4, '*': 0, '#': 2, '$': 3}
n2str = {v: k for k, v in str2n.items()}

orth_steps = ((1, 0), (0, 1), (-1, 0), (0, -1))
steps = ((-1, 0), (1, 0), (0, -1), (0, 1), (1, 1), (-1, 1), (-1, -1), (1, -1))


def insort(a, l):
    """Insere a na lista l ordenada do maior para o menor."""
    item, label = a
    i = 0
    for i in range(len(l)):
        if label > l[i][1]:
            break
    else:
        i += 1

    l[i:i] = a,


def inside(board, i, j):
    if j >= 0 and j < len(board[0]):
        return i >= 0 and i < len(board)
    return False


def free(board, i, j):
    """Verifica se board[i][j] está livre."""
    return (inside(board, i, j) and (board[i][j] == 0))


def soft_free(board, i, j, thresh=1):
    """Verifica se o valor de board[i][j] é menor que thresh."""
    return (inside(board, i, j) and (board[i][j] < thresh))


def count(n=0):
    """ Conta pra sempre. """
    while True:
        yield n
        n += 1


def available_steps(board, pos, orth=False):
    """Retorna todas os passos possíveis (e.g. [(1, 1), (0, -1)])
    em board a partir de pos. orth=True para só passos ortogonais."""
    i0, j0 = pos
    ret = []

    for di, dj in [steps, orth_steps][orth]:
        j, i = j0 + dj, i0 + di

        if free(board, i, j):
            ret.append((di, dj))

    return ret


def available_moves(board, pos, orth=False):
    """Retorna todas as próximas posições possíveis em board a partir de
    pos."""
    return [(pos[0] + di, pos[1] + dj)
            for di, dj in available_steps(board, pos)]


def get_start_end(board):
    start = None
    end = None

    for i in range(len(board)):
        for j in range(len(board[0])):
            content = board[i][j]

            if (not start) and (content == str2n['#']):
                start = (i, j)
                if end:
                    return (start, end)

            elif (not end) and (content == str2n['$']):
                end = (i, j)
                if start:
                    return (start, end)


def weight(path):
    """ Retorna o peso (distância euclidiana percorrida) de uma lista path de
    posições (i, j)."""
    ret = 0
    for i in range(1, len(path)):
        ret += ((path[i][0] - path[i-1][0]) ** 2 +
                (path[i][1] - path[i-1][1]) ** 2) ** .5
    return ret


def how_many(board, bool_func):
    """ Conta quantos valores em board fazer bool_func retornar True."""
    return sum(sum(map(bool_func, line)) for line in board)
