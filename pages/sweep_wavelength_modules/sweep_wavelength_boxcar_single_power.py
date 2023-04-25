from threading import Thread
from utils.config import VARIABLES, INSTANCES, LOGGER, UTILS
from utils.task import Task, RUNNING, PAUSED
from equipments.powermeter import MAX_PERIOD
# from pages.sweep_wavelength import SweepWavelength
from time import sleep, time
import numpy as np
import csv
from scipy.interpolate import interp1d


class SweepWavelengthBoxcarSinglePowerTask(Task):
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
        self.calibrate_func = None
        self.wavelength_list = []
        self.ch1_list = []

    def task(self):
        VARIABLES.var_spinbox_target_wavelength.set(self.curr_wavelength)
        self.page.set_wavelength_task.task_loop()
        VARIABLES.var_spinbox_target_actuator_position.set(
            self.calibrate_func(self.curr_wavelength))
        LOGGER.log(
            f"[Sweeping - {VARIABLES.var_entry_curr_wavelength.get()} nm] Go to pre-calibrated actuator position.")
        self.page.set_actuator_position_task.task_loop()
        sleep(MAX_PERIOD*2)
        curr_power = float(VARIABLES.var_entry_curr_power.get())
        curr_angle = float(VARIABLES.var_entry_curr_angle.get())
        angle_offset = float(VARIABLES.var_spinbox_boxcar_single_power_ndfilter_offset_angle.get())
        max_power = self.predict_max_power(curr_power, curr_angle, angle_offset)
        target_power = float(VARIABLES.var_spinbox_sweep_target_power.get())
        if  max_power < target_power:
            LOGGER.log(
                "[Sweep Paused] Current max power is lower than target power. Please adjust actuator position to reach large enough max power before resuming.")
            if self.status == RUNNING:
                self.pause()
                UTILS.push_notification("Paused due to low max power.")
            return
        target_angle = round(self.predict_angle(target_power, max_power, angle_offset), 6)
        VARIABLES.var_spinbox_target_angle.set(target_angle)
        LOGGER.log(
            f"[Sweeping - {VARIABLES.var_entry_curr_wavelength.get()} nm] Going to predicted angle {target_angle} deg.")
        self.page.set_angle_task.task_loop()
        LOGGER.log(
            f"[Sweeping - {VARIABLES.var_entry_curr_wavelength.get()} nm] Finding accurate target angle.")
        self.find_target_power_by_ndfilter()
        num_of_acquisitions = int(VARIABLES.var_spinbox_boxcar_single_power_number_of_data_acquisitions.get())
        time_interval = float(VARIABLES.var_spinbox_boxcar_single_power_time_interval.get())
        boxcar_ch1_voltage_sum = 0.0
        LOGGER.log(
                f"[Sweeping - {VARIABLES.var_entry_curr_wavelength.get()} nm] Acquiring data.")
        for _ in range(num_of_acquisitions):
            if self.check_stopping():
                return
            boxcar_ch1_voltage_sum += float(INSTANCES.boxcar.get_voltage())
            sleep(time_interval)
        if self.check_stopping():
            return
        self.wavelength_list.append(self.curr_wavelength)
        self.ch1_list.append(boxcar_ch1_voltage_sum / num_of_acquisitions)
        self.page.plot_boxcar_single_power.plot(self.wavelength_list, self.ch1_list)
        self.save_data(self.wavelength_list, self.ch1_list)
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
            UTILS.push_notification("Error: " + str(e))
            raise e

    def save_data(self, wavelength_list, ch1_list):
        if self.check_stopping():
            return
        if not self.page.save_boxcar_single_power.data_dict["header"]:
            self.page.save_boxcar_single_power.data_dict["header"].append("wavelength")
            self.page.save_boxcar_single_power.data_dict["header"].append("ch1")
        self.page.save_boxcar_single_power.data_dict["data"] = [wavelength_list, ch1_list]
        self.page.save_boxcar_single_power.save(update_datetime=False)

    def check_devices_valid(self):
        return INSTANCES.monochromator.valid and INSTANCES.actuator.valid \
            and INSTANCES.ndfilter.valid and INSTANCES.powermeter.valid and INSTANCES.boxcar.valid

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
            self.page.save_boxcar_single_power.update_datetime()
        if not self.calibrate_func:
            calibrate_file = VARIABLES.var_entry_boxcar_actuator_calibration_file.get()
            if calibrate_file == "":
                LOGGER.log("Please select a calibration file.")
                return
            try:
                with open(calibrate_file, 'r') as f:
                    reader = csv.reader(f)
                    next(reader)
                    wavelength = []
                    position = []
                    for row in reader:
                        wavelength.append(float(row[0]))
                        position.append(float(row[1]))
                    self.calibrate_func = interp1d(wavelength, position)
            except Exception as e:
                LOGGER.log(e)
                return
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
        self.page.save_boxcar_single_power.reset()
        self.calibrate_func = None
        self.wavelength_list = []
        self.ch1_list = []
        LOGGER.reset()

    def after_complete(self):
        super().after_complete()
        UTILS.push_notification("Sweep completed!")

    def predict_angle(self, power, amplitude, offset, coeff=0.33):
        '''
        Reverse function of amplitude*np.exp(-coeff*(angle-offset)**0.6).
        The 0.6 comes from empirical fitting with ndfilter calibration data.
        '''
        return (-np.log(power/amplitude)/coeff)**(1/0.6)+offset

    def predict_max_power(self, power, angle, offset, coeff=0.33):
        return power / np.exp(-coeff*(angle-offset)**0.6)
    
    def find_target_power_by_ndfilter(self):
        if self.check_stopping():
            return
        curr_power = float(VARIABLES.var_entry_curr_power.get())
        target_power = float(VARIABLES.var_spinbox_sweep_target_power.get())
        if VARIABLES.var_checkbutton_photon_flux_fixed.get():
            target_power = target_power * \
                float(VARIABLES.var_spinbox_wavelength_at_target_power.get()
                      ) / self.curr_wavelength
        LOGGER.log(
            f"[Sweeping - {VARIABLES.var_entry_curr_wavelength.get()} nm] Finding target power {round(target_power, 6)}uW by NDFilter.")
        delta = float('inf')
        while abs(target_power - curr_power) > 0.005 * target_power and abs(delta) > 0.005:
            if self.check_stopping():
                return
            delta = -0.5 * (target_power - curr_power) / curr_power * \
                10 * float(VARIABLES.var_spinbox_ndfilter_speed.get())
            curr_ndfilter_position = float(
                VARIABLES.var_entry_curr_angle.get())
            VARIABLES.var_spinbox_target_angle.set(
                round(curr_ndfilter_position + delta, 6))
            self.page.set_angle_task.task_loop()
            # wait for var_entry_curr_power to update
            sleep(INSTANCES.powermeter.max_period + 0.2)
            curr_power = float(VARIABLES.var_entry_curr_power.get())