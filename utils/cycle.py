
import threading
from time import sleep

class Cycle(threading.Thread):
    def __init__(self, period: int, task):
        threading.Thread.__init__(self)
        self._thread_name = f"Cycle {period}ms"
        self._instance = task.__self__
        self._task_name = task.__name__
        self._period = period / 1000
        self._start_task = True
        self.start()

    def run(self):
        while self._start_task:
            print("cycle before getattr")
            getattr(self._instance, self._task_name)()
            print("cycle before sleep")
            sleep(self._period)
            print("cycle after sleep")
        print("cycle end")

    def end(self):
        self._start_task = False
