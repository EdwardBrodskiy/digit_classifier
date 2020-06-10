import numpy as np
import pickle
import concurrent.futures


class Network:
    def __init__(self, *structure):
        self._structure = structure
        self.weights, self.biases = self._create_net(self._structure)

    def get_structure(self):
        return self._structure

    @staticmethod
    def _create_net(structure):
        weights, biases = [], []

        for i in range(len(structure) - 1):
            weights.append((np.random.rand(structure[i + 1], structure[i]) - 0.5) * 2)
            biases.append((np.random.rand(structure[i + 1], 1) - 1) * 2)

        return weights, biases

    def save(self, name):
        with open(name, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load(name):
        with open(name, 'rb') as file:
            net = pickle.load(file)
        return net

    def __iadd__(self, other):
        for i in range(len(self._structure) - 1):
            self.weights[i] += other.weights[i]
            self.biases[i] += other.biases[i]
        return self

    def __isub__(self, other):
        for i in range(len(self._structure) - 1):
            self.weights[i] -= other.weights[i]
            self.biases[i] -= other.biases[i]
        return self

    def __imul__(self, other):
        for i in range(len(self._structure) - 1):
            self.weights[i] *= other.weights[i]
            self.biases[i] *= other.biases[i]
        return self

    def __idiv__(self, other):
        for i in range(len(self._structure) - 1):
            self.weights[i] /= other
            self.biases[i] /= other
        return self

    def __str__(self):
        return "Weights:\n" + self.weights.__str__() + "\nBiases:\n" + self.biases.__str__()


class Classifier(Network):
    def calculate(self, inputs):
        for weight, bias in zip(self.weights, self.biases):
            inputs = np.matmul(weight, inputs) + bias
            inputs = self._sigmoid(inputs)

        return inputs

    @staticmethod
    def calc_cost(output, label):
        exp_outputs = np.zeros(shape=output.shape)
        exp_outputs[label, 0] = 1
        return np.sum((output - exp_outputs) ** 2)

    @staticmethod
    def pick(arr):
        top = arr.sum()
        num = np.random.rand(1, 1)[0, 0] * top
        for i in range(arr.shape[0]):
            num -= arr[i, 0]
            if num <= 0:
                return i
        return arr.shape[0] - 1

    @staticmethod
    def pick_max(arr):
        max_index = 0
        for i in range(arr.shape[0]):
            if arr[max_index, 0] < arr[i, 0]:
                max_index = i

        return max_index

    @staticmethod
    def _sigmoid(x):
        return np.divide(1, 1 + np.exp(-x))


class ClassifierTrainer(Classifier):

    def train_parallel(self, training_set):
        gradient = Gradient(*self.get_structure())

        for label in training_set:
            with concurrent.futures.ProcessPoolExecutor() as executor:
                results = executor.map(self.back_prop, [(training_set[label], label) for _ in training_set[label]])
                """
                for data in training_set[label]:
                    results.append(executor.submit(self.back_prop, (data, label)))

                for f in concurrent.futures.as_completed(results):
                    gradient += f.result()
                """
                for result in results:
                    gradient += result
        return gradient

    def train(self, training_set):
        gradient = Gradient(*self.get_structure())
        for label in training_set:
            for data in training_set[label]:
                gradient += self.back_prop(data, label)
        return gradient

    def back_prop(self, inputs, label):
        sub_gradient = Gradient(*self.get_structure())

        activations = [inputs]
        # TODO: see if calculate can be re-used
        for weight, bias in zip(self.weights, self.biases):
            inputs = np.matmul(weight, inputs) + bias
            inputs = self._sigmoid(inputs)
            activations.append(inputs)

        outputs = inputs

        d_activation = self._calc_d_cost(outputs, label)

        for i in reversed(range(len(self._structure) - 1)):
            d_sigmoid = self._fake_d_sigmoid(activations[i + 1])

            sub_gradient.biases[i] += d_activation * d_sigmoid

            sub_gradient.weights[i] += np.matmul(sub_gradient.biases[i], np.transpose(activations[i]))

            d_activation = np.matmul(np.transpose(self.weights[i]), sub_gradient.biases[i])

        return sub_gradient

    @staticmethod
    def _calc_d_cost(output, label):
        exp_outputs = np.zeros(shape=output.shape)
        exp_outputs[label, 0] = 1
        return output - exp_outputs

    @staticmethod
    def _fake_d_sigmoid(a):  # It is fake as it takes a value that was already put through sigmoid ie. a instead of z
        # as we put z through the sigmoid during the calculation anyway hence saving us a sigmoid operation!
        return a * (1 - a)


class Gradient(Network):
    @staticmethod
    def _create_net(structure):
        weights, biases = [], []

        for i in range(len(structure) - 1):
            weights.append(np.zeros(shape=(structure[i + 1], structure[i]), dtype="float32"))
            biases.append(np.zeros(shape=(structure[i + 1], 1), dtype="float32"))

        return weights, biases
