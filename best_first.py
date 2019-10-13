from utils import available_moves, get_start_end, insort, str2n


def heuristic(pos, goal):
    a = abs(pos[0] - goal[0])
    b = abs(pos[1] - goal[1])
    d = abs(a-b)
    return 2 ** .5 * min(a, b) + d


def best_first(board, start, goal):
    queue = [([start], 0)]
    path = [None]

    while path[-1] != goal:
        if not queue:
            path = None
            break
        # -1 ou 0?
        path = queue.pop()[0]
        curr = path[-1]
        board[curr[0]][curr[1]] = .4

        # Append moves
        for move in available_moves(board, path[-1]):
            insort((path + [move], heuristic(move, goal)), queue)
            board[move[0]][move[1]] = .2

    board[start[0]][start[1]] = str2n['#']
    return path


def search(board, search_func):
    se = get_start_end(board)
    board[se[1][0]][se[1][1]] = 0

    path = search_func(board, *se)

    board[se[1][0]][se[1][1]] = str2n['$']
    return path
