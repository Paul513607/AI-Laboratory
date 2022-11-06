import math
from typing import Callable

import numpy as np


class Layer:
    nr_of_inputs: int
    nr_of_neurons: int
    weights: np.ndarray
    biases: np.ndarray
    layer_activation: np.ndarray
    layer_error: np.ndarray
    layer_friction: np.ndarray
    cost_gradient_w: np.ndarray
    cost_gradient_b: np.ndarray

    def __init__(self, nr_nodes_in: int, nr_nodes_out: int):
        self.layer_error = None
        self.cost_gradient_w = None
        self.cost_gradient_b = None
        self.layer_friction = None
        self.layer_activation = np.zeros((1, 1))
        self.nr_of_inputs = nr_nodes_in
        self.nr_of_neurons = nr_nodes_out
        self.weights = np.random.normal(0, 1 / math.sqrt(nr_nodes_in), size=(self.nr_of_inputs, self.nr_of_neurons))
        self.biases = np.random.rand(1, self.nr_of_neurons)

    def calculate_output(self, training_input: np.ndarray):
        z = (training_input @ self.weights) + self.biases
        return z

    def activation_for_layer(self, output: np.ndarray, activation_function: Callable[[np.ndarray], np.ndarray]):
        activation = []
        for row in output:
            activation += [activation_function(row)]
        self.layer_activation = np.row_stack(activation)
