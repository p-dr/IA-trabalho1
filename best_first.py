from utils import available_moves, get_start_end, insort


def heuristic(pos, goal):
    a = abs(pos[0] - goal[0])
    b = abs(pos[1] - goal[1])
    d = abs(a-b)
    return 2 ** .5 * min(a, b) + d


def best_first(board, start, goal):
    print('Start/Goal', start, '/', goal)
    queue = [([start], 0)]
    path = [None]

    while path[-1] != goal:
        # print('Q', queue)
        if not queue:
            break
        # -1 ou 0?
        path = queue.pop()[0]
        print('moves', available_moves(board, path[-1]), 'from', path[-1])

        # Append moves
        for move in available_moves(board, path[-1]):
            insort((path + [move], heuristic(move, goal)), queue)
            board[move[0]][move[1]] = .2

    return path


def search(board, search_func):
    path = search_func(board, *get_start_end(board))
    return path
