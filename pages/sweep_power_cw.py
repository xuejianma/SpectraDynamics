from tkinter import ttk
from utils.config import VARIABLES, INSTANCES, LOGGER
from utils.spinbox import Spinbox
from utils.save import Save
from utils.task import Task
from utils.plot import Plot


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
        self.spinbox_target_setpoint = Spinbox(frame_1_1, from_=0, to=float('inf'), textvariable=VARIABLES.var_spinbox_cwcontroller_target_setpoint)
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
        self.spinbox_step_size = Spinbox(frame_1_2, from_=0, to=float('inf'), textvariable=VARIABLES.var_spinbox_cwcontroller_step_setpoint)
        self.spinbox_step_size.pack(side="top", anchor="w", padx=10)
        ttk.Label(frame_1_2, text="Number of measurements per point:").pack(side="top", anchor="w", padx=10)
        self.spinbox_sweep_power_cw_num = Spinbox(frame_1_2, from_=0, to=float('inf'), textvariable=VARIABLES.var_spinbox_sweep_power_cw_num)
        self.spinbox_sweep_power_cw_num.pack(side="top", anchor="w", padx=10)
        self.save = Save(frame_1_3, VARIABLES.var_entry_sweep_power_cw_directory, VARIABLES.var_entry_sweep_power_cw_filename)
        ttk.Label(frame_2_1, text="Ch1 (V-uW)").pack(side="top")
        self.plot_lifetime_instant_ch1 = Plot(frame_2_1, figsize=(12, 8))
        ttk.Label(frame_2_2, text="Ch2 (V-uW)").pack(side="top")
        self.plot_lifetime_average_ch1 = Plot(frame_2_2, figsize=(12, 8))
        SweepPowerCWTask(frame_1_3)
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
    def __init__(self, parent):
        super().__init__(parent)
    
    def task(self):
        super().task()

    def task_loop(self):
        try:
            super().task_loop()
        except Exception as e:
            LOGGER.log(e)
            self.reset()
            raise e
    
    def save_data(self):
        pass
    
    def start(self):
        super().start()
    
    def reset(self):
        super().reset()
    
    def paused(self):
        super().paused()
    

