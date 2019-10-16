from matplotlib import use
import matplotlib.pyplot as plt


def show_board(board):
    figure()
    plot_board(board)
    use('QT5Agg')
    plt.show()

def plot_board(board):
    plt.pcolor(board, cmap='inferno')


def figure():
    fig = plt.figure(figsize=(7, 7), frameon=False)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    return fig
