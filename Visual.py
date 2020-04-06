import numpy as np
from tkinter import *
import data_renderer


class Visual:

    def __init__(self, root):

        self.image = Frame(root)
        self.ui = Frame(root)
        self.image.grid(row=0, column=0)
        self.ui.grid(row=0, column=1)

        self.size = 700

        self.img_data_out = []

    def show_data(self, data):
        num_of_imgs = sum(len(data[i]) for i in data)
        side = self.next_largest_sq_side(num_of_imgs)
        scale_of_pixel = self.size / side / 28
        index = 0
        for label in data:
            for digit in data[label]:
                self.img_data_out.append(data_renderer.ImageData(Frame(self.image), scale_of_pixel, digit, label, "none"))
                self.img_data_out[-1].root.grid(row=index // side, column=index % side)
                index += 1

    def update_results_on_data(self, results):
        for i, result in enumerate(results):
            self.img_data_out[i].update_title(result)

    @staticmethod
    def next_largest_sq_side(num):
        x = 1
        while x ** 2 < num:
            x += 1
        return x
