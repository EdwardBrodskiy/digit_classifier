import math
from dataclasses import dataclass
from tkinter import *
from tkinter.ttk import *
from typing import Union, List, Iterator, Tuple

from utilities.colors import generate_color_set


@dataclass
class Size:
    width: int = 400
    height: int = 300


@dataclass
class Keys:
    x: str = 't'
    y: str = 'y'
    labels: Union[List[str], None] = None


@dataclass
class Limits:
    y_limit_max: Union[float, None] = None
    y_limit_min: Union[float, None] = None
    y_max: float = 1
    y_min: float = 0

    x_count: int = 0


@dataclass
class GraphConfig:
    size: Size = Size()
    keys: Keys = Keys()
    limits: Limits = Limits()


class Graph(Frame):
    def __init__(self, master=None, cfg: GraphConfig = GraphConfig(), **kwargs):
        super().__init__(master, **kwargs)

        self.cfg = cfg

        self._data = []
        self._lines = []

        self.colors = []

        self.canvas = Canvas(self, width=self.cfg.size.width, height=self.cfg.size.height, background='black', highlightthickness=0)
        self.canvas.pack()

        self.key_frame = Frame(self)
        self.key_frame.pack()
        self._labels = []
        if self.cfg.keys.labels is not None:
            self.colors = generate_color_set(len(self.cfg.keys.labels))
            for i, label in enumerate(self.cfg.keys.labels):
                self._labels.append(Label(self.key_frame, text=label, foreground=self.colors[i]))
                self._labels[-1].pack(side=LEFT)

    def write(self, new_points: List[float]):
        self.cfg.limits.y_max = max(*new_points, self.cfg.limits.y_max)
        if self.cfg.limits.y_limit_max is not None and self.cfg.limits.y_max > self.cfg.limits.y_limit_max:
            self.cfg.limits.y_max = self.cfg.limits.y_limit_max
            new_points = list(map(lambda y: min(y, self.cfg.limits.y_limit_max + 1), new_points))

        self.cfg.limits.y_min = min(*new_points, self.cfg.limits.y_min)
        if self.cfg.limits.y_limit_min is not None and self.cfg.limits.y_min < self.cfg.limits.y_limit_min:
            self.cfg.limits.y_min = self.cfg.limits.y_limit_min
            new_points = list(map(lambda y: max(y, self.cfg.limits.y_limit_min - 1), new_points))

        self._data.append(new_points)
        self._draw_lines()

    def _draw_lines(self):
        if len(self.colors) < len(self._data[-1]):
            self.colors = generate_color_set(len(self._data[0]))
        self._clear_lines()
        step = self._get_step()

        for column, points, next_points in self._get_visible_section():
            x0, x1 = column * step, (column + 1) * step
            col = []
            for line_i, point, next_point in zip(range(len(points)), points, next_points):
                y0, y1 = self._scale_value(point), self._scale_value(next_point)
                col.append(self.canvas.create_line(x0, y0, x1, y1, fill=self.colors[line_i]))
            self._lines.append(col)

    def _clear_lines(self):
        for col in self._lines:
            for line in col:
                self.canvas.delete(line)
        self._lines = []

    def _scale_value(self, val: float) -> float:
        span = self.cfg.limits.y_max - self.cfg.limits.y_min
        if span == 0:
            return (self.cfg.limits.y_max + 1) * self.cfg.size.height
        return (self.cfg.limits.y_max - val) / span * self.cfg.size.height

    def _get_step(self) -> float:
        if len(self._data) <= 1:
            return self.cfg.size.width
        elif self.cfg.limits.x_count == 0:
            return self.cfg.size.width / (len(self._data) - 1)
        else:
            return self.cfg.size.width / min((len(self._data) - 1), self.cfg.limits.x_count - 1)

    def _get_visible_section(self) -> Iterator[Tuple[int, List, List]]:
        if self.cfg.limits.x_count == 0 or len(self._data) <= self.cfg.limits.x_count:
            return zip(range(len(self._data) - 1), self._data[:-1], self._data[1:])
        else:
            return zip(range(self.cfg.limits.x_count), self._data[-self.cfg.limits.x_count:-1], self._data[1 - self.cfg.limits.x_count:])


if __name__ == '__main__':
    double_circle = [r / 720 * math.pi for r in range(0, 721, 1)]
    window = Tk()

    labels = list(map(lambda x: str(x), range(-10, 11)))
    ui = Graph(window, GraphConfig(Size(1200, 700), Keys(labels=labels)), bg='black')
    ui.pack()
    # import time
    # st = time.time()
    # while time.time() - st < 20:
    #     window.update_idletasks()
    #     window.update()
    for r in double_circle:
        ui.write([i * math.sin(r * 20) for i in range(-10, 11)])
        window.update_idletasks()
        window.update()
    window.mainloop()
