from typing import Callable

import numpy as np

import utils
from Layer import Layer


class Network:
    layer_sizes: [int]
    learning_rate: float
    nr_of_epochs: int
    layers: [Layer]

    def __init__(self, layer_sizes, learning_rate, nr_of_epochs):
        self.layer_sizes = layer_sizes
        self.learning_rate = learning_rate
        self.nr_of_epochs = nr_of_epochs
        self.layers = []
        for idx, input_size in enumerate(layer_sizes[:-1]):
            # the current layers nr of outputs(nodes) is the next layers number of inputs
            self.layers += [Layer(input_size, layer_sizes[idx + 1])]

    def make_copy(self):
        copy = Network(self.layer_sizes, self.learning_rate, self.nr_of_epochs)
        for idx, layer in enumerate(self.layers):
            layer_in_copy = copy.layers[idx]
            layer_in_copy.weights = np.copy(layer.weights)
            layer_in_copy.biases = np.copy(layer.biases)
        return copy

    def forward_propagation(self, training_set: np.ndarray, target: int,
                            activation_function: Callable[[np.ndarray], np.ndarray]):
        current_layer_input = training_set
        for layer in self.layers:
            activation = layer.compute_activation(current_layer_input, activation_function)
            layer.layer_activation = activation
            current_layer_input = layer.layer_activation
        comparison_target = utils.number_to_number_array(target, self.layers[-1].nr_of_neurons)
        return self.compute_output_layer_total_error(comparison_target)

    def compute_output_layer_total_error(self, target: np.ndarray):
        error = target - self.layers[-1].layer_activation
        error = (error * error) / 2
        return np.sum(error)

    def compute_last_layer_delta(self, target: np.ndarray):
        output_layer = self.layers[-1]
        output_activation = output_layer.layer_activation
        return - (target - output_activation) * output_activation * (1 - output_activation)

    def compute_hidden_layer_delta(self, output_layer_delta: np.ndarray):
        output_layer = self.layers[-1]
        hidden_layer = self.layers[-2]
        hidden_activation = hidden_layer.layer_activation
        return (output_layer_delta @ output_layer.weights.T) * hidden_activation * (1 - hidden_activation)

    def backpropagate(self, training_input: np.ndarray, target: int):
        output_layer = self.layers[-1]
        hidden_layer = self.layers[-2]

        first_layer_input = training_input.reshape(1, -1)
        last_layer_delta = self.compute_last_layer_delta(
            utils.number_to_number_array(target, output_layer.nr_of_neurons))
        output_layer.cost_gradient_w = hidden_layer.layer_activation.T @ last_layer_delta
        output_layer.cost_gradient_b = last_layer_delta

        output_layer.weights -= self.learning_rate * output_layer.cost_gradient_w
        output_layer.biases -= self.learning_rate * output_layer.cost_gradient_b

        hidden_layer_delta = self.compute_hidden_layer_delta(last_layer_delta)
        hidden_layer.cost_gradient_w = first_layer_input.T @ hidden_layer_delta
        hidden_layer.cost_gradient_b = hidden_layer_delta

        hidden_layer.weights -= self.learning_rate * hidden_layer.cost_gradient_w
        hidden_layer.biases -= self.learning_rate * hidden_layer.cost_gradient_b


    def online_training(self, training_data: np.ndarray,
                        activation_function: Callable[[np.ndarray], np.ndarray]):
        for idx in range(len(training_data[0])):
            self.forward_propagation(training_data[0][idx], training_data[1][idx], activation_function)
            self.backpropagate(training_data[0][idx], training_data[1][idx])

    def compute_average_total_error(self, data_set: np.ndarray,
                                    activation_function: Callable[[np.ndarray], np.ndarray]):
        total_set_error = 0
        for idx in range(len(data_set[0])):
            total_set_error += self.forward_propagation(data_set[0][idx], data_set[1][idx], activation_function)
        return total_set_error / len(data_set[0])

    def network_training(self, training_data: np.ndarray,
                         validation_data: np.ndarray,
                         activation_function: Callable[[np.ndarray], np.ndarray]
                         ):
        epochs = {}
        iteration = 1
        while iteration <= self.nr_of_epochs:
            self.online_training(training_data, activation_function)
            current_epoch_network = self.make_copy()
            epochs[iteration] = (
                current_epoch_network, current_epoch_network.compute_average_total_error(validation_data,
                                                                                         activation_function,
                                                                                         ),
                current_epoch_network.test_network_classification(validation_data, activation_function)
            )
            iteration += 1
            utils.shuffle_in_unison(training_data[0], training_data[1])
        return epochs

    def test_network_classification(self, test_data: np.ndarray, activation_function: [[np.ndarray], np.ndarray]):
        accurate = 0
        inaccurate = 0
        wrongfully_classified = []
        matrix = np.zeros((self.layers[-1].nr_of_neurons, self.layers[-1].nr_of_neurons), dtype=int)
        for index in range(len(test_data[0])):
            coordinates = test_data[0][index]
            actual_value = test_data[1][index]
            self.forward_propagation(coordinates, actual_value, activation_function)
            prediction_probabilities = self.layers[-1].layer_activation
            prediction = np.argmax(prediction_probabilities)
            if actual_value == prediction:
                accurate += 1
                matrix[prediction][prediction] += 1
            else:
                inaccurate += 1
                matrix[prediction][actual_value] += 1
                wrongfully_classified.append((coordinates, actual_value))

        return accurate, inaccurate, matrix, wrongfully_classified
