import tkinter as tk
from tkinter import ttk
from utils.task import Task
from utils.plot import Plot
from time import sleep
import threading

class Lifetime:
    def __init__(self, parent):
        self.parent = parent
        self.frame = self.set_frame()
        self.measure_task = Task(self.frame, num=10)
        self.button = ttk.Button(self.frame, text="Check Threads", command=self.thread_check)
        self.button.pack()
        self.plot_frame = ttk.Frame(self.frame)
        self.plot_frame.pack()
        self.plot = Plot(self.plot_frame)
    def thread_check(self):
        for thread in threading.enumerate():
            print(thread.name)
    def set_frame(self):
        frame = ttk.Frame(self.parent)
        frame.pack()
        return frame

    # def test_task(self, *args):
    #     # self.button.event_generate("<<Hello>>")
    #     run_progress = RunProgress()
    #     run_progress.run()

class MeasureTask(Task):
    def __init__(self, parent):
        super().__init__(parent)

    