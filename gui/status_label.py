from tkinter import *


class StatusLabel(Label):
    status_types = {
        'loading': {'text': 'Loading...', 'bg': 'yellow', 'fg': 'black'},
        'ready': {'text': 'Ready!.', 'bg': 'green', 'fg': 'black'},
        'running': {'text': 'Running', 'bg': 'yellow', 'fg': 'black'},
        'pausing': {'text': 'Pausing...', 'bg': 'orange', 'fg': 'black'},
        'testing': {'text': 'Testing...', 'bg': 'cyan', 'fg': 'black'},
        'error': {'text': 'ERROR', 'bg': 'red', 'fg': 'white'},
    }

    def __init__(self, master=None, status='loading'):
        super().__init__(master)

    def change_status(self, status):
        if status not in self.status_types:
            status = 'error'
        self.configure(**self.status_types[status])
