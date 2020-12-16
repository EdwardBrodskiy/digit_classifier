from collections import deque
from tkinter.ttk import *


class StatusLabel(Label):
    status_types = {
        'loading': {'text': 'Loading...', 'background': 'yellow', 'foreground': 'black'},
        'ready': {'text': 'Ready!.', 'background': 'green', 'foreground': 'black'},
        'running': {'text': 'Running', 'background': 'yellow', 'foreground': 'black'},
        'pausing': {'text': 'Pausing...', 'background': 'orange', 'foreground': 'black'},
        'testing': {'text': 'Testing...', 'background': 'cyan', 'foreground': 'black'},
        'error': {'text': 'ERROR', 'background': 'red', 'foreground': 'white'},
        'invalid_status': {'text': 'INVALID STATUS', 'background': 'red', 'foreground': 'white'},
    }

    def __init__(self, master=None, default_status='ready'):
        super().__init__(master)
        self.stack = deque()
        self.current_status = default_status

    def pop(self):
        self.current_status = self.stack.pop()
        self._update()

    def push(self, status):
        if status not in self.status_types:
            status = 'invalid_status'
        self.stack.append(self.current_status)
        self.current_status = status
        self._update()

    def _update(self):
        self.configure(**self.status_types[self.current_status])
