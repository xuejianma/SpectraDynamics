from tkinter import ttk
from utils.task import Task
from utils.plot import Plot
import numpy as np
from time import sleep

class Test:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack()
        self.random_data_generator = RandomDataGenerator(self.frame, num=10)
    def test(self):
        print("Test")

class RandomDataGenerator(Task):
    def __init__(self, parent, num):
        super().__init__(parent, num)
        self.plot = Plot(parent)
        self.data = []

    def task(self):
        sleep(1)
        self.data.append(np.random.random())
        self.plot.plot(self.data, ".-", c="r")

    def reset(self):
        super().reset()
        self.data.clear()