from time import sleep
from tkinter import ttk
from utils.config import GLOBALS, VARIABLES, INSTANCES, LOGGER
from utils.spinbox import Spinbox
from utils.save import Save
from utils.task import PAUSED, Task
from utils.plot import Plot
import numpy as np


class SweepPowerCW:
    def __init__(self, parent) -> None:
        self.frame = self.set_frame(parent)
    
    def set_frame(self, parent):
        frame = ttk.Frame(parent)
        frame.pack()
        frame_1 = ttk.Frame(frame)
        frame_1.pack(side="top", anchor="w", padx=10, pady=10)
        frame_1_1 = ttk.Frame(frame_1)
        frame_1_1.pack(side="left", padx=100)
        frame_1_2 = ttk.Frame(frame_1)
        frame_1_2.pack(side="left", padx=(100, 50))
        frame_1_3 = ttk.Frame(frame_1)
        frame_1_3.pack(side="left", padx=10)
        frame_2 = ttk.Frame(frame)
        frame_2.pack(side="top", padx=10, pady=10)
        frame_2_1 = ttk.Frame(frame_2)
        frame_2_1.pack(side="left", padx=10)
        frame_2_2 = ttk.Frame(frame_2)
        frame_2_2.pack(side="left", padx=10)
        ttk.Label(frame_1_1, text="CWController Currently: ").pack(side="top", anchor="w", padx=10)
        ttk.Entry(frame_1_1, state="readonly", textvariable=VARIABLES.var_entry_cwcontroller_status).pack(side="top", anchor="w", padx=10)
        ttk.Button(frame_1_1, text="ON", command=self.turn_on_cw).pack(side="top", anchor="w", padx=10)
        ttk.Button(frame_1_1, text="OFF", command=self.turn_off_cw).pack(side="top", anchor="w", padx=10)
        ttk.Label(frame_1_1, text="CWController Current Setpoint (mA): ").pack(side="top", anchor="w", padx=10)
        ttk.Entry(frame_1_1, state="readonly", textvariable=VARIABLES.var_entry_cwcontroller_curr_setpoint).pack(side="top", anchor="w", padx=10)
        ttk.Label(frame_1_1, text="Set Current Setpoint (mA): ").pack(side="top", anchor="w", padx=10)
        ttk.Label(frame_1_1, text="Recommended Safe Range: 0 - 40mA", font="TkDefaultFont 8").pack(side="top", anchor="w", padx=10)
        self.spinbox_target_setpoint = Spinbox(frame_1_1, from_=0, to=float('inf'), increment=0.1, textvariable=VARIABLES.var_spinbox_cwcontroller_target_setpoint)
        self.spinbox_target_setpoint.pack(side="top", anchor="w", padx=10)
        ttk.Button(frame_1_1, text="Set", command=self.on_set_current_setpoint).pack(side="top", anchor="w", padx=10)
        ttk.Label(frame_1_2, text="Start Current Setpoint (mA): ").pack(side="top", anchor="w", padx=10)
        ttk.Label(frame_1_2, text="Recommended Safe Range: 0 - 40mA", font="TkDefaultFont 8").pack(side="top", anchor="w", padx=10)
        self.spinbox_start_setpoint = Spinbox(frame_1_2, from_=0, to=float('inf'), textvariable=VARIABLES.var_spinbox_cwcontroller_start_setpoint)
        self.spinbox_start_setpoint.pack(side="top", anchor="w", padx=10)
        ttk.Label(frame_1_2, text="End Current Setpoint (mA): ").pack(side="top", anchor="w", padx=10)
        ttk.Label(frame_1_2, text="Recommended Safe Range: 0 - 40mA", font="TkDefaultFont 8").pack(side="top", anchor="w", padx=10)
        self.spinbox_end_setpoint = Spinbox(frame_1_2, from_=0, to=float('inf'), textvariable=VARIABLES.var_spinbox_cwcontroller_end_setpoint)
        self.spinbox_end_setpoint.pack(side="top", anchor="w", padx=10)
        ttk.Label(frame_1_2, text="Step Size (mA): ").pack(side="top", anchor="w", padx=10)
        self.spinbox_step_setpoint = Spinbox(frame_1_2, from_=0, to=float('inf'), textvariable=VARIABLES.var_spinbox_cwcontroller_step_setpoint)
        self.spinbox_step_setpoint.pack(side="top", anchor="w", padx=10)
        ttk.Label(frame_1_2, text="Number of measurements per point:").pack(side="top", anchor="w", padx=10)
        self.spinbox_sweep_power_cw_num = Spinbox(frame_1_2, from_=0, to=float('inf'), textvariable=VARIABLES.var_spinbox_sweep_power_cw_num)
        self.spinbox_sweep_power_cw_num.pack(side="top", anchor="w", padx=10)
        ttk.Label(frame_1_3, text="Background Power (uW):").pack(side="top", anchor="w")
        self.spinbox_background_power = Spinbox(frame_1_3, from_=0, to=float("inf"), increment=0.1, textvariable=VARIABLES.var_spinbox_background_power)
        self.spinbox_background_power.pack(side="top", anchor="w")
        ttk.Label(frame_1_3, text="Wait time after each setpoint change (s):").pack(side="top", anchor="w")
        Spinbox(frame_1_3, from_=0, to=float("inf"), increment=0.1, textvariable=VARIABLES.var_spinbox_cwcontroller_wait_time).pack(side="top", anchor="w")
        self.checkbutton_load_conversion = ttk.Checkbutton(frame_1_3, text="Load power from Setpoint Conversion page (instead of new powermeter measurement).", variable=VARIABLES.var_checkbutton_checkbutton_load_conversion)
        self.checkbutton_load_conversion.pack(side="top", anchor="w")
        self.save = Save(frame_1_3, VARIABLES.var_entry_sweep_power_cw_directory, VARIABLES.var_entry_sweep_power_cw_filename)
        ttk.Label(frame_2_1, text="Ch1 (V-uW)").pack(side="top")
        self.plot_lockin_top = Plot(frame_2_1, figsize=(10, 8))
        ttk.Label(frame_2_2, text="Ch2 (V-uW)").pack(side="top")
        self.plot_lockin_bottom = Plot(frame_2_2, figsize=(10, 8))
        SweepPowerCWTask(frame_1_3, self)
        return frame
    
    def turn_on_cw(self):
        INSTANCES.cwcontroller.set_on()
        VARIABLES.var_entry_cwcontroller_status.set(INSTANCES.cwcontroller.get_status())
    
    def turn_off_cw(self):
        INSTANCES.cwcontroller.set_off()
        VARIABLES.var_entry_cwcontroller_status.set(INSTANCES.cwcontroller.get_status())
    
    def on_set_current_setpoint(self):
        INSTANCES.cwcontroller.set_current_setpoint(VARIABLES.var_spinbox_cwcontroller_target_setpoint.get())
        VARIABLES.var_entry_cwcontroller_curr_setpoint.set(INSTANCES.cwcontroller.get_current_setpoint_mA())

class SweepPowerCWTask(Task):
    def __init__(self, parent, page: SweepPowerCW):
        super().__init__(parent)
        self.page = page
        self.on_off_widgets = [self.page.spinbox_start_setpoint,
                               self.page.spinbox_end_setpoint,
                               self.page.spinbox_step_setpoint,
                               self.page.spinbox_target_setpoint,
                               self.page.spinbox_sweep_power_cw_num,
                               self.page.spinbox_background_power,
                               self.page.checkbutton_load_conversion,
                               ]
        
    
    def task(self):
        INSTANCES.cwcontroller.set_current_setpoint(self.curr_setpoint)
        sleep(float(VARIABLES.var_spinbox_cwcontroller_wait_time.get()))
        VARIABLES.var_entry_cwcontroller_curr_setpoint.set(round(INSTANCES.cwcontroller.get_current_setpoint_mA(), 6))
        if VARIABLES.var_checkbutton_checkbutton_load_conversion.get():
            self.curr_power = GLOBALS.powers_converted_from_setpoints[GLOBALS.setpoints_to_convert.index(self.curr_setpoint)]
        else:
            sleep(INSTANCES.powermeter.max_period + 0.2)
            self.curr_power = round(INSTANCES.powermeter.get_power_uW() - float(VARIABLES.var_spinbox_background_power.get()), 6)
        LOGGER.log("[Sweeping power (CW)] Setpoint (mA): {}, Power (uW): {}.".format(self.curr_setpoint, self.curr_power))
        num = int(VARIABLES.var_spinbox_sweep_power_cw_num.get())
        data_lockin_top = 0
        data_lockin_bottom = 0
        for i in range(num):
            if self.check_stopping():
                return
            curr_data_top, curr_data_bottom = INSTANCES.lockin_top.get_output(), INSTANCES.lockin_bottom.get_output()
            data_lockin_top = data_lockin_top * (i / (i + 1)) + curr_data_top / (i + 1)
            data_lockin_bottom = data_lockin_bottom * (i / (i + 1)) + curr_data_bottom / (i + 1)
        if self.check_stopping():
            return
        self.X.append(self.curr_setpoint)
        self.power_list.append(self.curr_power)
        self.data_lockin_top_list.append(data_lockin_top)
        self.data_lockin_bottom_list.append(data_lockin_bottom)
        self.page.plot_lockin_top.plot(
            self.power_list, self.data_lockin_top_list, "-", c="black", linewidth=0.5)
        self.page.plot_lockin_bottom.plot(
            self.power_list, self.data_lockin_bottom_list, "-", c="black", linewidth=0.5)
        if self.check_stopping():
            return
        self.save_data()
        if float(VARIABLES.var_spinbox_cwcontroller_start_setpoint.get()) <= float(VARIABLES.var_spinbox_cwcontroller_end_setpoint.get()):
            self.curr_setpoint += float(
                VARIABLES.var_spinbox_cwcontroller_step_setpoint.get())
        else:
            self.curr_setpoint -= float(
                VARIABLES.var_spinbox_cwcontroller_step_setpoint.get())
        self.curr_setpoint = round(self.curr_setpoint, 6)

    def task_loop(self):
        try:
            super().task_loop()
        except Exception as e:
            LOGGER.log(e)
            self.reset()
            raise e
    
    def save_data(self):
        if self.check_stopping():
            return
        self.page.save.data_dict["header"] = ["Setpoint (mA)", "Power (uW)", "Ch1 (V)", "Ch2 (V)"]
        self.page.save.data_dict["data"] = [self.X, self.power_list, self.data_lockin_top_list, self.data_lockin_bottom_list]
        self.page.save.save(update_datetime=False)
    
    def start(self):
        for widget in self.on_off_widgets:
            widget.config(state="disabled")
        self.num = int(abs(float(VARIABLES.var_spinbox_cwcontroller_end_setpoint.get()) - float(
            VARIABLES.var_spinbox_cwcontroller_start_setpoint.get()))) / float(VARIABLES.var_spinbox_cwcontroller_step_setpoint.get()) + 1
        if self.status != PAUSED:
            self.curr_setpoint = float(VARIABLES.var_spinbox_cwcontroller_start_setpoint.get())
            self.page.save.update_datetime()
            self.X = []
            self.power_list = []
            self.data_lockin_top_list = []
            self.data_lockin_bottom_list = []
        super().start()
    
    def reset(self):
        for widget in self.on_off_widgets:
            widget.config(state="normal")
        INSTANCES.cwcontroller.set_current_setpoint(0)
        VARIABLES.var_entry_cwcontroller_curr_setpoint.set(round(INSTANCES.cwcontroller.get_current_setpoint_mA(), 6))
        self.page.save.reset()
        super().reset()
    
    def paused(self):
        super().paused()
        for widget in self.on_off_widgets:
            widget.config(state="normal")
    

