import math

import numpy as np


class Layer:
    nr_of_inputs: int
    nr_of_neurons: int
    weights: np.ndarray
    biases: np.ndarray

    def __init__(self, nr_nodes_in: int, nr_nodes_out: int):
        self.nr_of_inputs = nr_nodes_in
        self.nr_of_neurons = nr_nodes_out
        self.weights = np.random.normal(0, 1 / math.sqrt(nr_nodes_in), size=(self.nr_of_inputs, self.nr_of_neurons))
        self.biases = np.random.rand(1, self.nr_of_neurons)
