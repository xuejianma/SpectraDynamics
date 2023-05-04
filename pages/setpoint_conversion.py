from time import sleep
import tkinter as tk
from tkinter import StringVar, ttk
from utils.spinbox import Spinbox
from utils.config import INSTANCES, LOGGER, VARIABLES, GLOBALS
from utils.save import Save
from utils.task import PAUSED, Task


class SetpointConversion:
    def __init__(self, parent) -> None:
        self.frame = self.set_frame(parent)

    def set_frame(self, parent) -> None:
        frame = ttk.Frame(parent)
        frame.pack()
        frame_1 = ttk.Frame(frame)
        frame_1.pack(side="top", anchor="w", padx=10, pady=10)
        frame_2 = ttk.Frame(frame)
        frame_2.pack(side="top", anchor="w", padx=10, pady=10)
        frame_1_1 = ttk.Frame(frame_1)
        frame_1_1.pack(side="left", anchor="w", padx=10, pady=10)
        frame_1_2 = ttk.Frame(frame_1)
        frame_1_2.pack(side="left", anchor="w", padx=10, pady=10)
        frame_1_3 = ttk.Frame(frame_1)
        frame_1_3.pack(side="left", anchor="w", padx=10, pady=10)
        ttk.Label(frame_1_1, text="Start Current Setpoint (mA): ").pack(side="top", anchor="w", padx=10)
        ttk.Label(frame_1_1, text="Recommended Safe Range: 0 - 40mA", font="TkDefaultFont 8").pack(side="top", anchor="w", padx=10)
        self.spinbox_start_setpoint = Spinbox(frame_1_1, from_=0, to=float('inf'), textvariable=VARIABLES.var_spinbox_setpoint_conversion_start_setpoint)
        self.spinbox_start_setpoint.pack(side="top", anchor="w", padx=10)
        ttk.Label(frame_1_1, text="End Current Setpoint (mA): ").pack(side="top", anchor="w", padx=10)
        ttk.Label(frame_1_1, text="Recommended Safe Range: 0 - 40mA", font="TkDefaultFont 8").pack(side="top", anchor="w", padx=10)
        self.spinbox_end_setpoint = Spinbox(frame_1_1, from_=0, to=float('inf'), textvariable=VARIABLES.var_spinbox_setpoint_conversion_end_setpoint)
        self.spinbox_end_setpoint.pack(side="top", anchor="w", padx=10)
        ttk.Label(frame_1_1, text="Step Size (mA): ").pack(side="top", anchor="w", padx=10)
        self.spinbox_step_setpoint = Spinbox(frame_1_1, from_=0, to=float('inf'), textvariable=VARIABLES.var_spinbox_setpoint_conversion_step_setpoint)
        self.spinbox_step_setpoint.pack(side="top", anchor="w", padx=10)
        ttk.Label(frame_1_2, text="Background Power (uW):").pack(side="top", anchor="w")
        self.spinbox_background_power = Spinbox(frame_1_2, from_=0, to=float("inf"), increment=0.1, textvariable=VARIABLES.var_spinbox_background_power)
        self.spinbox_background_power.pack(side="top", anchor="w")
        ttk.Label(frame_1_2, text="Wait time after each setpoint change (s):").pack(side="top", anchor="w")
        Spinbox(frame_1_2, from_=0, to=float("inf"), increment=0.1, textvariable=VARIABLES.var_spinbox_cwcontroller_wait_time).pack(side="top", anchor="w", pady=(0, 20))
        self.save = Save(frame_1_2, VARIABLES.var_entry_setpoint_conversion_directory, VARIABLES.var_entry_setpoint_conversion_filename)
        ttk.Button(frame_1_2, text="Load from above file", command=self.load).pack(side="top", anchor="w", pady=(0, 20))
        SetPointConversionTask(frame_1_3, self)
        self.text_header = "Setpoint (mA),Power (uW)"
        ttk.Label(frame_2, text=self.text_header).pack(side="top", anchor="w", padx=10, pady=10)
        self.text_setpoint_power = tk.Text(frame_2)
        self.text_setpoint_power.pack(side="left", anchor="w", padx=10, pady=10)
        self.text_setpoint_power.bind("<Key>", lambda e: "break")
        self.scrollbar = ttk.Scrollbar(frame_2, orient="vertical", command=self.text_setpoint_power.yview)
        self.scrollbar.pack(side="left", fill="y")
        self.text_setpoint_power.configure(yscrollcommand=self.scrollbar.set)
        return frame
    def load(self):
        self.text_setpoint_power.delete("1.0", "end")
        X = []
        power_list = []
        try:
            with open(VARIABLES.var_entry_setpoint_conversion_directory.get() + "/" + VARIABLES.var_entry_setpoint_conversion_filename.get(), "r") as f:
                for line in f:
                    if self.text_header not in line:
                        self.text_setpoint_power.insert("end", line)
                        setpoint, power = line.split(",")
                        X.append(float(setpoint))
                        power_list.append(float(power))
            self.save.data_dict["header"] = ["Setpoint (mA)", "Power (uW)"]
            self.save.data_dict["data"] = [X, power_list]
            GLOBALS.setpoints_to_convert = X
            GLOBALS.powers_converted_from_setpoints = power_list
        except Exception as e:
            LOGGER.error("Error loading setpoint conversion file: " + str(e))
            raise e

class SetPointConversionTask(Task):
    def __init__(self, parent, page: SetpointConversion) -> None:
        super().__init__(parent)
        self.page = page
        self.on_off_widgets = [self.page.spinbox_start_setpoint,
                               self.page.spinbox_end_setpoint,
                               self.page.spinbox_step_setpoint,
                               self.page.spinbox_background_power,
                               ]
    
    def task(self):
        INSTANCES.cwcontroller.set_current_setpoint(self.curr_setpoint)
        sleep(float(VARIABLES.var_spinbox_cwcontroller_wait_time.get()))
        VARIABLES.var_entry_cwcontroller_curr_setpoint.set(round(INSTANCES.cwcontroller.get_current_setpoint_mA(), 6))
        sleep(INSTANCES.powermeter.max_period + 0.2)
        self.curr_power = round(INSTANCES.powermeter.get_power_uW() - float(VARIABLES.var_spinbox_background_power.get()), 6)
        LOGGER.log("[Sweeping setpoint conversion] Setpoint (mA): {}, Power (uW): {}.".format(self.curr_setpoint, self.curr_power))
        if self.check_stopping():
            return
        self.X.append(self.curr_setpoint)
        self.power_list.append(self.curr_power)
        self.page.text_setpoint_power.insert("end", "{},{}\n".format(self.curr_setpoint, self.curr_power))
        self.save_data()
        if float(VARIABLES.var_spinbox_setpoint_conversion_start_setpoint.get()) <= float(VARIABLES.var_spinbox_setpoint_conversion_end_setpoint.get()):
            self.curr_setpoint += float(
                VARIABLES.var_spinbox_setpoint_conversion_step_setpoint.get())
        else:
            self.curr_setpoint -= float(
                VARIABLES.var_spinbox_setpoint_conversion_step_setpoint.get())
        self.curr_setpoint = round(self.curr_setpoint, 6)
        
    def task_loop(self):
        try:
            super().task_loop()
        except Exception as e:
            LOGGER.log(e)
            self.reset(error=True)
            raise e
    
    def save_data(self):
        if self.check_stopping():
            return
        self.page.save.data_dict["header"] = ["Setpoint (mA)", "Power (uW)"]
        self.page.save.data_dict["data"] = [self.X, self.power_list]
        GLOBALS.setpoints_to_convert = self.X
        GLOBALS.powers_converted_from_setpoints = self.power_list
        self.page.save.save(update_datetime=False)

    def start(self):
        for widget in self.on_off_widgets:
            widget.config(state="disabled")
        self.num = int(abs(float(VARIABLES.var_spinbox_setpoint_conversion_end_setpoint.get()) - float(
            VARIABLES.var_spinbox_setpoint_conversion_start_setpoint.get()))) / float(VARIABLES.var_spinbox_setpoint_conversion_step_setpoint.get()) + 1
        if self.status != PAUSED:
            self.curr_setpoint = float(VARIABLES.var_spinbox_setpoint_conversion_start_setpoint.get())
            self.page.save.update_datetime()
            self.page.text_setpoint_power.delete("1.0", "end")
            self.X = []
            self.power_list = []
            GLOBALS.setpoints_to_convert = []
            GLOBALS.powers_converted_from_setpoints = []
        super().start()
    
    def reset(self, error=False):
        for widget in self.on_off_widgets:
            widget.config(state="normal")
        INSTANCES.cwcontroller.set_current_setpoint(0)
        VARIABLES.var_entry_cwcontroller_curr_setpoint.set(round(INSTANCES.cwcontroller.get_current_setpoint_mA(), 6))
        self.page.save.reset()
        super().reset()
        if not error:
            LOGGER.reset()
    
    def paused(self):
        super().paused()
        for widget in self.on_off_widgets:
            widget.config(state="normal")