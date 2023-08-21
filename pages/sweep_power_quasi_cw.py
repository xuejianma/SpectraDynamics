from time import sleep
from tkinter import ttk
from utils.spinbox import Spinbox
from utils.config import UTILS, VARIABLES, INSTANCES, LOGGER
from utils.save import Save
from utils.task import PAUSED, Task
from utils.plot import Plot
import numpy as np

class SweepPowerQuasiCW:
    def __init__(self, parent) -> None:
        self.frame = self.set_frame(parent)
    
    def set_frame(self, parent):
        frame = ttk.Frame(parent)
        frame_1 = ttk.Frame(frame)
        frame_1.pack(side="top", anchor="w", padx=10, pady=10)
        frame_1_1 = ttk.Frame(frame_1)
        frame_1_1.pack(side="left", padx=100)
        frame_1_2 = ttk.Frame(frame_1)
        frame_1_2.pack(side="left", padx=(100, 50))
        frame_1_3 = ttk.Frame(frame_1)
        frame_1_3.pack(side="left", padx=(100, 50))
        frame_2 = ttk.Frame(frame)
        frame_2.pack(side="top", padx=10, pady=10)
        frame_2_1 = ttk.Frame(frame_2)
        frame_2_1.pack(side="left", padx=10)
        frame_2_2 = ttk.Frame(frame_2)
        frame_2_2.pack(side="left", padx=10)
        ttk.Label(frame_1_1, text="Start angle (deg): ").pack(side="top", anchor="w")
        self.spinbox_start_angle = Spinbox(frame_1_1, from_=0, to=360, increment=1, width=15, textvariable=VARIABLES.var_spinbox_start_angle)
        self.spinbox_start_angle.pack(side="top", anchor="w")
        ttk.Label(frame_1_1, text="End angle (deg): ").pack(side="top", anchor="w")
        self.spinbox_end_angle = Spinbox(frame_1_1, from_=0, to=360, increment=1, width=15, textvariable=VARIABLES.var_spinbox_end_angle)
        self.spinbox_end_angle.pack(side="top", anchor="w")
        ttk.Label(frame_1_1, text="Step angle (deg): ", width=15).pack(side="top", anchor="w")
        self.spinbox_step_angle = Spinbox(frame_1_1, from_=0, to=360, increment=1, width=15, textvariable=VARIABLES.var_spinbox_step_angle)
        self.spinbox_step_angle.pack(side="top", anchor="w")
        ttk.Label(frame_1_2, text="Background Power (uW):").pack(
            side="top", anchor="w")
        self.spinbox_background_power = Spinbox(frame_1_2, from_=0, to=float(
            "inf"), increment=0.1, textvariable=VARIABLES.var_spinbox_background_power)
        self.spinbox_background_power.pack(side="top", anchor="w")
        ttk.Label(frame_1_2, text="Number of measurements: ").pack(side="top", anchor="w")
        self.spinbox_sweep_power_num = Spinbox(frame_1_2, from_=1, to=float(
            "inf"),increment=1, width=15, textvariable=VARIABLES.var_spinbox_sweep_power_num)
        self.spinbox_sweep_power_num.pack(side="top", anchor="w")
        ttk.Label(frame_1_2, text="Wait time (s): ").pack(side="top", anchor="w")
        Spinbox(frame_1_2, from_=0, to=float(
            "inf"), increment=1, width=15, textvariable=VARIABLES.var_spinbox_sweep_power_wait_time).pack(side="top", anchor="w")
        self.save = Save(frame_1_3, VARIABLES.var_entry_sweep_power_directory, VARIABLES.var_entry_sweep_power_filename)
        SweepPowerQuasiCWTask(frame_1_3, self)
        ttk.Label(frame_2_1, text="Ch1 (V-uW)").pack(side="top")
        self.plot_ch1 = Plot(frame_2_1, figsize=(10, 5))
        ttk.Label(frame_2_2, text="Ch2 (V-uW)").pack(side="top")
        self.plot_ch2 = Plot(frame_2_2, figsize=(10, 5))
        return frame



class SweepPowerQuasiCWTask(Task):
    def __init__(self, parent, page: SweepPowerQuasiCW) -> None:
        super().__init__(parent)
        self.page = page
        self.on_off_widgets = [self.page.spinbox_start_angle,
                               self.page.spinbox_end_angle,
                               self.page.spinbox_step_angle,
                               self.page.spinbox_sweep_power_num,
                               self.page.spinbox_background_power,
                               ]
        self.power_list = []
        self.data_ch1 = []
        self.data_ch2 = []

    def task(self):
        INSTANCES.ndfilter.set_angle_direct(self.curr_angle)
        VARIABLES.var_entry_curr_angle.set(INSTANCES.ndfilter.get_angle())
        sleep(INSTANCES.powermeter.max_period + 0.2)
        self.curr_power = round(INSTANCES.powermeter.get_power_uW() - float(VARIABLES.var_spinbox_background_power.get()), 6)
        VARIABLES.var_entry_curr_power.set(self.curr_power)
        num = int(VARIABLES.var_spinbox_sweep_power_num.get())
        X = None
        curr_data_ch1 = 0
        curr_data_ch2 = 0
        for i in range(num):
            if self.check_stopping():
                return
            LOGGER.log("[Sweeping power] Angle (deg): {}, Power (uW): {}, Measurement: {}/{}.".format(self.curr_angle, self.curr_power, i + 1, num))
            wait_time = float(
                VARIABLES.var_spinbox_sweep_power_wait_time.get())
            curr_data_ch1 += INSTANCES.lockin_top.get_output()
            curr_data_ch2 += INSTANCES.lockin_bottom.get_output()
            sleep(wait_time)
        curr_data_ch1 /= num
        curr_data_ch2 /= num
        self.power_list.append(self.curr_power)
        self.data_ch1.append(curr_data_ch1)
        self.data_ch2.append(curr_data_ch2)
        self.save_data(self.power_list, self.data_ch1, self.data_ch2)
        self.page.plot_ch1.plot(self.power_list, self.data_ch1)
        self.page.plot_ch2.plot(self.power_list, self.data_ch2)
        if self.check_stopping():
            return
        if float(VARIABLES.var_spinbox_start_angle.get()) <= float(VARIABLES.var_spinbox_end_angle.get()):
            self.curr_angle += float(
                VARIABLES.var_spinbox_step_angle.get())
        else:
            self.curr_angle -= float(
                VARIABLES.var_spinbox_step_angle.get())
        self.curr_angle = round(self.curr_angle, 6)
    
    def task_loop(self):
        try:
            super().task_loop()
        except Exception as e:
            LOGGER.log(e)
            self.reset(error=True)
            raise e
        
    def save_data(self, power_list, data_ch1, data_ch2):
        if self.check_stopping():
            return
        if not self.page.save.data_dict["header"]:
            self.page.save.data_dict["header"].append("Power (uW)")
            self.page.save.data_dict["header"].append("Ch1 (V)")
            self.page.save.data_dict["header"].append("Ch2 (V)")
            self.page.save.data_dict["data"].append(power_list)
            self.page.save.data_dict["data"].append(data_ch1)
            self.page.save.data_dict["data"].append(data_ch2)
        else:
            self.page.save.data_dict["data"][0] = power_list
            self.page.save.data_dict["data"][1] = data_ch1
            self.page.save.data_dict["data"][2] = data_ch2
        self.page.save.save(update_datetime=False)

    def start(self):
        for widget in self.on_off_widgets:
            widget.config(state="disabled")
        self.num = int(abs(float(VARIABLES.var_spinbox_end_angle.get()) - float(
            VARIABLES.var_spinbox_start_angle.get()))) / float(VARIABLES.var_spinbox_step_angle.get()) + 1
        if self.status != PAUSED:
            self.curr_angle = float(VARIABLES.var_spinbox_start_angle.get())
            self.page.save.update_datetime()
        super().start()

    def reset(self, error=False):
        for widget in self.on_off_widgets:
            widget.config(state="normal")
        self.page.save.reset()
        self.power_list = []
        self.data_ch1 = []
        self.data_ch2 = []
        super().reset()
        if not error:
            LOGGER.reset()

    def paused(self):
        super().paused()
        for widget in self.on_off_widgets:
            widget.config(state="normal")