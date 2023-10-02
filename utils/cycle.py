import threading
from time import sleep


class Cycle(threading.Thread):
    def __init__(self, period: int, task):
        threading.Thread.__init__(self, name=f"Cycle {period}ms", daemon=True)
        self._instance = task.__self__
        self._task_name = task.__name__
        self._period = period / 1000
        self._task = getattr(self._instance, self._task_name)
        self.start()

    def run(self):
        while True:
            self._task()
            sleep(self._period)

