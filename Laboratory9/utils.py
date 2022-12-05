import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


def display_grid(grid, title):
    width = len(grid[0])
    height = len(grid)
    plt.figure(figsize=(height, width))
    plt.xticks(size=14, color='red')
    plt.yticks(size=14, color='red')
    plt.title(title, size=28)
    plt.imshow(grid)
    plt.show()


def display_grids_with_slider(grids):
    grid = grids[0]
    width = len(grid[0])
    height = len(grid)
    plt.rcParams["figure.figsize"] = [width, height]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()
    img = ax.imshow(grid)
    axcolor = 'yellow'
    ax_slider = plt.axes([0.20, 0.01, 0.65, 0.03], facecolor=axcolor)
    slider = Slider(ax_slider, 'Slide->', 0, len(grids) - 1, valinit=0)

    def update(val):
        ax.imshow(grids[int(val)])
        fig.canvas.draw_idle()

    slider.on_changed(update)
    plt.show()
