from Algorithm import QLearning
import utils

if __name__ == '__main__':
    algorithm = QLearning(episodes=50)

    algorithm.train()
    path = algorithm.get_path()
    print(path)
    algorithm.render_politic()
    utils.display_grids_with_slider(algorithm.episodes_qtable)
