from utils import (count, str2n, n2str, orth_steps, steps,
                   inside)
from random import random, choice
from pathlib import Path
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


def free(board, i, j):
    """Verifica se board[i][j] está livre."""
    # Note: goal square is now considered a free square.
    return (inside(board, i, j) and (not board[i][j]))


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


def build_walls(board, nseeds=None, turn_prob=.2, end_prob=.0):
    # only_free takes lot of time
    if nseeds is None:
        nseeds = int(len(board) * len(board[0]) / 10)

    for i in range(nseeds):
        seed = seeds_gen(board, 1)
        random_walk(board, seed, str2n['-'], turn_prob, end_prob, orth=True)


def seeds_gen(board, nseeds=None):
    # only_free takes lot of time
    seeds = []

    while len(seeds) < nseeds:
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

    # Define start and goal squares
    dist_thresh = (len(new_board) + len(new_board[0])) / 2
    start, goal = (0, 0), (0, 0)

    while manhattan_dist(start, goal) < dist_thresh:
        start = seeds_gen(new_board, 1)
        goal = seeds_gen(new_board, 1)

    new_board[start[0]][start[1]] = str2n['$']
    new_board[goal[0]][goal[1]] = str2n['#']

    # Build obstacle walls
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
    """Lê arquivo de tabuleiros no formato .boards, yielding os tabuleiros a
    cada leitura."""

    with open(path, 'r') as f:
        content = f.read()

    for board_str in content.split('\n\n')[:-1]:
        yield parse_board(board_str)


def main():

    if '-h' in argv:
        print('Generate N boards and save to filename_N_IxJ.boards.')
        print('Usage: python gen_boards.py N filename I J.')
        exit()

    out_dir = Path('board_database')
    out_dir.mkdir(exist_ok=True)

    I, J = int(argv[3]), int(argv[4])

    with (out_dir/f'{argv[1]}_{argv[2]}_{I}x{J}.boards').open('w') as f:
        for i in range(int(argv[2])):
            print(f'Writing board {i}/{argv[2]}...', end='\r')
            write_board(gen_board(I, J), f)
    print('Done.' + ' ' * 50)


if __name__ == '__main__':
    main()
