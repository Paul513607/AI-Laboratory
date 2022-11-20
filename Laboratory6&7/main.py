import gzip
import pickle
from pprint import pprint

import matplotlib.colors
import matplotlib.pyplot as plt

import numpy as np

import parse
import utils
from Network import Network

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    all_data = parse.parse_data(r'resources/iris.data')
    train_data, test_data = utils.split_data(all_data, 0.2)
    nr_of_epochs = 50
    network = Network([4, 4, 3], 0.5, nr_of_epochs)
    epochs = network.network_training(train_data, test_data, utils.sigmoid_activation)
    best_epoch = min(epochs.values(), key=lambda x: x[1])
    for idx, epoch in enumerate(epochs.values()):
        print("Epoch ", idx, ":", 'error - ', epoch[1], ', (acc, inacc)')
    epoch_nums = epochs.keys()
    epoch_vals = [epoch[1] for epoch in epochs.values()]
    epoch_vals_2 = [epoch[2][0] / (len(test_data[0])) for epoch in epochs.values()]
    utils.plot_graph(epoch_nums, epoch_vals, epoch_vals_2)

    utils.plot_confusion_matrix(best_epoch)

    best_epoch_index = [i for i in epochs if epochs[i] == best_epoch][0]
    print("Best epoch results on validation set: epoch", best_epoch_index, ' with result ', best_epoch[1])
    # print("Test on training data ",
    #       best_epoch[0].test_network(train_test_set, utils.sigmoid_activation, utils.softmax_activation))
    # print('Test on training data for the last epoch ', epochs[nr_of_epochs][0].test_network(train_test_set, utils.sigmoid_activation, utils.softmax_activation))
    print("Test on test data ",
          best_epoch[0].test_network_classification(test_data, utils.sigmoid_activation))

    utils.plot_points_and_wrongfully_classified_points(test_data, 'sepal length', 'sepal width', best_epoch)
    utils.plot_points_and_wrongfully_classified_points(test_data, 'petal length', 'petal width', best_epoch)
