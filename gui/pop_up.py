from tkinter import *
from tkinter.ttk import *

from networks import network

file_extension = '\N{cucumber}'


class NewNetwork:
    def __init__(self, root, file_handeler):
        self.top = Toplevel(root)
        self.file_handler = file_handeler

        self.title = Label(self.top, text="Create new Network")

        self.structure_entries = [Entry(self.top, width=4) for _ in range(3)]
        self.structure_entries[0].insert(END, '784')
        self.structure_entries[-1].insert(END, '10')

        self.layer_button = Button(self.top, text="+", command=self.add_layer)

        self.name_label = Label(self.top, text="Enter network name:")
        self.name = Entry(self.top)

        self.enter_button = Button(self.top, text="Enter")

        self.enter_button.bind("<Button-1>", self.enter)
        # .enter_button.bind("<Enter>", self.enter)

        self.map_all()

    def map_all(self):
        self.title.grid(column=0, row=0, columnspan=len(self.structure_entries) + 1)

        for col, e in enumerate(self.structure_entries[:-1]):
            e.grid(row=1, column=col)
        else:
            self.layer_button.grid(column=len(self.structure_entries) - 1, row=1)
            self.structure_entries[-1].grid(column=len(self.structure_entries), row=1)

        self.name_label.grid(column=0, row=2, columnspan=len(self.structure_entries) + 1)

        self.name.grid(column=0, row=3, columnspan=len(self.structure_entries) + 1)

        self.enter_button.grid(column=0, row=4, columnspan=len(self.structure_entries) + 1)

    def add_layer(self):
        self.structure_entries.insert(len(self.structure_entries) - 1, Entry(self.top, width=4))
        self.map_all()

    def enter(self, event):
        if self._is_valid():
            self.file_handler.loaded_object = network.ClassifierTrainer(*list(map(lambda e: int(e.get()), self.structure_entries)))
            self.file_handler.save_as(self.name.get() + file_extension)
            self.top.destroy()

    def _is_valid(self):
        try:
            structure = list(map(lambda e: int(e.get()), self.structure_entries))
            for num in structure:
                if num < 1:
                    return False
        except ValueError:
            return False

        return len(self.name.get()) > 0


class LoadNetwork:
    def __init__(self, root, file_handler):
        self.top = Toplevel(root)
        self.file_handler = file_handler

        Label(self.top, text="Double click to_status select").pack()

        self.options = Listbox(self.top)
        self.options.pack()

        self.file_names = self.file_handler.show_all()
        for file_name in self.file_names:
            self.options.insert(END, file_name.split('.')[0])

        self.options.bind("<Double-Button-1>", self.select)

    def select(self, event):
        index = self.options.curselection()[0]
        self.file_handler.load(self.file_names[index])
        self.top.destroy()


class SaveByName:
    def __init__(self, root, file_handler):
        self.top = Toplevel(root)
        self.file_handler = file_handler

        Label(self.top, text="Enter file name").pack()

        self.entry = Entry(self.top)
        self.entry.pack()
        self.entry.insert(END, self.file_handler.current_file_name.split('.')[0])

        self.enter_button = Button(self.top, text="Enter")
        self.enter_button.pack()
        self.enter_button.bind("<Button-1>", self.enter)

    def enter(self, event):
        self.file_handler.save_as(self.entry.get() + '.' + file_extension)
        self.top.destroy()


