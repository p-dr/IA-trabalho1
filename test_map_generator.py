from gen_boards import gen_board
from matplotlib.pyplot import pcolor, show
from sys import argv

while True:
    board = gen_board(* map(eval, argv[1:]))
    pcolor(board)
    show()
