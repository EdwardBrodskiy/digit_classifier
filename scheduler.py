import time


class Scheduler:
    def __init__(self):
        self.schedule = {}

    def add_event(self, name, frequency):
        self.schedule[name] = [frequency, time.perf_counter()]

    def check_event(self, name):
        if self.schedule[name][0] <= time.perf_counter() - self.schedule[name][1]:
            self.schedule[name][1] = time.perf_counter()
            return True
        return False
