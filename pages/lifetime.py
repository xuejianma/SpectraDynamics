import numpy as np
import tkinter as tk
from tkinter import ttk
from utils.task import Task
from utils.plot import Plot
from utils.spinbox import Spinbox
from equipments.oscilloscope import Oscilloscope
import csv


class Lifetime:
    def __init__(self, parent) -> None:
        # var_num.set("10")
        self.oscilloscope = Oscilloscope()
        self.frame = self.set_frame(parent)

    def set_frame(self, parent):
        var_num = tk.StringVar(value=20)
        var_wait_time = tk.StringVar(value=6)
        var_directory = tk.StringVar(value="test")
        frame = ttk.Frame(parent)
        frame_1 = ttk.Frame(frame, padding=10)
        frame_1.pack(side="top")
        frame_2 = ttk.Frame(frame, padding=10)
        frame_2.pack(side="top")
        frame_3 = ttk.Frame(frame, padding=10)
        frame_3.pack(side="top")
        frame_1_1 = ttk.Frame(frame_1, padding=10)
        frame_1_1.pack(side="left")
        frame_1_2 = ttk.Frame(frame_1, padding=10)
        frame_1_2.pack(side="left")
        frame_2_1 = ttk.Frame(frame_2, padding=10)
        frame_2_1.pack(side="left")
        frame_2_2 = ttk.Frame(frame_2, padding=10)
        frame_2_2.pack(side="left")
        frame_3_1 = ttk.Frame(frame_3, padding=10)
        frame_3_1.pack(side="left")
        frame_3_2 = ttk.Frame(frame_3, padding=10)
        frame_3_2.pack(side="left")
        spinbox_num = Spinbox(frame_1_1, from_=0, to=100, textvariable=var_num)
        spinbox_num.pack()
        spinbox_wait_time = Spinbox(frame_1_1, from_=0, textvariable=var_wait_time)
        spinbox_wait_time.pack()
        entry_directory = ttk.Entry(frame_1_1, textvariable=var_directory, width=50)
        entry_directory.pack(side="left")
        button_directory = ttk.Button(frame_1_1, text="Select Saving Directory...", command=lambda: self.select_directory(var_directory))
        button_directory.pack(side="left")
        plot_lifetime_instant_ch1 = Plot(frame_2_1)
        plot_lifetime_average_ch1 = Plot(frame_2_2)
        plot_lifetime_instant_ch2 = Plot(frame_3_1)
        plot_lifetime_average_ch2 = Plot(frame_3_2)
        lifetime_task = LifetimeTask(frame_1_2, self.oscilloscope, var_num, var_wait_time, var_directory, spinbox_num, plot_lifetime_instant_ch1, plot_lifetime_average_ch1, plot_lifetime_instant_ch2, plot_lifetime_average_ch2)
        return frame
    
    def select_directory(self, var_directory):
        directory = tk.filedialog.askdirectory()
        var_directory.set(directory)
        # TODO: set old name when new directory is not valid


class LifetimeTask(Task):
    def __init__(self, parent, oscilloscope, var_num, var_wait_time, var_directory, spinbox_num, plot_lifetime_instant_ch1, plot_lifetime_average_ch1, plot_lifetime_instant_ch2, plot_lifetime_average_ch2):
        super().__init__(parent, var_num)
        self.oscilloscope = oscilloscope
        self.num_spinbox = spinbox_num
        self.var_wait_time = var_wait_time
        self.var_directory = var_directory
        self.X = None
        self.data_ch1 = []
        self.data_ch2 = []
        self.plot_lifetime_instant_ch1 = plot_lifetime_instant_ch1
        self.plot_lifetime_average_ch1 = plot_lifetime_average_ch1
        self.plot_lifetime_instant_ch2 = plot_lifetime_instant_ch2
        self.plot_lifetime_average_ch2 = plot_lifetime_average_ch2
        

    def task(self):
        self.X, curr_data_ch1, curr_data_ch2 = self.oscilloscope.get_data(int(self.var_wait_time.get()), None)
        self.data_ch1.append(curr_data_ch1)
        self.data_ch2.append(curr_data_ch2)
        self.plot_lifetime_instant_ch1.plot(self.X, self.data_ch1[-1], ".-", c="black")
        self.plot_lifetime_average_ch1.plot(self.X, np.mean(self.data_ch1, axis=0), ".-", c="black")
        self.plot_lifetime_instant_ch2.plot(self.X, curr_data_ch2, ".-", c="black")
        self.plot_lifetime_average_ch2.plot(self.X, np.mean(self.data_ch2, axis=0), ".-", c="black")

    def start(self):
        self.data_ch1.clear()
        self.data_ch2.clear()
        self.num_spinbox.config(state="disabled")
        super().start()
        # self.plot.clear()

    def reset(self):
        super().reset()
        with open(self.var_directory.get() + "/test.csv", "w", newline="") as f:
            data_to_save = np.stack((self.X, np.mean(self.data_ch1, axis=0), np.mean(self.data_ch2, axis=0)), axis=1)
            writer = csv.writer(f)
            writer.writerow(["Time(s)", "Ch1(V)", "Ch2(V)"])
            writer.writerows(data_to_save)
        self.num_spinbox.config(state="normal")
