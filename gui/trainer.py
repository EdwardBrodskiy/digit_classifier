from dataclasses import dataclass
from tkinter import *
from tkinter.ttk import *
from typing import List, Optional

from data_managers import DataHandler
from data_managers.file_manager import FileManager
from gui.graph import Graph, GraphConfig, Limits, Keys
from gui.network_info import NetworkInfoUI
from gui.pop_up import LoadNetwork
from gui.settings_gui import SettingsGUI
from gui.status_label import StatusLabel
from networks.network import ClassifierTrainer


@dataclass
class NetworkSettings:
    network: Widget
    gradient_multiplier: Optional[DoubleVar] = None

    def __post_init__(self):
        self.gradient_multiplier = DoubleVar(self.network, 1.0)

    def get_gradient_multiplier(self):
        value = SettingsGUI.try_get(self.gradient_multiplier.get)
        if value is not None and value > 0:
            return value
        return False


@dataclass
class DataHandlerSettings:
    data_handler: Widget
    sub_set_size: Optional[IntVar] = None

    def __post_init__(self):
        self.sub_set_size = IntVar(self.data_handler, 16)

    def get_sub_set_size(self):
        value = SettingsGUI.try_get(self.sub_set_size.get)
        if value is not None and value > 0:
            return value
        return False


@dataclass
class GeneralSettings:
    general_settings: Widget
    number_of_epochs: Optional[IntVar] = None
    test_network_after_epoch: Optional[BooleanVar] = None

    def __post_init__(self):
        self.number_of_epochs = IntVar(self.general_settings, 0)
        self.test_network_after_epoch = BooleanVar(self.general_settings, True)

    def get_number_of_epochs(self):
        value = SettingsGUI.try_get(self.number_of_epochs.get)
        if value is not None:
            return value
        return False


@dataclass
class TrainerSettings:
    settings: Widget
    network: Optional[NetworkSettings] = None
    data_handler: Optional[DataHandlerSettings] = None
    general: Optional[GeneralSettings] = None

    def __post_init__(self):
        self.network = NetworkSettings(self.settings)
        self.data_handler = DataHandlerSettings(self.settings)
        self.general = GeneralSettings(self.settings)


class TrainerGUI(Frame):
    def __init__(self, master=None, file_manager: FileManager = None, **kwargs):
        super().__init__(master, **kwargs)
        self.file_manager = file_manager
        self.file_manager.bind(self.on_new_network)

        # upper
        self.upper_ui = Frame()
        self.upper_ui.pack(anchor='n', fill='x')

        self.status_label = StatusLabel(self.upper_ui)
        self.status_label.pack(side=LEFT, fill='both')

        self.progress_bar = Progressbar(self.upper_ui, maximum=60000, length=600)
        self.progress_bar.pack(side=LEFT, fill='both')

        self.start_button = Button(self.upper_ui, text='Start', command=self.start_training)
        self.start_button.pack(side=RIGHT)

        self.pause_button = Button(self.upper_ui, text='Pause', state='disabled', command=self.pause_training)
        self.pause_button.pack(side=RIGHT)

        self.test_button = Button(self.upper_ui, text='test', command=self.test_network)
        self.test_button.pack(side=RIGHT)

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

        # settings_ui

        self.settings: TrainerSettings = TrainerSettings(self.main_ui)

        self.settings_ui = SettingsGUI(self.main_ui, schema=self.settings)
        self.settings_ui.grid(column=2, row=0, rowspan=2, ipadx=2)

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

    def start_training(self):
        if not self.require_loaded_trainer():
            return
        self.start_button.configure(state='disabled')
        self.pause_button.configure(state='normal')
        self.is_training = True
        self.status_label.push('running')
        while self.is_training:
            number_of_epochs = self.validate_input(self.settings.general.get_number_of_epochs)
            self.settings.general.number_of_epochs.set(number_of_epochs - 1)
            if self.validate_input(self.settings.general.get_number_of_epochs) == 0:
                self.pause_training()
            self.training_data.groups = self.validate_input(self.settings.data_handler.get_sub_set_size)

            for training_set in self.training_data.get_epoch():
                self.progress_bar.step(self.training_data.groups)
                self.update_idletasks()
                self.update()

                gradient = self.file_manager.loaded_object.train(training_set)
                gradient_multiplier = self.validate_input(self.settings.network.get_gradient_multiplier)
                gradient = gradient.__idiv__(self.training_data.groups / gradient_multiplier)
                self.file_manager.loaded_object -= gradient



            if self.settings.general.test_network_after_epoch.get():
                self.test_network()

        # as to get here we need to have paused so pop pausing and running
        self.status_label.pop()
        self.status_label.pop()
        self.start_button.configure(state='normal')

    def pause_training(self):
        self.pause_button.configure(state='disabled')
        self.status_label.push('pausing')
        self.is_training = False

    def test_network(self):
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

    def validate_input(self, get_function, undesired=False):
        value = get_function()
        if value is undesired:
            self.status_label.push('error')
            value = self.settings_ui.wait_for(get_function)
            self.status_label.pop()
        return value
