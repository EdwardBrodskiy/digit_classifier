from tkinter import *
from tkinter.ttk import *

from networks.network import Network


class NetworkInfoUI(Frame):
    def __init__(self, master=None, network_name='', network: Network = None, **kwargs):
        super(NetworkInfoUI, self).__init__(master, **kwargs)
        if network is None:
            Label(self, text='No Network').grid(column=0, row=0)
            return
        self.network = network
        self.name = Label(self, text=network_name.split('.')[0])
        self.structure = Label(self, text=f'Structure: {self.network.get_structure()}')

        self.name.grid(column=0, row=0)
        self.structure.grid(column=0, row=1)

    def update_network(self, name, network):
        self.network = network
        self.name.configure(text=name.split('.')[0])
        self.structure.configure(text=f'Structure: {self.network.get_structure()}')
