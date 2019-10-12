import best_first as bf
import matplotlib.pyplot as plt
from gen_boards import gen_board
from sys import argv

while True:
    board = gen_board(int(argv[1]), int(argv[2]))
    try:
        path = bf.search(board, bf.best_first)
    except:
        path = None

    if path:
        for i, j in path[1:-1]:
            board[i][j] = 1

    print(path)
    plt.figure(figsize=(7, 7), frameon=False)
    plt.axis('off')
    plt.pcolor(board, cmap='inferno')
    plt.show()


