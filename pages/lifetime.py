import numpy as np
import tkinter as tk
from tkinter import ttk
from utils.task import Task
from utils.plot import Plot
from utils.spinbox import Spinbox
from utils.save import Save
from utils.config import VARIABLES, INSTANCES


class Lifetime:
    def __init__(self, parent) -> None:
        self.oscilloscope = INSTANCES.oscilloscope
        self.frame = self.set_frame(parent)

    def set_frame(self, parent):
        frame = ttk.Frame(parent)
        frame_1 = ttk.Frame(frame)
        frame_1.pack(side="top", anchor="w", padx=10, pady=10)
        frame_2 = ttk.Frame(frame)
        frame_2.pack(side="top", padx=10, pady=10)
        frame_3 = ttk.Frame(frame)
        frame_3.pack(side="top", padx=10, pady=10)
        frame_1_1 = ttk.Frame(frame_1)
        frame_1_1.pack(side="left", padx=100)
        frame_1_2 = ttk.Frame(frame_1)
        frame_1_2.pack(side="left", padx=(100, 50))
        frame_2_1 = ttk.Frame(frame_2)
        frame_2_1.pack(side="left", padx=10)
        frame_2_2 = ttk.Frame(frame_2)
        frame_2_2.pack(side="left", padx=10)
        frame_3_1 = ttk.Frame(frame_3)
        frame_3_1.pack(side="left", padx=10)
        frame_3_2 = ttk.Frame(frame_3)
        frame_3_2.pack(side="left", padx=10)
        frame_1_1_1 = ttk.Frame(frame_1_1)
        frame_1_1_1.pack(side="top", anchor="w")
        ttk.Label(frame_1_1_1, text="Number of measurements: ").grid(row=0, column=0, pady=4)
        self.spinbox_num = Spinbox(frame_1_1_1, from_=1, to=float("inf"), textvariable=VARIABLES.var_spinbox_lifetime_num)
        self.spinbox_num.grid(row=0, column=1)
        ttk.Label(frame_1_1_1, text="Wait time (s): ").grid(row=1, column=0, sticky="w", pady=4)
        Spinbox(frame_1_1_1, from_=0, to=float("inf"), textvariable=VARIABLES.var_spinbox_lifetime_wait_time).grid(row=1, column=1)
        self.plot_lifetime_instant_ch1 = Plot(frame_2_1)
        self.plot_lifetime_average_ch1 = Plot(frame_2_2)
        self.plot_lifetime_instant_ch2 = Plot(frame_3_1)
        self.plot_lifetime_average_ch2 = Plot(frame_3_2)
        self.save = Save(frame_1_1, VARIABLES.var_entry_lifetime_directory, VARIABLES.var_entry_lifetime_filename)
        LifetimeTask(frame_1_2, self)

        return frame


class LifetimeTask(Task):
    def __init__(self, parent, page: Lifetime) -> None:
        super().__init__(parent)
        self.page = page
        self.oscilloscope = INSTANCES.oscilloscope
        # self.spinbox_num = spinbox_num
        self.X = None
        # self.save = save
        self.page.save.data_dict["header"] = ["Time(s)", "Ch1(V)", "Ch2(V)"]
        self.data_ch1 = None
        self.data_ch2 = None
        # self.plot_lifetime_instant_ch1 = plot_lifetime_instant_ch1
        # self.plot_lifetime_average_ch1 = plot_lifetime_average_ch1
        # self.plot_lifetime_instant_ch2 = plot_lifetime_instant_ch2
        # self.plot_lifetime_average_ch2 = plot_lifetime_average_ch2

    def task(self):
        self.X, curr_data_ch1, curr_data_ch2 = self.oscilloscope.get_data(
            int(VARIABLES.var_spinbox_lifetime_wait_time.get()))
        self.data_ch1 = np.asarray(self.data_ch1) * (self.i / (self.i + 1)) + np.asarray(
            curr_data_ch1) * (1 / (self.i + 1)) if self.i > 0 else curr_data_ch1
        self.data_ch2 = np.asarray(self.data_ch2) * (self.i / (self.i + 1)) + np.asarray(
            curr_data_ch2) * (1 / (self.i + 1)) if self.i > 0 else curr_data_ch2
        self.save_data()
        self.page.plot_lifetime_instant_ch1.plot(
            self.X, curr_data_ch1, "-", c="black", linewidth=0.5)
        self.page.plot_lifetime_average_ch1.plot(
            self.X, self.data_ch1, "-", c="black", linewidth=0.5)
        self.page.plot_lifetime_instant_ch2.plot(
            self.X, curr_data_ch2, "-", c="black", linewidth=0.5)
        self.page.plot_lifetime_average_ch2.plot(
            self.X, self.data_ch2, "-", c="black", linewidth=0.5)

    def start(self):
        self.num = int(float(VARIABLES.var_spinbox_lifetime_num.get()))
        self.page.spinbox_num.config(state="disabled")
        self.page.save.update_datetime()
        super().start()

    def reset(self):
        super().reset()
        self.page.spinbox_num.config(state="normal")

    def save_data(self):
        data_to_save = np.stack((self.X, self.data_ch1, self.data_ch2), axis=1)
        self.page.save.data_dict["data"] = data_to_save
        self.page.save.save(update_datetime=False)