from tkinter import *


class Graph: # TODO: full re work
    def __init__(self, root, data, bounds="default", width=200, height=100, colour_set=None):
        self.root = root
        self.width = width
        self.height = height
        self.data = data

        if colour_set is None:
            self.color_set = DefaultColourSet(len(self.data))
        else:
            self.color_set = colour_set

        self.can = Canvas(root, width=self.width, height=self.height)
        self.can.pack()

        self.bounds = bounds


class ColourSet:
    def __init__(self, *colour_set):
        self._colour_set = colour_set

    def __getitem__(self, item):
        return self._colour_set[item]

    def __len__(self):
        return len(self._colour_set)


class DefaultColourSet(ColourSet):
    def __init__(self, size):
        super().__init__(*self.generate_color_set(size))

    def generate_color_set(self, size):
        color_set = []
        saturation, light = 1, 0.5
        step = 360 // size
        for hue in range(0, 360, step):
            color_set.append(self.hsl_to_rgb(hue, saturation, light))
        return color_set

    def hsl_to_rgb(self, hue, saturation, light):
        c = (1.0 - self.modulus(2.0 * light - 1.0)) * saturation
        x = c * (1.0 - self.modulus((hue / 60.0) // 2.0 - 1.0))
        m = light - c / 2.0

        inverse_colour = [0, 0, 0]
        if hue < 60.0:
            inverse_colour = [c, x, 0]
        elif hue < 120.0:
            inverse_colour = [x, c, 0]
        elif hue < 180.0:
            inverse_colour = [0, c, x]
        elif hue < 240.0:
            inverse_colour = [0, x, c]
        elif hue < 300.0:
            inverse_colour = [x, 0, c]
        elif hue < 360.0:
            inverse_colour = [c, 0, x]

        colour = "#"
        for i in range(3):
            colour += hex(int(round((inverse_colour[i] + m) * 255, 0)))[2:]

        return colour

    @staticmethod
    def modulus(num):
        if num < 0:
            return -num
        return num
