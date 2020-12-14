from collections import deque
from tkinter import *


class StatusLabel(Label):
    status_types = {
        'loading': {'text': 'Loading...', 'bg': 'yellow', 'fg': 'black'},
        'ready': {'text': 'Ready!.', 'bg': 'green', 'fg': 'black'},
        'running': {'text': 'Running', 'bg': 'yellow', 'fg': 'black'},
        'pausing': {'text': 'Pausing...', 'bg': 'orange', 'fg': 'black'},
        'testing': {'text': 'Testing...', 'bg': 'cyan', 'fg': 'black'},
        'error': {'text': 'ERROR', 'bg': 'red', 'fg': 'white'},
        'invalid_status': {'text': 'INVALID STATUS', 'bg': 'red', 'fg': 'white'},
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
