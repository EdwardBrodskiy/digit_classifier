from dataclasses import dataclass, is_dataclass
from tkinter import *
from typing import Union


@dataclass
class NetworkSettings:
    network_settings: Widget
    gradient_multiplier: Union[DoubleVar, None] = None
    selection_method: Union[StringVar, None] = None

    def __post_init__(self):
        self.gradient_multiplier = DoubleVar(self.network_settings, 1.1)
        self.selection_method = StringVar(self.network_settings, 'def')


@dataclass
class EmptySettings:
    no_settings_structure_given: Widget


class LabeledWidget(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master)
        self.label = Label(self, **kw)
        self.label.pack(side=LEFT)
        self.widget = None

    def set_widget(self, widget):
        self.widget = widget
        self.widget.pack(side=LEFT)


class SettingsGUI(Frame):
    def __init__(self, master=None, schema=None, **kw):
        super().__init__(master, **kw)

        self.schema = schema if schema is not None else EmptySettings(self)
        self._parse_schema(self, self.schema)

    def change_schema(self, new_schema):
        self.schema = new_schema
        self._parse_schema(self, self.schema)

    def wait_for(self, function, is_not=False):
        value = False
        while value == is_not:
            value = function()
            self.update_idletasks()
            self.update()
        return value

    @staticmethod
    def try_get(get_function):
        try:
            return get_function()
        except TclError:
            return None

    @staticmethod
    def _parse_schema(root, schema):
        attributes = schema.__dict__
        for name, value in attributes.items():
            name = name.replace('_', ' ')
            if is_dataclass(value):
                frame = Frame(root)
                SettingsGUI._parse_schema(frame, value)
                frame.pack(fill='x', pady=10)
            elif isinstance(value, (DoubleVar, StringVar, IntVar)):
                widget = LabeledWidget(root, text=name)
                widget.set_widget(Entry(widget, textvariable=value))
                widget.pack()
            elif isinstance(value, BooleanVar):
                widget = LabeledWidget(root, text=name)
                widget.set_widget(Checkbutton(widget, variable=value))
                widget.pack()
            else:
                widget = Label(root, text=name, bg='light grey')
                widget.pack(fill='x')





