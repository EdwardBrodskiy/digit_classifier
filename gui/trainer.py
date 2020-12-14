from data_managers import DataHandler
from data_managers.file_manager import FileManager
from gui.graph import *
from gui.network_info import NetworkInfoUI
from gui.pop_up import LoadNetwork
from gui.status_label import StatusLabel
from networks.network import ClassifierTrainer


class TrainerGUI(Frame):
    def __init__(self, master=None, file_manager: FileManager = None, **kwargs):
        super().__init__(master, **kwargs)
        self.file_manager = file_manager
        self.file_manager.bind(self.on_new_network)

        # upper
        self.upper_ui = Frame()
        self.upper_ui.pack(anchor='n', fill='x', ipadx=4, padx=2, pady=2)

        self.status_label = StatusLabel(self.upper_ui)
        self.status_label.pack(side=LEFT, fill='both')

        self.start_button = Button(self.upper_ui, text='Start', bg='green')
        self.start_button.pack(side=RIGHT)
        self.start_button.bind('<Button-1>', self.start_training)

        self.pause_button = Button(self.upper_ui, text='Pause', bg='orange')
        self.pause_button.pack(side=RIGHT)
        self.pause_button.bind('<Button-1>', self.pause_training)

        self.test_button = Button(self.upper_ui, text='test', bg='cyan')
        self.test_button.pack(side=RIGHT)
        self.test_button.bind('<Button-1>', self.test_network)

        # main
        self.main_ui = Frame()
        self.main_ui.pack(fill='both')

        self.require_loaded_trainer()
        self.net_info = NetworkInfoUI(self.main_ui, self.file_manager.current_file_name[:-4], self.file_manager.loaded_object)
        self.net_info.grid(column=0, row=0)
        self.graph_all_digits = Graph(self.main_ui, GraphConfig(limits=Limits(x_count=100), keys=Keys(labels=list(range(10)))))
        self.graph_all_digits.grid(column=1, row=0)
        self.graph_average = Graph(self.main_ui)
        self.graph_average.grid(column=0, row=1)

        self.status_label.push('loading')

        self.is_training = False
        self.update_idletasks()
        self.update()
        self.training_data = DataHandler.DataHandler("../training_data/train/train-labels.idx1-ubyte",
                                                     "../training_data/train/train-images.idx3-ubyte",
                                                     )
        self.testing_data = DataHandler.DataHandler("../training_data/test/t10k-labels.idx1-ubyte",
                                                    "../training_data/test/t10k-images.idx3-ubyte",
                                                    )
        self.status_label.pop()

    def on_new_network(self):
        self.net_info.update_network(self.file_manager.current_file_name[:-4], self.file_manager.loaded_object)

    def require_loaded_trainer(self):
        if type(self.file_manager.loaded_object) is ClassifierTrainer:
            return True
        else:
            self.status_label.push('error')
            LoadNetwork(self, self.file_manager)
            self.status_label.pop()
            return False

    def start_training(self, event):
        if not self.require_loaded_trainer():
            return
        self.is_training = True
        self.status_label.push('running')
        while self.is_training:
            for training_set in self.training_data.get_epoch():
                self.update_idletasks()
                self.update()
                gradient = self.file_manager.loaded_object.train(training_set)
                gradient = gradient.__idiv__(self.training_data.groups)
                self.file_manager.loaded_object -= gradient
            self.test_network(None)
        # as to get here we need to have paused so pop pausing and running
        self.status_label.pop()
        self.status_label.pop()

    def pause_training(self, event):
        self.status_label.push('pausing')
        self.is_training = False

    def test_network(self, event):
        if not self.require_loaded_trainer():
            return
        self.status_label.push('testing')
        accuracies: List[float] = [0 for _ in range(10)]
        for label, value in self.testing_data.get_all_data():
            self.update_idletasks()
            self.update()
            if self.file_manager.loaded_object.pick(self.file_manager.loaded_object.calculate(value)) == label:
                accuracies[label] += 1
        for label in self.testing_data.data:
            accuracies[label] = accuracies[label] / len(self.testing_data.data[label])
        self.graph_all_digits.write(accuracies)
        self.graph_average.write([sum(accuracies) / len(accuracies)])
        self.status_label.pop()
