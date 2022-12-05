from Algorithm import QLearning
import utils

if __name__ == '__main__':
    algorithm = QLearning(episodes=50)

    algorithm.train()
    # algorithm.train_sarsa()
    path = algorithm.get_path()
    # path = algorithm.get_path_sarsa()
    print(path)
    algorithm.render_politic()
    utils.display_grids_with_slider(algorithm.episodes_qtable)
