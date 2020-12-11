from tkinter import *

import numpy as np

from file_managers import DataHandler
from gui.graph import Graph
from gui.network_info import NetworkInfoUI
from networks.network import ClassifierTrainer


class TrainerGUI(Frame):
    def __init__(self, master=None, network: ClassifierTrainer = None, **kwargs):
        super().__init__(master, **kwargs)
        self.network = network

        # upper
        self.upper_ui = Frame()
        self.upper_ui.pack(side=TOP, anchor='n', fill='x', ipadx=4, padx=2, pady=2)

        self.start_button = Button(self.upper_ui, text='Start', bg='green')
        self.start_button.pack(side=RIGHT)
        self.start_button.bind('<Button-1>', self.start_training)

        self.pause_button = Button(self.upper_ui, text='Pause', bg='orange')
        self.pause_button.pack(side=RIGHT)
        self.pause_button.bind('<Button-1>', self.pause_training)

        # main
        self.main_ui = Frame()
        self.main_ui.pack(fill='both')

        self.net_info = NetworkInfoUI(self.main_ui, self.network)
        self.net_info.grid(column=0, row=0)
        self.g1 = Graph(self.main_ui)
        self.g1.grid(column=1, row=0)
        self.g2 = Graph(self.main_ui)
        self.g2.grid(column=0, row=1)

        loading_label = Label(self.upper_ui, text='Loading...', bg='yellow')
        loading_label.pack(side=LEFT, fill='both')

        self.is_training = False
        self.update_idletasks()
        self.update()
        self.training_data = DataHandler.read_mnist("../training_data/train/train-images.idx3-ubyte",
                                                    "../training_data/train/train-labels.idx1-ubyte",
                                                    amount=0.1)
        self.testing_data = DataHandler.read_mnist("../training_data/test/t10k-images.idx3-ubyte",
                                                   "../training_data/test/t10k-labels.idx1-ubyte",
                                                   amount=0.1)
        self.points = {i: 0 for i in self.training_data}
        loading_label.destroy()

    def start_training(self, event):
        self.is_training = True
        running_label = Label(self.upper_ui, text='Training', bg='green')
        running_label.pack(side=LEFT, fill='both')
        while self.is_training:
            self.update_idletasks()
            self.update()
            training_set, points = DataHandler.take_out_each(self.training_data, 5, self.points)
            gradient = self.network.train(training_set)
            gradient = gradient.__idiv__(50)
            self.network -= gradient
        running_label.destroy()

    def pause_training(self, event):
        self.is_training = False

    def test_network(self, event):
        accuracies = np.zeros(shape=(10, 1))
        for label in self.testing_data:
            for i in self.testing_data[label]:
                if self.network.pick(self.network.calculate(i)) == label:
                    accuracies[label, 0] += 1
            accuracies[label, 0] = accuracies[label, 0] / len(self.testing_data[label])
        accuracies *= 100
        print(np.transpose(accuracies))
        accuracy = accuracies.sum() / 10
        print(accuracy)

        points = {digit: len(self.training_data[digit]) for digit in self.training_data}
