import numpy as np


class Network:
    def __init__(self, *structure):
        self.structure = structure
        self.weights = []
        self.biases = []

        for i in range(len(structure) - 1):
            self.weights.append((np.random.rand(structure[i + 1], structure[i]) - 0.5) * 2)
            self.biases.append((np.random.rand(structure[i + 1], 1) - 1) * 2)

    def calculate(self, inputs):
        for weight, bias in zip(self.weights, self.biases):
            inputs = np.matmul(weight, inputs) + bias
            inputs = self.sigmoid(inputs)

        return inputs

    def back_prop(self, inputs, label):
        d_weights, d_biases = self.create_net(self.structure)

        activations = [inputs]

        for weight, bias in zip(self.weights, self.biases):
            inputs = np.matmul(weight, inputs) + bias
            inputs = self.sigmoid(inputs)
            activations.append(inputs)
        outputs = inputs

        d_activation = self.calc_d_cost(outputs, label)

        for i in reversed(range(len(self.structure) - 1)):
            d_sigmoid = self.d_sigmoid(activations[i + 1])

            d_biases[i] += d_activation * d_sigmoid

            d_weights[i] += np.matmul(d_biases[i], np.transpose(activations[i]))

            d_activation = np.matmul(np.transpose(self.weights[i]), d_biases[i])

        return d_weights, d_biases

    @staticmethod
    def calc_d_cost(output, label):
        exp_outputs = np.zeros(shape=output.shape)
        exp_outputs[label, 0] = 1
        return output - exp_outputs

    @staticmethod
    def calc_cost(output, label):
        exp_outputs = np.zeros(shape=output.shape)
        exp_outputs[label, 0] = 1
        return np.sum((output - exp_outputs) ** 2)

    @staticmethod
    def create_net(structure):
        connections = []
        biases = []

        for i in range(len(structure) - 1):
            connections.append(np.zeros(shape=(structure[i + 1], structure[i]), dtype="float32"))
            biases.append(np.zeros(shape=(structure[i + 1], 1), dtype="float32"))

        return connections, biases

    def d_sigmoid(self, z):
        x = self.sigmoid(z)
        return x * (1 - x)

    @staticmethod
    def sigmoid(x):
        return np.divide(1, 1 + np.exp(-x))

    @staticmethod
    def subtract_gradient(a, b):
        d = a
        for i in range(len(b)):
            for j in range(len(b[i])):
                d[i][j] -= b[i][j]
        return d

    @staticmethod
    def add_gradient(a, b):
        d = a
        for i in range(len(b)):
            for j in range(len(b[i])):
                d[i][j] += b[i][j]
        return d

    @staticmethod
    def scale_gradient(a, scalar):
        d = a
        for i in range(len(a)):
            for j in range(len(a[i])):
                d[i][j] *= scalar
        return d

    def __str__(self):
        return "Weights:\n" + self.weights.__str__() + "\nBiases:\n" + self.biases.__str__()
