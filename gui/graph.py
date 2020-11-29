import math
from tkinter import *

c = 0

class Graph(Frame):
    def __init__(self, master=None, width=400, height=300, x_label='x', y_label='y', col=None):
        super().__init__(master)

        self.width = width
        self.height = height

        self.x_label = x_label
        self.y_label = y_label
        self.col = col

        self._data = []
        self._lines = []
        self._max = 1

        self.canvas = Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill='black')

        self.canvas.bind('<Button-1>', lambda _ : self.write([math.sin(c) + 1, math.cos(c) + 1]))

    def write(self, new_points):
        global c
        c += 0.1
        self._data.append(new_points)
        self._max = max(*new_points, self._max)
        print('hi')
        self._draw_lines()

    def _draw_lines(self):
        for col in self._lines:
            for line in col:
                self.canvas.delete(line)
        self._lines = []
        step = self._get_step()
        for i in range(len(self._data) - 1):
            x0, x1 = i * step, (i + 1) * step
            col = []
            for j in range(len(self._data[i])):
                y0, y1 = (self._max - self._data[i][j]) / self._max * self.height, (self._max - self._data[i + 1][j]) / self._max * self.height
                col.append(self.canvas.create_line(x0, y0, x1, y1, fill='white'))
            self._lines.append(col)

    def _get_step(self):
        if len(self._data) <= 1:
            return self.width
        if self.col is None:
            return self.width / (len(self._data) - 1)


if __name__ == '__main__':
    import random

    window = Tk()

    ui = Graph(window, 400, 300)
    ui.pack()


    window.mainloop()
