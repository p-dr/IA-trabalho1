from matplotlib import use
import matplotlib.pyplot as plt


def show_board(board, fig=None, show=True):
    if fig is None:
        fig = plt.figure(figsize=(7, 7), frameon=False)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')

    plt.pcolor(board, cmap='inferno')
    use('QT5Agg')

    if show:
        plt.show()

    return fig
