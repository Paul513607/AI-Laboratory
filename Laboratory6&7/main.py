import gzip
import pickle

import numpy as np

import parse
import utils
from Network import Network

with gzip.open(r'retele_neuronale/mnist.pkl.gz', 'rb') as fd:
    train_set_rn, valid_set_rn, test_set_rn = pickle.load(fd, encoding='latin')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # all_data = parse.parse_data(r'resources/iris.data')
    # train_data, test_data = utils.split_data(all_data, 0.2)
    train_test_set = train_set_rn[0][:10000], train_set_rn[1][:10000]
    nr_of_epochs = 200
    network = Network([784, 100, 10], 0.005, nr_of_epochs)
    epochs = network.training_phase(32, train_set_rn, valid_set_rn, utils.sigmoid_activation, utils.softmax_activation,
                                    5, 0.9)
    best_epoch = max(epochs.values(), key=lambda x: x[1][0])
    for idx, epoch in enumerate(epochs.values()):
        print("Epoch ", idx, ":", epoch[1])
    best_epoch_index = [i for i in epochs if epochs[i] == best_epoch][0]
    print("Best epoch results on validation set: epoch", best_epoch_index, ' with result ', best_epoch[1])
    print("Test on training data ",
          best_epoch[0].test_network(train_test_set, utils.sigmoid_activation, utils.softmax_activation))
    print('Test on training data for the last epoch ', epochs[nr_of_epochs][0].test_network(train_test_set, utils.sigmoid_activation, utils.softmax_activation))
    print("Test on test data ",
          best_epoch[0].test_network(test_set_rn, utils.sigmoid_activation, utils.softmax_activation))

