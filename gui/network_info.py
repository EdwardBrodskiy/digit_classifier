from tkinter import *

from networks.network import Network


class NetworkInfoUI(Frame):
    def __init__(self, master=None, network: Network = None, **kwargs):
        super(NetworkInfoUI, self).__init__(master, **kwargs)
        if network is None:
            Label(self, text='No Network').grid(column=0, row=0)
            return
        self.network = network
        self.structure = Label(self, text=f'Structure: {network.get_structure()}')

        self.structure.grid(column=0, row=0)
