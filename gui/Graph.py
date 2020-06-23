from tkinter import *
from gui import graphSettings


class Graph:
    def __init__(self, root, data, bounds="default", width=200, height=100, colour_set=None):
        self.root = root
        self.width = width
        self.height = height
        self.data = data

        if colour_set is None:
            self.color_set = graphSettings.DefaultColourSet(len(self.data))
        else:
            self.color_set = colour_set

        self.can = Canvas(root, width=self.width, height=self.height)
        self.can.pack()

        self.bounds = bounds

    def set_up_graph(self):




class RunningGraph(Graph):
    def update
