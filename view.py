import matplotlib.pyplot as plt
from matplotlib import use


def show_board(board):
    fig = plt.figure(figsize=(7, 7), frameon=False)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    plt.pcolor(board, cmap='inferno')
    use('QT5Agg')
    plt.show()
