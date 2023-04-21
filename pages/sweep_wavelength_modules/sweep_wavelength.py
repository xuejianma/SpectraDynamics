from threading import Thread
from utils.config import VARIABLES, INSTANCES, LOGGER, UTILS
from utils.task import Task, RUNNING, PAUSED
from time import sleep
import numpy as np

class SweepWavelengthTask(Task):
    def __init__(self, parent, page) -> None:
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
        self.find_background_power()
        self.find_max_power_by_actuator()
        self.find_target_power_by_ndfilter()
        self.measure_lifetime()
        if self.check_stopping():
            return
        if not self.check_devices_valid():
            LOGGER.log(
                f"[Sweeping - {VARIABLES.var_entry_curr_wavelength.get()} nm] Invalid device(s).")
            self.pause()
            UTILS.push_notification("Paused due to invalid device(s).")
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

    def find_background_power(self):
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
        if float(VARIABLES.var_spinbox_background_power.get()) > 0.1:
            LOGGER.log(
                f"[Sweeping - {VARIABLES.var_entry_curr_wavelength.get()} nm] Background power is too large.")
            self.pause()
            UTILS.push_notification("Paused due to large background power.")
            return
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
        curr_power = float(VARIABLES.var_entry_curr_power.get())
        target_power = float(VARIABLES.var_spinbox_sweep_target_power.get())
        if VARIABLES.var_checkbutton_photon_flux_fixed.get():
            target_power = target_power * float(VARIABLES.var_spinbox_wavelength_at_target_power.get()) / self.curr_wavelength
        if curr_power < target_power:
            LOGGER.log(
                "[Sweep Paused] Current max power is lower than target power. Please adjust actuator position to reach large enough max power before resuming.")
            if self.status == RUNNING:
                self.pause()
                UTILS.push_notification("Paused due to low max power.")
        else:
            LOGGER.log(
                f"[Sweeping - {VARIABLES.var_entry_curr_wavelength.get()} nm] Finding target power {round(target_power, 6)}uW by NDFilter. Background power is {round(float(VARIABLES.var_spinbox_background_power.get()), 6)}uW.")
            delta = float('inf')
            while abs(target_power - curr_power) > 0.005 * target_power and abs(delta) > 0.005:
                if self.check_stopping():
                    return
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
        if not self.page.save_oscilloscope.data_dict["header"]:
            self.page.save_oscilloscope.data_dict["header"].append("time(s)")
            self.page.save_oscilloscope.data_dict["data"].append(X)
        self.page.save_oscilloscope.data_dict["header"].append(
            f"{self.curr_wavelength}nm_ch1")
        self.page.save_oscilloscope.data_dict["data"].append(data_ch1)
        self.page.save_oscilloscope.data_dict["header"].append(
            f"{self.curr_wavelength}nm_ch2")
        self.page.save_oscilloscope.data_dict["data"].append(data_ch2)
        self.page.save_oscilloscope.save(update_datetime=False)

    def check_devices_valid(self):
        return INSTANCES.oscilloscope.valid and INSTANCES.monochromator.valid and INSTANCES.actuator.valid \
            and INSTANCES.ndfilter.valid and INSTANCES.powermeter.valid

    def start(self):
        if not self.check_devices_valid():
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
            self.page.save_oscilloscope.update_datetime()
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
        self.page.save_oscilloscope.reset()
        LOGGER.reset()

    def after_complete(self):
        super().after_complete()
        UTILS.push_notification("Sweep completed!")
