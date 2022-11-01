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
