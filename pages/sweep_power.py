from time import sleep
from tkinter import ttk
from utils.spinbox import Spinbox
from utils.config import UTILS, VARIABLES, INSTANCES, LOGGER
from utils.save import Save
from utils.task import PAUSED, Task
from utils.plot import Plot
import numpy as np

class SweepPower:
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
        frame_3 = ttk.Frame(frame)
        frame_3.pack(side="top", padx=10, pady=10)
        frame_3_1 = ttk.Frame(frame_3)
        frame_3_1.pack(side="left", padx=10)
        frame_3_2 = ttk.Frame(frame_3)
        frame_3_2.pack(side="left", padx=10)
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
        SweepPowerTask(frame_1_3, self)
        ttk.Label(frame_2_1, text="Ch1 Instant (V-s)").pack(side="top")
        self.plot_lifetime_instant_ch1 = Plot(frame_2_1)
        ttk.Label(frame_2_2, text="Ch1 Average (V-s)").pack(side="top")
        self.plot_lifetime_average_ch1 = Plot(frame_2_2)
        ttk.Label(frame_3_1, text="Ch2 Instant (V-s)").pack(side="top")
        self.plot_lifetime_instant_ch2 = Plot(frame_3_1)
        ttk.Label(frame_3_2, text="Ch2 Average (V-s)").pack(side="top")
        self.plot_lifetime_average_ch2 = Plot(frame_3_2)
        return frame



class SweepPowerTask(Task):
    def __init__(self, parent, page: SweepPower) -> None:
        super().__init__(parent)
        self.page = page
        self.on_off_widgets = [self.page.spinbox_start_angle,
                               self.page.spinbox_end_angle,
                               self.page.spinbox_step_angle,
                               self.page.spinbox_sweep_power_num,
                               self.page.spinbox_background_power,
                               ]

    def task(self):
        INSTANCES.ndfilter.set_angle(self.curr_angle)
        VARIABLES.var_entry_curr_angle.set(INSTANCES.ndfilter.get_angle())
        sleep(INSTANCES.powermeter.max_period + 0.2)
        self.curr_power = np.round(INSTANCES.powermeter.get_power_uW(), 4) - float(VARIABLES.var_spinbox_background_power.get())
        VARIABLES.var_entry_curr_power.set(self.curr_power)
        num = int(VARIABLES.var_spinbox_sweep_power_num.get())
        X = None
        data_ch1 = None
        data_ch2 = None
        for i in range(num):
            if self.check_stopping():
                return
            LOGGER.log("[Sweeping power] Angle (deg): {}, Power (uW): {}, Measurement: {}/{}.".format(self.curr_angle, self.curr_power, i + 1, num))
            wait_time = float(
                VARIABLES.var_spinbox_sweep_power_wait_time.get())
            X, curr_data_ch1, curr_data_ch2 = INSTANCES.oscilloscope.get_data(
                wait_time)
            data_ch1 = np.asarray(data_ch1) * (i / (i + 1)) + np.asarray(
                curr_data_ch1) * (1 / (i + 1)) if i > 0 else curr_data_ch1
            data_ch2 = np.asarray(data_ch2) * (i / (i + 1)) + np.asarray(
                curr_data_ch2) * (1 / (i + 1)) if i > 0 else curr_data_ch2
            # Below code for plotting in new thread is to update GUI in real time.
            # Directly plotting can only update GUI after the loop is finished,
            # though not freezing the GUI since the loop is already running in a
            # different thread other than the main thread. Use with caution as it
            # has small chance to cause thread safety issues.

            def plot():
                self.page.plot_lifetime_instant_ch1.plot(
                    X, curr_data_ch1, "-", c="black", linewidth=0.5)
                self.page.plot_lifetime_average_ch1.plot(
                    X, data_ch1, "-", c="black", linewidth=0.5)
                self.page.plot_lifetime_instant_ch2.plot(
                    X, curr_data_ch2, "-", c="black", linewidth=0.5)
                self.page.plot_lifetime_average_ch2.plot(
                    X, data_ch2, "-", c="black", linewidth=0.5)
            plot()
            # plot_thread = Thread(target=plot)
            # plot_thread.setDaemon(True)
            # plot_thread.start()
        self.save_data(X, data_ch1, data_ch2)
        if self.check_stopping():
            return
        if float(VARIABLES.var_spinbox_start_angle.get()) <= float(VARIABLES.var_spinbox_end_angle.get()):
            self.curr_angle += float(
                VARIABLES.var_spinbox_step_angle.get())
        else:
            self.curr_angle -= float(
                VARIABLES.var_spinbox_step_angle.get())
    
    def task_loop(self):
        try:
            super().task_loop()
        except Exception as e:
            LOGGER.log(e)
            self.reset()
            raise e
        
    def save_data(self, X, data_ch1, data_ch2):
        if self.check_stopping():
            return
        if not self.page.save.data_dict["header"]:
            self.page.save.data_dict["header"].append("time(s)")
            self.page.save.data_dict["data"].append(X)
        self.page.save.data_dict["header"].append(
            f"{self.curr_angle}deg_{self.curr_power}uW_ch1")
        self.page.save.data_dict["data"].append(data_ch1)
        self.page.save.data_dict["header"].append(
            f"{self.curr_angle}deg_{self.curr_power}uW_ch2")
        self.page.save.data_dict["data"].append(data_ch2)
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

    def reset(self):
        for widget in self.on_off_widgets:
            widget.config(state="normal")
        self.page.save.reset()
        super().reset()

    def paused(self):
        super().paused()
        for widget in self.on_off_widgets:
            widget.config(state="normal")