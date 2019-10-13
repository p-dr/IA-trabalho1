from utils import soft_free, count, available_steps, str2n, n2str
from random import random, choice
from math import floor
from sys import argv


def prob(p):
    return lambda x: random() < p


def manhattan_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def blank_board(i, j):
    return [[0] * j for i in range(i)]


def clean_dust(board, thresh=1):
    """ Remove de board valores menores que thresh."""
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] < thresh:
                board[i][j] = 0


def all_free(board, thresh=1e-7):
    return [[i, j] for i in range(len(board))
            for j in range(len(board[0]))
            if soft_free(board, i, j, thresh)]


def random_step(board, pos, orth):
    steps = available_steps(board, pos, orth)
    if steps:
        return choice(steps)


def random_walk(board, start, trail, turn_func,
                end_func, orth, length=None):
    if isinstance(turn_func, float):
        turn_func = prob(turn_func)

    if length:
        end_func = lambda x: x > length

    elif isinstance(end_func, float):
        end_func = prob(end_func)

    pos = start
    # MARQUE START NO TABULEIRO
    step = random_step(board, pos, orth)

    for l in count():
        valid_steps = available_steps(board, pos, orth)
        if not valid_steps:
            break

        # Cria sujeira em volta para não formar traços juntos
        for s in valid_steps:
            board[pos[0] + s[0]][pos[1] + s[1]] = .1

        # Pára se bater em alguma coisa
        if step not in valid_steps:
            break

        pos[0] += step[0]
        pos[1] += step[1]
        board[pos[0]][pos[1]] = trail

        if end_func(l):
            break

        if turn_func(l):
            step = random_step(board, pos, orth)

    return pos


def build_walls(board, nseeds=None, turn_prob=.2, end_prob=.0,
                only_free=False):
    # only_free takes lot of time
    if nseeds is None:
        nseeds = int(len(board) * len(board[0]) / 10)

    for i in range(nseeds):
        seed = seeds_gen(board, 1, only_free=only_free)
        random_walk(board, seed, str2n['-'], turn_prob, end_prob, orth=True)


def seeds_gen(board, nseeds=None, only_free=False):
    # only_free takes lot of time
    seeds = []

    while len(seeds) < nseeds:
        if only_free:
            seed = choice(all_free(board, thresh=1))
        else:
            seed = [floor(random() * len(board)),
                    floor(random() * len(board[0]))]

        if nseeds == 1:
            return seed

        # always True if only_free
        if seed not in seeds:
            seeds.append(seed)

    return seeds


def gen_board(i, j, *args, **kwargs):
    new_board = blank_board(i, j)
    dist_thresh = (len(new_board) + len(new_board[0])) / 2
    start, goal = (0, 0), (0, 0)

    while manhattan_dist(start, goal) < dist_thresh:
        start = seeds_gen(new_board, 1)
        goal = seeds_gen(new_board, 1)

    new_board[start[0]][start[1]] = str2n['$']
    new_board[goal[0]][goal[1]] = str2n['#']

    build_walls(new_board, *args, **kwargs)
    clean_dust(new_board, thresh=min(str2n['#'], str2n['-'], str2n['$']))

    return new_board


def write_board(board, f):
    f.write(f'{len(board)} {len(board[0])}\n')

    for line in board:
        f.write(''.join([n2str[n] for n in line]) + '\n')
    f.write('\n')


def parse_board(board_str):
    """Converte tabuleiro em string para formato numérico."""
    board = []
    # Pula a primeira linha com as dimensões.
    for line in board_str.split('\n')[1:]:
        board.append([str2n[char] for char in line])
    return board


def read_boards(path):
    """Lê arquivo de tabuleiros no formato .boards e retorna lista com
       todos eles em formato numérico."""

    with open(path, 'r') as f:
        content = f.read()

    boards = []
    for board_str in content.split('\n\n')[:-1]:
        boards.append(parse_board(board_str))

    return boards


def main():
    if '-h' in argv:
        print('Generate N boards and save to filename_N_IxJ.boards.')
        print('Usage: python gen_boards.py N filename I J.')
        exit()

    I, J = int(argv[3]), int(argv[4])

    with open(f'{argv[2]}_{argv[1]}_{I}x{J}.boards', 'w') as f:
        for i in range(int(argv[1])):
            write_board(gen_board(I, J), f)

if __name__ == '__main__':
    main()
