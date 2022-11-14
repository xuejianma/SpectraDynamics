from tkinter import ttk
from utils.config import INSTANCES, VARIABLES
from utils.spinbox import Spinbox
from threading import Thread
from time import sleep

class SweepWavelength:
    def __init__(self, parent) -> None:
        self.set_angle_task = SetAngleTask()
        self.frame, self.button_power = self.set_frame(parent)
        self.read_power_task = ReadPowerTask(self.button_power)

    def set_frame(self, parent):
        frame = ttk.Frame(parent)
        frame_1 = ttk.Frame(frame)
        frame_1.pack(side="top", anchor="w", padx=10, pady=10)
        frame_2 = ttk.Frame(frame)
        frame_2.pack(side="top", padx=10, pady=10)
        frame_1_1 = ttk.Frame(frame_1)
        frame_1_1.pack(side="left")
        frame_1_2 = ttk.Frame(frame_1)
        frame_1_2.pack(side="left")
        frame_1_3 = ttk.Frame(frame_1)
        frame_1_3.pack(side="left")
        label_angle = ttk.Label(frame_1_2, text="Current Angle (deg): ")
        label_angle.pack(side="top", anchor="w")
        entry_angle = ttk.Entry(frame_1_2, state="readonly", textvariable=VARIABLES.var_entry_curr_angle)
        entry_angle.pack(side="top", anchor="w")
        label_set_angle = ttk.Label(frame_1_2, text="Set Angle (deg): ")
        label_set_angle.pack(side="top", anchor="w")
        spinbox_set_angle = Spinbox(frame_1_2, from_=0, to=360, increment=0.1, textvariable=VARIABLES.var_spinbox_set_angle)
        spinbox_set_angle.pack(side="top", anchor="w")
        button_set_angle = ttk.Button(frame_1_2, text="Set Angle", command=self.set_angle_task.start)
        button_set_angle.pack(side="top", anchor="w")
        label_power = ttk.Label(frame_1_3, text="Current Power (mW): ")
        label_power.pack(side="top", anchor="w")
        entry_power = ttk.Entry(frame_1_3, state="readonly", textvariable=VARIABLES.var_entry_curr_power)
        entry_power.pack(side="top", anchor="w")
        button_power = ttk.Button(frame_1_3, text="Turn ON", command=self.toggle_power)
        button_power.pack(side="top", anchor="w")
        return frame, button_power
    def set_angle(self):
        INSTANCES.ndfilter.set_angle(VARIABLES.var_spinbox_set_angle.get())
    def toggle_power(self):
        if self.read_power_task.is_running:
            self.button_power.config(state="disabled")
            self.read_power_task.terminate()
            self.button_power["text"] = "Turn ON"
        else:
            self.read_power_task.start()
            self.button_power["text"] = "Turn OFF"

class SetAngleTask():
    def task_loop(self):
        INSTANCES.ndfilter.set_angle(VARIABLES.var_spinbox_set_angle.get())
        VARIABLES.var_entry_curr_angle.set(INSTANCES.ndfilter.get_angle())
    def start(self):
        thread = Thread(target=self.task_loop)
        thread.start()

class ReadPowerTask():
    def __init__(self, button_power) -> None:
        self.is_running = False
        self.button_power = button_power
    def task_loop(self):
        while self.is_running:
            power_sum = 0
            for _ in range(5):
                power_sum += INSTANCES.powermeter.get_power_uW()
                sleep(0.1)
            VARIABLES.var_entry_curr_power.set(power_sum / 5)
        self.button_power.config(state="normal")
    def start(self):
        self.is_running = True
        thread = Thread(target=self.task_loop)
        thread.start()
    def terminate(self):
        self.is_running = False