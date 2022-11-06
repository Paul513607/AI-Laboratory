from typing import Callable

import numpy as np

import utils
from Layer import Layer


class Network:
    layer_sizes: list[int]
    learning_rate: float
    nr_of_epochs: int
    layers: list[Layer]

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

    def calculate_outputs(self, training_set: np.ndarray, activation_function: Callable[[np.ndarray], np.ndarray],
                          output_activation_function: Callable[[np.ndarray], np.ndarray]):
        training_input = training_set
        for layer in self.layers[:-1]:
            output = layer.calculate_output(training_input)
            layer.activation_for_layer(output, activation_function)
            training_input = layer.layer_activation
        output_layer = self.layers[-1]
        output = output_layer.calculate_output(training_input)
        output_layer.activation_for_layer(output, output_activation_function)

        return output_layer.layer_activation

    def calculate_last_layer_error(self, output_activation: np.ndarray, expected_labels: np.ndarray):
        t = np.array([utils.number_to_number_array(x, self.layers[-1].nr_of_neurons) for x in expected_labels])
        last_layer_error = output_activation - t
        self.layers[-1].layer_error = last_layer_error
        return last_layer_error

    def backpropagation(self, linearization_factor: float, friction_value: float, total_dataset_size: int, training_set: np.ndarray, expected_labels: np.ndarray,
                        activation_function: Callable,
                        output_activation_function: Callable):
        batch_size = len(training_set)
        output_layer_activation = self.calculate_outputs(training_set, activation_function, output_activation_function)

        for index, layer in reversed(list(enumerate(self.layers))):
            # if the current layer is the output layer
            if index == len(self.layers) - 1:
                layer_error = self.calculate_last_layer_error(output_layer_activation, expected_labels)
                continue
            else:
                next_layer = self.layers[index + 1]
                layer.layer_error = layer.layer_activation * (1 - layer.layer_activation) * \
                                    (next_layer.layer_error @ next_layer.weights.T)
                next_layer.cost_gradient_b = next_layer.layer_error
                next_layer.cost_gradient_w = layer.layer_activation.T @ next_layer.layer_error
                if next_layer.layer_friction is None:
                    next_layer.layer_friction = np.zeros(next_layer.cost_gradient_w.shape)
                next_layer.layer_friction = friction_value * next_layer.layer_friction - (self.learning_rate / batch_size) * next_layer.cost_gradient_w
                next_layer.weights = (1 - self.learning_rate * linearization_factor / total_dataset_size) * next_layer.weights \
                                     + next_layer.layer_friction
                next_layer.biases += np.sum(self.learning_rate * next_layer.cost_gradient_b, axis=0)
        # calculam weight-urile si bias-urile pentru primul strat
        # de aminitit!!! pentru primul strat activation in cadrul calcului de cost_gradient reprezinta inputul primit la inceput
        first_layer = self.layers[0]
        first_layer.cost_gradient_b = first_layer.layer_error
        first_layer.cost_gradient_w = training_set.T @ first_layer.layer_error
        if first_layer.layer_friction is None:
            first_layer.layer_friction = np.zeros(first_layer.cost_gradient_w.shape)
        first_layer.layer_friction = friction_value * first_layer.layer_friction - (
                    self.learning_rate / batch_size) * first_layer.cost_gradient_w
        first_layer.weights = (1 - self.learning_rate * linearization_factor / total_dataset_size) * first_layer.weights \
                             + first_layer.layer_friction
        first_layer.biases += np.sum((-self.learning_rate) * first_layer.cost_gradient_b, axis=0)

    def training_phase(self, batch_size: int, training_data: np.ndarray,
                       validation_data: np.ndarray,
                       activation_function: Callable,
                       output_activation_function: Callable,
                       linearization_factor: float,
                       friction_value: float):
        epochs = {}
        iteration = 1
        while iteration <= self.nr_of_epochs:
            batch_start = 0
            while True:
                nr_of_rows = min(batch_size, len(training_data[0]) - batch_start)
                training_set = training_data[0][batch_start:batch_start + nr_of_rows]
                expected_labels = training_data[1][batch_start:batch_start + nr_of_rows]
                batch_start += nr_of_rows
                self.backpropagation(linearization_factor, friction_value, len(training_set[0]), training_set, expected_labels, activation_function,
                                     output_activation_function)
                if batch_start >= len(training_set[0]):
                    break
            current_epoch_network = self.make_copy()
            epochs[iteration] = (current_epoch_network, current_epoch_network.test_network(validation_data,
                                                                                           activation_function,
                                                                                           output_activation_function),
                                 )
            iteration += 1
        return epochs

    def test_network(self, test_data: np.ndarray, activation_function: Callable, output_activation_function: Callable):
        accurate = 0
        inaccurate = 0
        for index in range(len(test_data[0])):
            coordinates = test_data[0][index]
            actual_value = test_data[1][index]
            prediction_probabilities = self.calculate_outputs(coordinates, activation_function,
                                                              output_activation_function)
            prediction = np.argmax(prediction_probabilities)
            if actual_value == prediction:
                accurate += 1
            else:
                inaccurate += 1
        return accurate, inaccurate
