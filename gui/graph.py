import math
from tkinter import *


class Graph(Frame):
    def __init__(self, master=None, width=400, height=300, x_label='x', y_label='y', columns=None):
        super().__init__(master)

        self.width = width
        self.height = height

        self.x_label = x_label
        self.y_label = y_label
        self.columns = columns

        self._data = []
        self._lines = []
        self._max = 1
        self._min = 0
        self.y_limit = 1000

        self.colours = None

        self.canvas = Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill='black')

    def write(self, new_points):
        for i, point in enumerate(new_points):
            if -self.y_limit <= point <= self.y_limit:
                if self._max < point:
                    self._max = point
                elif self._min > point:
                    self._min = point
            else:
                if point > 0:
                    self._max = self.y_limit
                    new_points[i] = self._max + 1
                else:
                    self._min = -self.y_limit
                    new_points[i] = self._min - 1
        self._data.append(new_points)
        self._draw_lines()

    def _draw_lines(self):
        if self.colours is None:
            self.colours = self.generate_color_set(len(self._data[0]))
        for col in self._lines:
            for line in col:
                self.canvas.delete(line)
        self._lines = []
        step = self._get_step()
        for i in range(len(self._data) - 1):
            x0, x1 = i * step, (i + 1) * step
            col = []
            for j in range(len(self._data[i])):
                y0, y1 = self._scale_value(self._data[i][j]), self._scale_value(self._data[i + 1][j])
                col.append(self.canvas.create_line(x0, y0, x1, y1, fill=self.colours[j]))
            self._lines.append(col)

    def _clear_lines(self):
        for col in self._lines:
            for line in col:
                self.canvas.delete(line)
        self._lines = []

    def _scale_value(self, val):
        return (self._max - val) / (self._max - self._min) * self.height

    def _get_step(self):
        if len(self._data) <= 1:
            return self.width
        if self.columns is None:
            return self.width / (len(self._data) - 1)

    def generate_color_set(self, size):
        color_set = []
        saturation, light = 1, 0.5
        step = 360 // size
        for hue in range(0, 360, step):
            color_set.append(self._hsl_to_rgb(hue, saturation, light))
        return color_set

    def _hsl_to_rgb(self, hue, saturation, light):
        c = (1.0 - abs(2.0 * light - 1.0)) * saturation
        x = c * (1.0 - abs(self.fmod(hue / 60, 2) - 1.0))
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
            sub_col = hex(int(round((inverse_colour[i] + m) * 255, 0)))[2:]
            if len(sub_col) == 1:
                sub_col = '0' + sub_col
            colour += sub_col

        return colour

    @staticmethod
    def fmod(a, b):
        while a > b:
            a -= b
        return a


if __name__ == '__main__':
    double_circle = [r / 720 * math.pi for r in range(0, 720, 1)]
    window = Tk()

    ui = Graph(window, 1200, 700)
    ui.pack()

    for r in double_circle:
        ui.write([i * math.exp(r) + 12 * math.sin((i * 3 + r) * 60) for i in range(-10, 11)])
    window.mainloop()
