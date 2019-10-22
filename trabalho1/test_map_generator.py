from gen_boards import gen_board
from view import show_board
from sys import argv

while True:
    board = gen_board(*map(eval, argv[1:]))
    show_board(board)
