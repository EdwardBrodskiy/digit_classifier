from tkinter import *
import numpy as np
import network
import data_renderer
import DataAnalyser


class RunGUI:
    def __init__(self, root, classifier, width=400, height=400, title="Unnamed"):
        self.root = root
        self.top = Toplevel(self.root)
        self.top.title(title)
        self.classifier = classifier

        self.edges = []
        self.distance = 2
        self.distance_sq = self.distance ** 2
        self.stroke = 10

        self.width, self.height = width, height

        self.ai_vision_frame = Frame(self.top)
        self.ai_vision_frame.pack(side="right")

        self.canvas = Canvas(self.top, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        self.result = Label(self.top, text="")
        self.result.pack()

        self.image = data_renderer.Image(self.ai_vision_frame, np.zeros(shape=(784, 1)), width=100, height=100)

        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.re_calculate)

        self.canvas.bind("<Button-3>", self.clear_all)

    def start_draw(self, event):
        self.edges.append([])

    def draw(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        if self.sufficiently_far(x, y):
            self.draw_circle(x, y, self.stroke)
            self.edges[-1].append((x, y))

    def draw_circle(self, x, y, r):
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="white", width=0)

    def sufficiently_far(self, x, y):
        if self.edges[-1]:
            dx = x - self.edges[-1][-1][0]
            dy = y - self.edges[-1][-1][1]
            return dx ** 2 + dy ** 2 > self.distance_sq
        else:
            return True

    def clear_all(self, event):
        self.canvas.delete(ALL)
        self.edges = []

    def re_calculate(self, event):
        combined_edges = []
        for edge in self.edges:
            combined_edges += edge
        if combined_edges:
            image = self.format_data_to_mnist(combined_edges)

            self.image.update(image)

            result = self.classifier.calculate(image)

            for i in range(10):
                print(i, ":", round(result[i, 0] * 100, 1), end=", ")
            print("")

            choice = self.classifier.pick_max(result)
            certainty = round(result[choice, 0] * 100, 1)
            self.result.config(text="I am " + str(certainty) + "% certain that it is a " + str(choice))

    def format_data_to_mnist(self, combined_edges):
        image = np.zeros(shape=(784, 1), dtype="float32")

        offset = self.get_offset_for_mnist(combined_edges)
        for i, point in enumerate(combined_edges):
            combined_edges[i] = (point[0] + offset[0], point[1] + offset[1])

        scalar = self.get_scalar_for_mnist(combined_edges)
        center = (self.width / 2, self.height / 2)
        for i, point in enumerate(combined_edges):
            combined_edges[i] = ((point[0] - center[0]) * scalar[0] + center[0], (point[1] - center[1]) * scalar[1] + center[1])

        for point in combined_edges:
            x, y = self.re_map(point)

            image = self.add_blob(image, x, y, fall=0.6)

        for i in range(784):
            if image[i, 0] > 1:
                image[i, 0] = 1
            if image[i, 0] < 0:
                image[i, 0] = 0

        print(DataAnalyser.get_size_range({0: [image]}))
        return image

    def re_map(self, point):
        return int(round(point[0] * 28 / self.width - 1, 0)), int(round(point[1] * 28 / self.height - 1, 0))

    @staticmethod
    def add_blob(image, x, y, start=.9, fall=0.4):
        radius = int(start // fall)
        for i in range(-radius, radius):
            for j in range(-radius, radius):
                image[(x + i) + (y + j) * 28] += start - (i ** 2 + j ** 2) ** 0.5 * fall
        return image

    def get_offset_for_mnist(self, points):

        max_x = max(points, key=lambda c: c[0])[0]
        max_y = max(points, key=lambda c: c[1])[1]
        min_x = min(points, key=lambda c: c[0])[0]
        min_y = min(points, key=lambda c: c[1])[1]

        offset_x = ((self.width - max_x) - min_x) / 2
        offset_y = ((self.height - max_y) - min_y) / 2

        return offset_x, offset_y

    def get_scalar_for_mnist(self, points):

        min_y = min(points, key=lambda c: c[1])[1]
        min_x = min(points, key=lambda c: c[0])[0]

        target_min_x = (28 - 14.787200707261428) / 2 / 28 * self.width
        target_min_y = (28 - 18.72819776796893) / 2 / 28 * self.height

        center = [self.width / 2, self.height / 2]

        if center[0] - min_x < self.width / 10:
            scl_x = 1
        else:
            scl_x = (center[0] - target_min_x) / (center[0] - min_x)

        scl_y = (center[1] - target_min_y) / (center[1] - min_y)
        return [scl_x, scl_y]
