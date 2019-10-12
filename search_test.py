import best_first as bf
import matplotlib.pyplot as plt
from gen_boards import gen_board
from sys import argv

while True:
    board = gen_board(int(argv[1]), int(argv[2]))
    path = bf.search(board, bf.best_first)
    plt.pcolor(board)
    for i, j in path:
        board[i][j] = 1
    print(path)
    plt.show()


