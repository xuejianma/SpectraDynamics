from tkinter import ttk
from utils.config import INSTANCES, VARIABLES, LOGGER
from utils.spinbox import Spinbox
from utils.plot import Plot
from utils.task import Task, RUNNING
from utils.save import Save
from threading import Thread
from time import sleep
import numpy as np


class SweepWavelength:
    def __init__(self, parent) -> None:
        self.frame, frame_1_7 = self.set_frame(parent)
        self.set_angle_task = SetAngleTask(self.button_set_angle)
        self.read_power_task = ReadPowerTask(self.button_power)
        self.set_wavelength_task = SetWavelengthTask(
            self.button_set_wavelength)
        self.set_actuator_position_task = SetActuatorPositionTask(
            self.button_set_actuator_position)
        Save(frame_1_7, VARIABLES.var_entry_sweep_wavelength_directory, VARIABLES.var_entry_sweep_wavelength_filename,
             substitute_dict={"wavelength": VARIABLES.var_entry_curr_wavelength})
        SweepWavelengthTask(frame_1_7, self)

    def set_frame(self, parent):
        frame = ttk.Frame(parent)
        frame_1 = ttk.Frame(frame)
        frame_1.pack(side="top", anchor="w", padx=10, pady=10)
        frame_2 = ttk.Frame(frame)
        frame_2.pack(side="top", padx=10)
        frame_3 = ttk.Frame(frame)
        frame_3.pack(side="top", padx=10, pady=10)
        frame_1_1 = ttk.Frame(frame_1)
        frame_1_1.pack(side="left", anchor="n", padx=10)
        frame_1_2 = ttk.Frame(frame_1)
        frame_1_2.pack(side="left", anchor="n", padx=10)
        frame_1_3 = ttk.Frame(frame_1)
        frame_1_3.pack(side="left", anchor="n", padx=10)
        frame_1_4 = ttk.Frame(frame_1)
        frame_1_4.pack(side="left", anchor="n", padx=10)
        frame_1_5 = ttk.Frame(frame_1)
        frame_1_5.pack(side="left", anchor="n", padx=10)
        frame_1_6 = ttk.Frame(frame_1)
        frame_1_6.pack(side="left", anchor="n", padx=10)
        frame_1_7 = ttk.Frame(frame_1)
        frame_1_7.pack(side="left", anchor="n", padx=10)
        frame_2_1 = ttk.Frame(frame_2)
        frame_2_1.pack(side="left", anchor="n", padx=10)
        frame_2_2 = ttk.Frame(frame_2)
        frame_2_2.pack(side="left", anchor="n", padx=10)
        frame_3_1 = ttk.Frame(frame_3)
        frame_3_1.pack(side="left", anchor="n", padx=10)
        frame_3_2 = ttk.Frame(frame_3)
        frame_3_2.pack(side="left", anchor="n", padx=10)
        ttk.Label(frame_1_1, text="Current Wavelength (nm):").pack(
            side="top", anchor="w")
        ttk.Entry(frame_1_1, state="readonly", textvariable=VARIABLES.var_entry_curr_wavelength).pack(
            side="top", anchor="w")
        ttk.Label(frame_1_1, text="Target Wavelength (nm):").pack(
            side="top", anchor="w")
        self.spinbox_target_wavelength = Spinbox(frame_1_1, from_=0, to=float("inf"), increment=0.1,
                                                 textvariable=VARIABLES.var_spinbox_target_wavelength)
        self.spinbox_target_wavelength.pack(side="top", anchor="w")
        self.button_set_wavelength = ttk.Button(
            frame_1_1, text="Set Wavelength", command=self.on_set_wavelength)
        self.button_set_wavelength.pack(side="top", anchor="w")
        ttk.Label(frame_1_2, text="Current NDFilter Angle (deg): ").pack(
            side="top", anchor="w")
        ttk.Entry(frame_1_2, state="readonly", textvariable=VARIABLES.var_entry_curr_angle).pack(
            side="top", anchor="w")
        ttk.Label(frame_1_2, text="Target Angle (deg): ").pack(
            side="top", anchor="w")
        self.spinbox_target_angle = Spinbox(frame_1_2, from_=0, to=360, increment=0.1,
                                            textvariable=VARIABLES.var_spinbox_target_angle)
        self.spinbox_target_angle.pack(side="top", anchor="w")
        self.button_set_angle = ttk.Button(
            frame_1_2, text="Set Angle", command=self.on_set_angle)
        self.button_set_angle.pack(side="top", anchor="w")
        ttk.Label(frame_1_2, text="Note: Make sure power decreases\nwith NDFilter angle.",
                  font="TkDefaultFont 8").pack(side="top", anchor="w")
        ttk.Label(frame_1_3, text="Actuator Position (mm): ").pack(
            side="top", anchor="w")
        ttk.Entry(frame_1_3, state="readonly", textvariable=VARIABLES.var_entry_curr_actuator_position).pack(
            side="top", anchor="w")
        ttk.Label(frame_1_3, text="Target Actuator Position (mm): ").pack(
            side="top", anchor="w")
        self.spinbox_target_actuator_position = Spinbox(frame_1_3, from_=0, to=float("inf"), increment=0.1,
                                                        textvariable=VARIABLES.var_spinbox_target_actuator_position)
        self.spinbox_target_actuator_position.pack(side="top", anchor="w")
        self.button_set_actuator_position = ttk.Button(
            frame_1_3, text="Set Position", command=self.on_set_actuator_position)
        self.button_set_actuator_position.pack(side="top", anchor="w")
        ttk.Label(frame_1_4, text="Sweep Start Wavelength (nm): ").pack(
            side="top", anchor="w")
        self.spinbox_sweep_start_wavelength = Spinbox(frame_1_4, from_=0, to=float(
            "inf"), increment=0.1, textvariable=VARIABLES.var_spinbox_sweep_start_wavelength)
        self.spinbox_sweep_start_wavelength.pack(side="top", anchor="w")
        ttk.Label(frame_1_4, text="Sweep End Wavelength (nm): ").pack(
            side="top", anchor="w")
        self.spinbox_sweep_end_wavelength = Spinbox(frame_1_4, from_=0, to=float(
            "inf"), increment=0.1, textvariable=VARIABLES.var_spinbox_sweep_end_wavelength)
        self.spinbox_sweep_end_wavelength.pack(side="top", anchor="w")
        ttk.Label(frame_1_4, text="Sweep Step Size (nm): ").pack(
            side="top", anchor="w")
        self.spinbox_sweep_step_size = Spinbox(frame_1_4, from_=0, to=float(
            "inf"), increment=0.1, textvariable=VARIABLES.var_spinbox_sweep_step_size)
        self.spinbox_sweep_step_size.pack(side="top", anchor="w")
        ttk.Label(frame_1_5, text="Current Power (uW): ").pack(
            side="top", anchor="w")
        ttk.Entry(frame_1_5, state="readonly", textvariable=VARIABLES.var_entry_curr_power).pack(
            side="top", anchor="w")
        self.button_power = ttk.Button(
            frame_1_5, text="Turn ON", command=self.toggle_power_reading)
        self.button_power.pack(side="top", anchor="w")
        ttk.Label(frame_1_5, text="Target Power (uW): ").pack(
            side="top", anchor="w")
        self.spinbox_target_power = Spinbox(frame_1_5, from_=0, to=float("inf"), increment=0.1,
                                            textvariable=VARIABLES.var_spinbox_sweep_target_power)
        self.spinbox_target_power.pack(side="top", anchor="w")
        ttk.Label(frame_1_6, text="Number of measurements\nper wavelength").pack(
            side="top", anchor="w")
        self.spinbox_sweep_lifetime_num = Spinbox(frame_1_6, from_=0, to=float(
            "inf"), textvariable=VARIABLES.var_spinbox_sweep_lifetime_num)
        self.spinbox_sweep_lifetime_num.pack(side="top", anchor="w")
        ttk.Label(frame_1_6, text="Actuator explore range\nfor max power (±mm)").pack(
            side="top", anchor="w")
        self.spinbox_sweep_actuator_explore_range = Spinbox(frame_1_6, from_=0, to=float("inf"), increment=0.1,
                                                            textvariable=VARIABLES.var_spinbox_sweep_actuator_explore_range)
        self.spinbox_sweep_actuator_explore_range.pack(side="top", anchor="w")
        self.label_oscilloscope_wait_time = ttk.Label(
            frame_1_6, text="Oscilloscope wait time (s): ")
        self.label_oscilloscope_wait_time.pack(side="top", anchor="w")
        self.spinbox_sweep_oscilloscope_wait_time = Spinbox(frame_1_6, from_=0, to=float(
            "inf"), increment=0.1, textvariable=VARIABLES.var_spinbox_sweep_lifetime_wait_time)
        self.spinbox_sweep_oscilloscope_wait_time.pack(side="top", anchor="w")
        self.plot_lifetime_instant_ch1 = Plot(frame_2_1)
        self.plot_lifetime_average_ch1 = Plot(frame_2_2)
        self.plot_lifetime_instant_ch2 = Plot(frame_3_1)
        self.plot_lifetime_average_ch2 = Plot(frame_3_2)
        return frame, frame_1_7

    def toggle_power_reading(self):
        if self.read_power_task.is_running:
            self.turn_off_power_reading()
        else:
            self.turn_on_power_reading()

    def turn_off_power_reading(self):
        self.button_power.config(state="disabled")
        self.read_power_task.terminate()
        self.button_power["text"] = "Turn ON"

    def turn_on_power_reading(self):
        self.read_power_task.start()
        self.button_power["text"] = "Turn OFF"

    def on_set_angle(self):
        self.set_angle_task.start()

    def on_set_wavelength(self):
        self.set_wavelength_task.start()

    def on_set_actuator_position(self):
        self.set_actuator_position_task.start()


class SetAngleTask():
    def __init__(self, button_set_angle) -> None:
        self.button_set_angle = button_set_angle
        self.external_button_control = False

    def task_loop(self):
        if not self.external_button_control:
            self.button_set_angle.config(state="disabled")
        try:
            INSTANCES.ndfilter.set_angle(
                float(VARIABLES.var_spinbox_target_angle.get()))
            VARIABLES.var_entry_curr_angle.set(
                round(INSTANCES.ndfilter.get_angle(), 4))
        except Exception as e:
            LOGGER.log(e)
            raise e
        finally:
            if not self.external_button_control:
                self.button_set_angle.config(state="normal")

    def start(self):
        thread = Thread(target=self.task_loop)
        thread.start()


class ReadPowerTask():
    def __init__(self, button_power) -> None:
        self.is_running = False
        self.button_power = button_power

    def task_loop(self):
        try:
            while self.is_running:
                power = INSTANCES.powermeter.get_power_uW()
                VARIABLES.var_entry_curr_power.set(power)
        except Exception as e:
            LOGGER.log(e)
            raise e
        finally:
            self.button_power.config(state="normal")

    def start(self):
        self.is_running = True
        thread = Thread(target=self.task_loop)
        thread.start()

    def terminate(self):
        self.is_running = False


class SetWavelengthTask():
    def __init__(self, button_set_wavelength) -> None:
        self.button_set_wavelength = button_set_wavelength
        self.external_button_control = False

    def task_loop(self):
        if not self.external_button_control:
            self.button_set_wavelength.config(state="disabled")
        try:
            INSTANCES.monochromator.set_wavelength(
                float(VARIABLES.var_spinbox_target_wavelength.get()))
            VARIABLES.var_entry_curr_wavelength.set(
                round(INSTANCES.monochromator.get_wavelength(), 4))
        except Exception as e:
            LOGGER.log(e)
            raise e
        finally:
            if not self.external_button_control:
                self.button_set_wavelength.config(state="normal")

    def start(self):
        thread = Thread(target=self.task_loop)
        thread.start()


class SetActuatorPositionTask():
    def __init__(self, button_set_actuator_position) -> None:
        self.button_set_actuator_position = button_set_actuator_position
        self.external_button_control = False

    def task_loop(self):
        if not self.external_button_control:
            self.button_set_actuator_position.config(state="disabled")
        try:
            INSTANCES.actuator.set_position(
                float(VARIABLES.var_spinbox_target_actuator_position.get()))
            VARIABLES.var_entry_curr_actuator_position.set(
                round(INSTANCES.actuator.get_position(), 4))
        except Exception as e:
            LOGGER.log(e)
            raise e
        finally:
            if not self.external_button_control:
                self.button_set_actuator_position.config(state="normal")

    def start(self):
        thread = Thread(target=self.task_loop)
        thread.start()


class SweepWavelengthTask(Task):
    def __init__(self, parent, page: SweepWavelength) -> None:
        '''
        spinbox_sweep_start_wavelength, spinbox_sweep_end_wavelength,
                 spinbox_sweep_step_size, set_wavelength_task, set_angle_task, read_power_task,
                 set_actuator_position_task, turn_on_power_reading
        '''
        super().__init__(parent)
        self.page = page
        self.start_wavelength = float(
            VARIABLES.var_spinbox_sweep_start_wavelength.get())
        self.end_wavelength = float(
            VARIABLES.var_spinbox_sweep_end_wavelength.get())
        self.curr_wavelength = self.start_wavelength
        self.on_off_widgets = [self.page.spinbox_target_wavelength,
                               self.page.button_set_wavelength,
                               self.page.spinbox_target_angle,
                               self.page.button_set_angle,
                               self.page.spinbox_target_actuator_position,
                               self.page.button_set_actuator_position,
                               self.page.spinbox_sweep_start_wavelength,
                               self.page.spinbox_sweep_end_wavelength,
                               self.page.spinbox_sweep_step_size,
                               self.page.button_power,
                               self.page.spinbox_target_power,
                               self.page.spinbox_sweep_lifetime_num,
                               self.page.spinbox_sweep_actuator_explore_range,
                               self.page.spinbox_sweep_oscilloscope_wait_time,
                               ]

    def task(self):
        VARIABLES.var_spinbox_target_wavelength.set(self.curr_wavelength)
        self.page.set_wavelength_task.task_loop()
        VARIABLES.var_spinbox_target_angle.set(0)
        self.page.set_angle_task.task_loop()
        self.find_max_power_by_actuator()
        self.find_target_power_by_ndfilter()
        self.measure_lifetime()
        self.curr_wavelength += float(
            VARIABLES.var_spinbox_sweep_step_size.get())

    def find_max_power_by_actuator(self):
        actuator_explore_range = float(
            VARIABLES.var_spinbox_sweep_actuator_explore_range.get())
        curr_actuator_position = float(
            VARIABLES.var_entry_curr_actuator_position.get())
        max_power = 0
        max_power_actuator_position = 0
        actuator_limit = 12
        actuator_explore_step = 0.1
        for actuator_position in np.arange(max(curr_actuator_position - actuator_explore_range, 0),
                                           min(curr_actuator_position +
                                               actuator_explore_range, actuator_limit)
                                           + actuator_explore_step, actuator_explore_step):
            actuator_position = round(actuator_position, 4)
            VARIABLES.var_spinbox_target_actuator_position.set(
                actuator_position)
            self.page.set_actuator_position_task.task_loop()
            sleep(0.5)  # wait for var_entry_curr_power to update
            power = float(VARIABLES.var_entry_curr_power.get())
            if power > max_power:
                max_power = power
                max_power_actuator_position = actuator_position
        VARIABLES.var_spinbox_target_actuator_position.set(
            max_power_actuator_position)
        self.page.set_actuator_position_task.task_loop()

    def find_target_power_by_ndfilter(self):
        curr_power = float(VARIABLES.var_entry_curr_power.get())
        target_power = float(VARIABLES.var_spinbox_sweep_target_power.get())
        if curr_power < target_power:
            LOGGER.log(
                "[Sweep Paused] Current max power is lower than target power. Please adjust actuator position to reach large enough max power before resuming.")
            if self.status == RUNNING:
                self.pause()
        else:
            while abs(target_power - curr_power) > 0.1:
                delta = -0.5 * (target_power - curr_power)
                curr_ndfilter_position = float(
                    VARIABLES.var_entry_curr_angle.get())
                VARIABLES.var_spinbox_target_angle.set(
                    round(curr_ndfilter_position + delta, 4))
                self.page.set_angle_task.task_loop()
                sleep(0.5)  # wait for var_entry_curr_power to update
                curr_power = float(VARIABLES.var_entry_curr_power.get())
    
    def measure_lifetime(self):
        pass
        # num = int(VARIABLES.var_spinbox_sweep_lifetime_num.get())
        # wait_time = float(VARIABLES.var_spinbox_sweep_oscilloscope_wait_time.get())
        # for _ in range(num):
        #     self.X, curr_data_ch1, curr_data_ch2 = INSTANCES.oscilloscope.get_data(wait_time)
        #     sleep(0.5)
        # self.page.turn_off_power_reading()
        # Also TODO: disable start button when changing angle/wavelength/actuator position, etc


    def start(self):
        if not INSTANCES.oscilloscope.valid or not INSTANCES.monochromator.valid or not INSTANCES.ndfilter.valid \
                or not INSTANCES.actuator.valid or not INSTANCES.powermeter.valid:
            LOGGER.log(
                "Not all devices are connected! Please connect all devices in Device Manager page before starting a sweep.")
            return
        for widget in self.on_off_widgets:
            widget.config(state="disabled")
        self.page.set_wavelength_task.external_button_control = True
        self.page.set_angle_task.external_button_control = True
        self.page.set_actuator_position_task.external_button_control = True
        if not self.page.read_power_task.is_running:
            self.page.turn_on_power_reading()
        self.num = int(float(VARIABLES.var_spinbox_sweep_end_wavelength.get()) - float(
            VARIABLES.var_spinbox_sweep_start_wavelength.get())) / float(VARIABLES.var_spinbox_sweep_step_size.get())
        super().start()
    
    def paused(self):
        super().paused()
        for widget in self.on_off_widgets:
            widget.config(state="normal")

    def reset(self):
        super().reset()
        for widget in self.on_off_widgets:
            widget.config(state="normal")
