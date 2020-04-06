import numpy as np
from tkinter import *


class ImageData:
    def __init__(self, root, size, img_data, label, result):
        self.root = root
        self.label = label

        self.previous_result = 0

        self.title = Label(self.root, text=self.format_message(result), background="orange")
        self.title.pack()
        self.img = SquareImage(self.root, img_data, size=size)

        self.img.draw()

    def update_title(self, result):
        if result > self.previous_result:
            color = "red"
        else:
            color = "green"
        self.previous_result = result
        self.title.configure(text=self.format_message(result), background=color)

    def format_message(self, result):
        return str(self.label) + " : " + str(result)


class Image:
    def __init__(self, root, img_data, width=28, height=28, resolution=(28, 28)):
        self.root = root
        self.width = width
        self.height = height
        self.resolution = resolution
        self.pixel_size = self._calculate_pixel_size()
        self.img_data = img_data
        self.can = Canvas(self.root, width=self.width, height=self.height, background="black")
        self.can.pack()

    def draw(self):
        for i in range(self.img_data.shape[0]):
            x = i % self.resolution[0] * self.pixel_size[0]
            y = i // self.resolution[1] * self.pixel_size[1]
            color = self._float_to_hex(self.img_data[i, 0])
            self.can.create_rectangle(x, y, x + self.pixel_size[0], y + self.pixel_size[1], fill=color, outline=color)

    def update(self, img):
        self.img_data = img
        self.can.delete(ALL)
        self.draw()

    def _calculate_pixel_size(self):
        return int(round(self.width / self.resolution[0], 0)), int(round(self.height / self.resolution[1], 0))

    @staticmethod
    def _float_to_hex(num):
        num_h = hex(int(round(num * 255, 0)))[2:]
        if len(num_h) == 1:
            num_h = '0' + num_h
        return '#' + num_h * 3


class SquareImage(Image):
    def __init__(self, root, img_data, size=28, resolution=28):
        super().__init__(root, img_data, width=size, height=size, resolution=(resolution, resolution))
