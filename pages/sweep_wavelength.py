from tkinter import ttk
from utils.config import INSTANCES, VARIABLES, LOGGER, UTILS
from utils.spinbox import Spinbox
from utils.plot import Plot
from utils.task import Task, RUNNING, PAUSED, PAUSING, TERMINATING
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
        self.home_actuator_task = HomeActuatorTask(self.button_home_actuator)
        self.save = Save(frame_1_7, VARIABLES.var_entry_sweep_wavelength_directory,
                         VARIABLES.var_entry_sweep_wavelength_filename,
                         substitute_dict={})
        SweepWavelengthTask(frame_1_7, self)
        self.on_change_for_photon_flux_fixed()

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
        self.spinbox_target_wavelength = Spinbox(frame_1_1, from_=0, to=float("inf"),
                                                 textvariable=VARIABLES.var_spinbox_target_wavelength)
        self.spinbox_target_wavelength.pack(side="top", anchor="w")
        self.button_set_wavelength = ttk.Button(
            frame_1_1, text="Set Wavelength", command=self.on_set_wavelength)
        self.button_set_wavelength.pack(side="top", anchor="w")
        ttk.Label(frame_1_2, text="Actuator Position (mm): ").pack(
            side="top", anchor="w")
        ttk.Entry(frame_1_2, state="readonly", textvariable=VARIABLES.var_entry_curr_actuator_position).pack(
            side="top", anchor="w")
        ttk.Label(frame_1_2, text="Target Actuator Position (mm): ").pack(
            side="top", anchor="w")
        self.spinbox_target_actuator_position = Spinbox(frame_1_2, from_=0, to=float("inf"), increment=0.01,
                                                        textvariable=VARIABLES.var_spinbox_target_actuator_position)
        self.spinbox_target_actuator_position.pack(side="top", anchor="w")
        self.button_set_actuator_position = ttk.Button(
            frame_1_2, text="Set Position", command=self.on_set_actuator_position)
        self.button_set_actuator_position.pack(side="top", anchor="w")
        self.button_home_actuator = ttk.Button(
            frame_1_2, text="Home", command=self.on_home_actuator)
        self.button_home_actuator.pack(side="top", anchor="w")
        ttk.Label(frame_1_3, text="Current NDFilter Angle (deg): ").pack(
            side="top", anchor="w")
        ttk.Entry(frame_1_3, state="readonly", textvariable=VARIABLES.var_entry_curr_angle).pack(
            side="top", anchor="w")
        ttk.Label(frame_1_3, text="Target Angle (deg): ").pack(
            side="top", anchor="w")
        self.spinbox_target_angle = Spinbox(frame_1_3, from_=0, to=360, increment=0.1,
                                            textvariable=VARIABLES.var_spinbox_target_angle)
        self.spinbox_target_angle.pack(side="top", anchor="w")
        self.button_set_angle = ttk.Button(
            frame_1_3, text="Set Angle", command=self.on_set_angle)
        self.button_set_angle.pack(side="top", anchor="w")
        ttk.Label(frame_1_3, text="Note: Make sure power decreases\nwith NDFilter angle.",
                  font="TkDefaultFont 8").pack(side="top", anchor="w")
        ttk.Label(frame_1_3, text="NDFilter Spin Relative Speed (default 1.0)").pack(
            side="top", anchor="w")
        Spinbox(frame_1_3, from_=0, to=float("inf"), increment=1,
                textvariable=VARIABLES.var_spinbox_ndfilter_speed).pack(side="top", anchor="w")
        ttk.Label(frame_1_4, text="Sweep Start Wavelength (nm): ").pack(
            side="top", anchor="w")
        self.spinbox_sweep_start_wavelength = Spinbox(frame_1_4, from_=0, to=float(
            "inf"), increment=0.1, textvariable=VARIABLES.var_spinbox_sweep_start_wavelength)
        self.spinbox_sweep_start_wavelength.pack(side="top", anchor="w")
        VARIABLES.var_spinbox_sweep_start_wavelength.trace_add("write", lambda val, index, mode: self.on_change_for_photon_flux_fixed())
        ttk.Label(frame_1_4, text="Sweep End Wavelength (nm): ").pack(
            side="top", anchor="w")
        self.spinbox_sweep_end_wavelength = Spinbox(frame_1_4, from_=0, to=float(
            "inf"), increment=0.1, textvariable=VARIABLES.var_spinbox_sweep_end_wavelength)
        self.spinbox_sweep_end_wavelength.pack(side="top", anchor="w")
        VARIABLES.var_spinbox_sweep_end_wavelength.trace_add("write", lambda val, index, mode: self.on_change_for_photon_flux_fixed())
        ttk.Label(frame_1_4, text="Sweep Step Size (nm): ").pack(
            side="top", anchor="w")
        self.spinbox_sweep_step_size = Spinbox(frame_1_4, from_=0, to=float(
            "inf"), textvariable=VARIABLES.var_spinbox_sweep_step_size)
        self.spinbox_sweep_step_size.pack(side="top", anchor="w")
        self.checkbutton_photon_flux_fixed = ttk.Checkbutton(
            frame_1_4, text="Photon Flux Fixed\n(instead of power fixed)", variable=VARIABLES.var_checkbutton_photon_flux_fixed)
        self.checkbutton_photon_flux_fixed.pack(side="top", anchor="w")
        VARIABLES.var_checkbutton_photon_flux_fixed.trace_add("write", lambda val, index, mode: self.on_change_for_photon_flux_fixed())
        self.label_photon_flux_fixed = ttk.Label(frame_1_4, text="\n\n")
        self.label_photon_flux_fixed.pack(side="top", anchor="w")
        ttk.Label(frame_1_5, text="Current Power (rel. uW): ").pack(
            side="top", anchor="w")
        ttk.Entry(frame_1_5, state="readonly", textvariable=VARIABLES.var_entry_curr_power).pack(
            side="top", anchor="w")
        self.button_power = ttk.Button(
            frame_1_5, text="Turn ON", command=self.toggle_power_reading)
        self.button_power.pack(side="top", anchor="w")
        self.button_set_background_power = ttk.Button(
            frame_1_5, text="Set As Background Power", command=UTILS.set_background_power)
        self.button_set_background_power.pack(side="top", anchor="w")
        ttk.Label(frame_1_5, text="Background Power (uW):").pack(
            side="top", anchor="w")
        self.spinbox_background_power = Spinbox(frame_1_5, from_=0, to=float(
            "inf"), increment=0.1, textvariable=VARIABLES.var_spinbox_background_power)
        self.spinbox_background_power.pack(side="top", anchor="w")
        ttk.Label(frame_1_5, text="Target Power (uW): ").pack(
            side="top", anchor="w")
        self.spinbox_target_power = Spinbox(frame_1_5, from_=0, to=float("inf"), increment=0.1,
                                            textvariable=VARIABLES.var_spinbox_sweep_target_power)
        self.spinbox_target_power.pack(side="top", anchor="w")
        VARIABLES.var_spinbox_sweep_target_power.trace_add("write", lambda val, index, mode: self.on_change_for_photon_flux_fixed())
        ttk.Label(frame_1_5, text="Wavelength at target power (nm)\n(for fixed photon flux mode)").pack(side="top", anchor="w")
        self.spinbox_wavelength_at_target_power = Spinbox(frame_1_5, from_=0, to=float("inf"), increment=0.1,
                textvariable=VARIABLES.var_spinbox_wavelength_at_target_power)
        self.spinbox_wavelength_at_target_power.pack(side="top", anchor="w")
        VARIABLES.var_spinbox_wavelength_at_target_power.trace_add("write", lambda val, index, mode: self.on_change_for_photon_flux_fixed())
        self.label_oscilloscope_wait_time = ttk.Label(
            frame_1_6, text="Oscilloscope wait time (s): ")
        self.label_oscilloscope_wait_time.pack(side="top", anchor="w")
        self.spinbox_sweep_oscilloscope_wait_time = Spinbox(frame_1_6, from_=0, to=float(
            "inf"), textvariable=VARIABLES.var_spinbox_sweep_lifetime_wait_time)
        self.spinbox_sweep_oscilloscope_wait_time.pack(side="top", anchor="w")
        ttk.Label(frame_1_6, text="Number of measurements\nper wavelength").pack(
            side="top", anchor="w")
        self.spinbox_sweep_lifetime_num = Spinbox(frame_1_6, from_=0, to=float(
            "inf"), textvariable=VARIABLES.var_spinbox_sweep_lifetime_num)
        self.spinbox_sweep_lifetime_num.pack(side="top", anchor="w")
        ttk.Label(frame_1_6, text="Actuator explore range\nfor max power (∓mm, Δ)").pack(
            side="top", anchor="w")
        self.spinbox_sweep_actuator_explore_range_negative = Spinbox(frame_1_6, from_=-float("inf"), to=0, increment=0.01, width=5,
                                                                     textvariable=VARIABLES.var_spinbox_sweep_actuator_explore_range_negative)
        self.spinbox_sweep_actuator_explore_range_negative.pack(side="left")
        self.spinbox_sweep_actuator_explore_range_positive = Spinbox(frame_1_6, from_=0, to=float("inf"), increment=0.01, width=5,
                                                                     textvariable=VARIABLES.var_spinbox_sweep_actuator_explore_range_positive)
        self.spinbox_sweep_actuator_explore_range_positive.pack(side="left")
        self.spinbox_sweep_actuator_explore_range_step_size = Spinbox(frame_1_6, from_=0, to=float("inf"), increment=0.01, width=5,
                                                                      textvariable=VARIABLES.var_spinbox_sweep_actuator_explore_range_step_size)
        self.spinbox_sweep_actuator_explore_range_step_size.pack(side="left")
        ttk.Label(frame_2_1, text="Ch1 Instant (V-s)").pack(side="top")
        self.plot_lifetime_instant_ch1 = Plot(frame_2_1)
        ttk.Label(frame_2_2, text="Ch1 Average (V-s)").pack(side="top")
        self.plot_lifetime_average_ch1 = Plot(frame_2_2)
        ttk.Label(frame_3_1, text="Ch2 Instant (V-s)").pack(side="top")
        self.plot_lifetime_instant_ch2 = Plot(frame_3_1)
        ttk.Label(frame_3_2, text="Ch2 Average (V-s)").pack(side="top")
        self.plot_lifetime_average_ch2 = Plot(frame_3_2)
        return frame, frame_1_7

    def toggle_power_reading(self):
        if self.read_power_task.is_running:
            self.turn_off_power_reading()
        else:
            self.turn_on_power_reading()
    
    def on_change_for_photon_flux_fixed(self):
        if VARIABLES.var_checkbutton_photon_flux_fixed.get():
            self.spinbox_wavelength_at_target_power.config(state="normal")
            target_wavelength = float(VARIABLES.var_spinbox_wavelength_at_target_power.get())
            start_wavelength = float(VARIABLES.var_spinbox_sweep_start_wavelength.get())
            end_wavelength = float(VARIABLES.var_spinbox_sweep_end_wavelength.get())
            target_power = round(float(VARIABLES.var_spinbox_sweep_target_power.get()), 6)
            start_power = round(target_power * target_wavelength / start_wavelength, 6)
            end_power = round(target_power * target_wavelength / end_wavelength, 6)
            pair_to_display = []
            pair_to_display.append((start_wavelength, start_power))
            if (target_wavelength, target_power) not in pair_to_display:
                pair_to_display.append((target_wavelength, target_power))
            if (end_wavelength, end_power) not in pair_to_display:
                pair_to_display.append((end_wavelength, end_power))
            pair_to_display.sort(key=lambda x: x[0])
            text_to_display = ""
            for pair in pair_to_display:
                text_to_display += str(pair[0]) + "nm: " + str(pair[1]) + "uW\n"
            if len(pair_to_display) == 1:
                text_to_display += "\n\n"
            elif len(pair_to_display) == 2:
                text_to_display += "\n"
            self.label_photon_flux_fixed.config(text=text_to_display[:-1])
        else:
            self.spinbox_wavelength_at_target_power.config(state="disabled")
            self.label_photon_flux_fixed.config(text="\n\n")

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

    def on_home_actuator(self):
        self.home_actuator_task.start()


class SetAngleTask():
    def __init__(self, button_set_angle) -> None:
        self.is_running = False
        self.button_set_angle = button_set_angle
        self.external_button_control = False

    def task_loop(self):
        if not self.external_button_control:
            self.button_set_angle.config(state="disabled")
        try:
            INSTANCES.ndfilter.set_angle(
                float(VARIABLES.var_spinbox_target_angle.get()))
            VARIABLES.var_entry_curr_angle.set(
                round(INSTANCES.ndfilter.get_angle(), 6))
        except Exception as e:
            LOGGER.log(e)
            raise e
        finally:
            if not self.external_button_control:
                self.button_set_angle.config(state="normal")
            self.is_running = False

    def start(self):
        self.is_running = True
        thread = Thread(target=self.task_loop)
        thread.setDaemon(True)
        thread.start()


class ReadPowerTask():
    def __init__(self, button_power) -> None:
        self.is_running = False
        self.button_power = button_power

    def task_loop(self):
        try:
            count = 0
            max_try = 10
            error = None
            # sometimes the powermeter will have VisaIOError and rerunning the command will fix it.
            while count < max_try:
                try:
                    while self.is_running:
                        power = INSTANCES.powermeter.get_power_uW()
                        background_power = float(
                            VARIABLES.var_spinbox_background_power.get())
                        VARIABLES.var_entry_curr_power.set(
                            round(power - background_power, 6))
                    break
                except Exception as e:
                    LOGGER.log(e)
                    count += 1
                    error = e
                    sleep(0.1)
            if count == max_try:
                raise error
        except Exception as e:
            LOGGER.log(e)
            raise e
        finally:
            if self.button_power["text"] == "Turn OFF":
                self.button_power["text"] = "Turn ON"
            self.button_power.config(state="normal")
            # Set is_running to False here in case the stopping comes from error and self.terminate() is not called.
            self.is_running = False

    def start(self):
        self.is_running = True
        thread = Thread(target=self.task_loop)
        thread.setDaemon(True)
        thread.start()

    def terminate(self):
        self.is_running = False


class SetWavelengthTask():
    def __init__(self, button_set_wavelength) -> None:
        self.is_running = False
        self.button_set_wavelength = button_set_wavelength
        self.external_button_control = False

    def task_loop(self):
        if not self.external_button_control:
            self.button_set_wavelength.config(state="disabled")
        try:
            INSTANCES.powermeter.set_wavelength(
                float(VARIABLES.var_spinbox_target_wavelength.get()))
        except Exception as e:
            LOGGER.log(e)
            raise e
        finally:
            if not self.external_button_control:
                self.button_set_wavelength.config(state="normal")
            self.is_running = False
        try:
            INSTANCES.monochromator.set_wavelength(
                float(VARIABLES.var_spinbox_target_wavelength.get()))
            VARIABLES.var_entry_curr_wavelength.set(
                round(INSTANCES.monochromator.get_wavelength(), 6))
        except Exception as e:
            LOGGER.log(e)
            raise e
        finally:
            if not self.external_button_control:
                self.button_set_wavelength.config(state="normal")
            self.is_running = False

    def start(self):
        self.is_running = True
        thread = Thread(target=self.task_loop)
        thread.setDaemon(True)
        thread.start()


class SetActuatorPositionTask():
    def __init__(self, button_set_actuator_position) -> None:
        self.is_running = False
        self.button_set_actuator_position = button_set_actuator_position
        self.external_button_control = False

    def task_loop(self):
        if not self.external_button_control:
            self.button_set_actuator_position.config(state="disabled")
        try:
            INSTANCES.actuator.set_position(
                float(VARIABLES.var_spinbox_target_actuator_position.get()))
            VARIABLES.var_entry_curr_actuator_position.set(
                round(INSTANCES.actuator.get_position(), 6))
        except Exception as e:
            LOGGER.log(e)
            raise e
        finally:
            if not self.external_button_control:
                self.button_set_actuator_position.config(state="normal")
            self.is_running = False

    def start(self):
        self.is_running = True
        thread = Thread(target=self.task_loop)
        thread.setDaemon(True)
        thread.start()


class HomeActuatorTask():
    def __init__(self, button_home_actuator) -> None:
        self.is_running = False
        self.button_home_actuator = button_home_actuator
        self.external_button_control = False

    def task_loop(self):
        if not self.external_button_control:
            self.button_home_actuator.config(state="disabled")
        try:
            INSTANCES.actuator.home()
            VARIABLES.var_entry_curr_actuator_position.set(
                round(INSTANCES.actuator.get_position(), 6))
        except Exception as e:
            LOGGER.log(e)
            raise e
        finally:
            if not self.external_button_control:
                self.button_home_actuator.config(state="normal")
            self.is_running = False

    def start(self):
        self.is_running = True
        thread = Thread(target=self.task_loop)
        thread.setDaemon(True)
        thread.start()


class SweepWavelengthTask(Task):
    def __init__(self, parent, page: SweepWavelength) -> None:
        super().__init__(parent)
        self.page = page
        self.on_off_widgets = [self.page.spinbox_target_wavelength,
                               self.page.button_set_wavelength,
                               self.page.spinbox_target_actuator_position,
                               self.page.button_set_actuator_position,
                               self.page.button_home_actuator,
                               self.page.spinbox_target_angle,
                               self.page.button_set_angle,
                               self.page.spinbox_sweep_start_wavelength,
                               self.page.spinbox_sweep_end_wavelength,
                               self.page.spinbox_sweep_step_size,
                               self.page.checkbutton_photon_flux_fixed,
                               self.page.button_power,
                               self.page.button_set_background_power,
                               self.page.spinbox_target_power,
                               self.page.spinbox_wavelength_at_target_power,
                               self.page.spinbox_sweep_lifetime_num,
                               self.page.spinbox_sweep_actuator_explore_range_negative,
                               self.page.spinbox_sweep_actuator_explore_range_positive,
                               self.page.spinbox_sweep_actuator_explore_range_step_size,
                               self.page.spinbox_background_power,
                               ]
        self.external_button_control_list = [
            self.page.set_wavelength_task,
            self.page.set_angle_task,
            self.page.set_actuator_position_task,
            self.page.home_actuator_task,
        ]

    def task(self):
        VARIABLES.var_spinbox_target_wavelength.set(self.curr_wavelength)
        self.page.set_wavelength_task.task_loop()
        VARIABLES.var_spinbox_target_angle.set(0)
        self.page.set_angle_task.task_loop()
        self.find_backgrond_power()
        self.find_max_power_by_actuator()
        self.find_target_power_by_ndfilter()
        self.measure_lifetime()
        if self.check_stopping():
            return
        if float(VARIABLES.var_spinbox_sweep_start_wavelength.get()) <= float(VARIABLES.var_spinbox_sweep_end_wavelength.get()):
            self.curr_wavelength += float(
                VARIABLES.var_spinbox_sweep_step_size.get())
        else:
            self.curr_wavelength -= float(
                VARIABLES.var_spinbox_sweep_step_size.get())
        self.curr_wavelength = round(self.curr_wavelength, 6)

    def task_loop(self):
        try:
            super().task_loop()
        except Exception as e:
            LOGGER.log(e)
            self.reset()
            raise e

    def find_backgrond_power(self):
        if self.check_stopping():
            return
        LOGGER.log(
            f"[Sweeping - {VARIABLES.var_entry_curr_wavelength.get()} nm] Finding background power...")
        curr_actuator_position = float(
            VARIABLES.var_entry_curr_actuator_position.get())
        # move actuator to a misaligned position to find background power
        if curr_actuator_position >= 6:
            VARIABLES.var_spinbox_target_actuator_position.set(
                round(curr_actuator_position - 6, 6))
        else:
            VARIABLES.var_spinbox_target_actuator_position.set(
                round(curr_actuator_position + 6, 6))
        self.page.set_actuator_position_task.task_loop()
        # wait for var_entry_curr_power to update before getting power
        sleep(INSTANCES.powermeter.max_period + 0.2)
        UTILS.set_background_power()
        VARIABLES.var_spinbox_target_actuator_position.set(
            round(curr_actuator_position, 6))
        self.page.set_actuator_position_task.task_loop()

    def find_max_power_by_actuator(self):
        if self.check_stopping():
            return
        LOGGER.log(
            f"[Sweeping - {VARIABLES.var_entry_curr_wavelength.get()} nm] Finding max power by actuator...")
        actuator_explore_range_negative = float(
            VARIABLES.var_spinbox_sweep_actuator_explore_range_negative.get())
        actuator_explore_range_positive = float(
            VARIABLES.var_spinbox_sweep_actuator_explore_range_positive.get())
        actuator_explore_range_step_size = float(
            VARIABLES.var_spinbox_sweep_actuator_explore_range_step_size.get())
        curr_actuator_position = float(
            VARIABLES.var_entry_curr_actuator_position.get())
        max_power = 0
        max_power_actuator_position = 0
        actuator_limit = 12
        for actuator_position in np.arange(max(curr_actuator_position + actuator_explore_range_negative, 0),
                                           min(curr_actuator_position +
                                               actuator_explore_range_positive, actuator_limit)
                                           + actuator_explore_range_step_size, actuator_explore_range_step_size):
            if self.check_stopping():
                return
            actuator_position = round(actuator_position, 6)
            VARIABLES.var_spinbox_target_actuator_position.set(
                actuator_position)
            self.page.set_actuator_position_task.task_loop()
            # wait for var_entry_curr_power to update before getting power
            sleep(INSTANCES.powermeter.max_period + 0.2)
            power = float(VARIABLES.var_entry_curr_power.get())
            if power > max_power:
                max_power = power
                max_power_actuator_position = actuator_position
        VARIABLES.var_spinbox_target_actuator_position.set(
            max_power_actuator_position)
        self.page.set_actuator_position_task.task_loop()
        # wait for var_entry_curr_power to update before getting power in find_target_power_by_ndfilter
        sleep(INSTANCES.powermeter.max_period + 0.2)

    def find_target_power_by_ndfilter(self):
        if self.check_stopping():
            return
        LOGGER.log(
            f"[Sweeping - {VARIABLES.var_entry_curr_wavelength.get()} nm] Finding target power by NDFilter...")
        curr_power = float(VARIABLES.var_entry_curr_power.get())
        target_power = float(VARIABLES.var_spinbox_sweep_target_power.get())
        if VARIABLES.var_checkbutton_photon_flux_fixed.get():
            target_power = target_power * float(VARIABLES.var_spinbox_wavelength_at_target_power.get()) / self.curr_wavelength
        if curr_power < target_power:
            LOGGER.log(
                "[Sweep Paused] Current max power is lower than target power. Please adjust actuator position to reach large enough max power before resuming.")
            if self.status == RUNNING:
                self.pause()
        else:
            LOGGER.log(
                "[Sweeping] Finding target power {}uW by NDFilter..".format(round(target_power, 6)))
            delta = float('inf')
            while abs(target_power - curr_power) > 0.005 * target_power and abs(delta) > 0.005:
                if self.check_stopping():
                    return
                delta = -0.5 * (target_power - curr_power) / curr_power * 10
                delta = -0.5 * (target_power - curr_power) / curr_power * 10 * float(VARIABLES.var_spinbox_ndfilter_speed.get())
                curr_ndfilter_position = float(
                    VARIABLES.var_entry_curr_angle.get())
                VARIABLES.var_spinbox_target_angle.set(
                    round(curr_ndfilter_position + delta, 6))
                self.page.set_angle_task.task_loop()
                # wait for var_entry_curr_power to update
                sleep(INSTANCES.powermeter.max_period + 0.2)
                curr_power = float(VARIABLES.var_entry_curr_power.get())

    def measure_lifetime(self):
        if self.check_stopping():
            return
        num = int(VARIABLES.var_spinbox_sweep_lifetime_num.get())
        X = None
        data_ch1 = None
        data_ch2 = None
        for i in range(num):
            if self.check_stopping():
                return
            LOGGER.log(
                f"[Sweeping - {VARIABLES.var_entry_curr_wavelength.get()} nm] Measuring lifetime, round %d/%d..." % (i + 1, num))
            wait_time = float(
                VARIABLES.var_spinbox_sweep_lifetime_wait_time.get())
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
            plot_thread = Thread(target=plot)
            plot_thread.setDaemon(True)
            plot_thread.start()
        self.save_data(X, data_ch1, data_ch2)

    def save_data(self, X, data_ch1, data_ch2):
        if self.check_stopping():
            return
        if not self.page.save.data_dict["header"]:
            self.page.save.data_dict["header"].append("time(s)")
            self.page.save.data_dict["data"].append(X)
        self.page.save.data_dict["header"].append(
            f"{self.curr_wavelength}nm_ch1")
        self.page.save.data_dict["data"].append(data_ch1)
        self.page.save.data_dict["header"].append(
            f"{self.curr_wavelength}nm_ch2")
        self.page.save.data_dict["data"].append(data_ch2)
        self.page.save.save(update_datetime=False)

    def start(self):
        if not INSTANCES.oscilloscope.valid or not INSTANCES.monochromator.valid or not INSTANCES.actuator.valid \
                or not INSTANCES.ndfilter.valid or not INSTANCES.powermeter.valid:
            LOGGER.log(
                "Not all devices are connected! Please connect all devices in Device Manager page before starting a sweep.")
            return
        if self.page.set_wavelength_task.is_running:
            LOGGER.log(
                "Please wait for the monochromator to finish setting wavelength before starting a sweep.")
            return
        if self.page.set_actuator_position_task.is_running:
            LOGGER.log(
                "Please wait for the actuator to finish setting position before starting a sweep.")
            return
        if self.page.set_angle_task.is_running:
            LOGGER.log(
                "Please wait for the NDFilter to finish setting angle before starting a sweep.")
            return
        if self.page.home_actuator_task.is_running:
            LOGGER.log(
                "Please wait for the actuator to finish homing before starting a sweep.")
            return
        for widget in self.on_off_widgets:
            widget.config(state="disabled")
        for external_button_control in self.external_button_control_list:
            external_button_control.external_button_control = True
        if not self.page.read_power_task.is_running:
            self.page.turn_on_power_reading()
        self.num = int(abs(float(VARIABLES.var_spinbox_sweep_end_wavelength.get()) - float(
            VARIABLES.var_spinbox_sweep_start_wavelength.get()))) / float(VARIABLES.var_spinbox_sweep_step_size.get()) + 1
        if self.status != PAUSED:
            self.curr_wavelength = float(
                VARIABLES.var_spinbox_sweep_start_wavelength.get())
            self.page.save.update_datetime()
        super().start()

    def paused(self):
        super().paused()
        for widget in self.on_off_widgets:
            widget.config(state="normal")
        for external_button_control in self.external_button_control_list:
            external_button_control.external_button_control = False

    def reset(self):
        super().reset()
        VARIABLES.var_spinbox_target_angle.set(0)
        self.page.set_angle_task.task_loop()
        for widget in self.on_off_widgets:
            widget.config(state="normal")
        for external_button_control in self.external_button_control_list:
            external_button_control.external_button_control = False
        self.page.save.reset()
        LOGGER.reset()
