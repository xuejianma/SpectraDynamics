from threading import Thread
from utils.config import VARIABLES, INSTANCES, LOGGER, UTILS
from utils.task import Task, RUNNING, PAUSED
from equipments.powermeter import MAX_PERIOD
# from pages.sweep_wavelength import SweepWavelength
from time import sleep, time
import numpy as np
import csv
from scipy.interpolate import interp1d


class CalibrateNDFilterTask(Task):
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
                               self.page.spinbox_calibrate_ndfilter_starting_angle,
                               self.page.spinbox_calibrate_ndfilter_ending_angle,
                               self.page.spinbox_calibrate_actuator_steps,
                               ]
        self.external_button_control_list = [
            self.page.set_wavelength_task,
            self.page.set_angle_task,
            self.page.set_actuator_position_task,
            self.page.home_actuator_task,
        ]
        self.calibrate_func = None
        self.wavelength_list = []
        self.angle_list = []
        self.power_lists = []

    def task(self):
        pass
        # check MAX_PERIOD
        VARIABLES.var_spinbox_target_wavelength.set(self.curr_wavelength)
        self.page.set_wavelength_task.task_loop()
        VARIABLES.var_spinbox_target_actuator_position.set(
            self.calibrate_func(self.curr_wavelength))
        LOGGER.log(
            f"[Sweeping - {VARIABLES.var_entry_curr_wavelength.get()} nm] Go to pre-calibrated actuator position.")
        self.page.set_actuator_position_task.task_loop()
        VARIABLES.var_spinbox_target_angle.set(0)
        LOGGER.log(
            f"[Sweeping - {VARIABLES.var_entry_curr_wavelength.get()} nm] Going to 0 degree.")
        self.page.set_angle_task.task_loop()
        power_list = []
        for i, angle in enumerate(self.angle_list):
            if self.check_stopping():
                return
            VARIABLES.var_spinbox_target_angle.set(round(angle, 6))
            if (i+1) % (len(self.angle_list) / 50) == 0 or len(self.angle_list) <= 50:
                LOGGER.log(
                    f"[Sweeping - {VARIABLES.var_entry_curr_wavelength.get()} nm] Angle sweeping: ({((i+1)/len(self.angle_list))*100:.2f}%)")
                self.page.plot_calibrate_ndfilter_curve.plot(self.angle_list[:len(power_list)], power_list)
            prev_time = time()
            self.page.set_angle_task.task_loop()
            curr_time = time()
            if curr_time - prev_time < MAX_PERIOD * 2:
                print(f"sleeping {MAX_PERIOD * 2 - (curr_time - prev_time)}")
                sleep(MAX_PERIOD * 2 - (curr_time - prev_time))
            power_list.append(float(VARIABLES.var_entry_curr_power.get()))
        self.wavelength_list.append(self.curr_wavelength)
        self.power_lists.append(power_list)
        self.page.plot_calibrate_ndfilter_heatmap.pcolormesh(self.wavelength_list, self.angle_list[:len(power_list)], np.array(self.power_lists).T)
        self.save_data(self.angle_list, power_list)
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
            self.reset(error=True)
            UTILS.push_notification("Error: " + str(e))
            raise e

    def save_data(self, angle_list, power_list):
        if self.check_stopping():
            return
        if not self.page.save_calibrate_ndfilter.data_dict["header"]:
            self.page.save_calibrate_ndfilter.data_dict["header"].append("angle")
            self.page.save_calibrate_ndfilter.data_dict["data"].append(angle_list)
        self.page.save_calibrate_ndfilter.data_dict["header"].append(
            f"{self.curr_wavelength}")
        self.page.save_calibrate_ndfilter.data_dict["data"].append(power_list)
        self.page.save_calibrate_ndfilter.save(update_datetime=False)

    def check_devices_valid(self):
        return INSTANCES.monochromator.valid and INSTANCES.actuator.valid \
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
        starting_angle = float(
            VARIABLES.var_spinbox_calibrate_ndfilter_starting_angle.get())
        ending_angle = float(
            VARIABLES.var_spinbox_calibrate_ndfilter_ending_angle.get())
        if starting_angle > ending_angle:
            LOGGER.log(
                "Starting angle cannot be larger than ending angle.")
            return
        steps = int(VARIABLES.var_spinbox_calibrate_ndfilter_steps.get())
        self.angle_list = list(np.logspace(0,np.log(ending_angle - starting_angle + 1)/np.log(10), steps) + starting_angle - 1)
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
            self.page.save_calibrate_ndfilter.update_datetime()
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

    def reset(self, error=False):
        super().reset()
        VARIABLES.var_spinbox_target_angle.set(0)
        self.page.set_angle_task.task_loop()
        for widget in self.on_off_widgets:
            widget.config(state="normal")
        for external_button_control in self.external_button_control_list:
            external_button_control.external_button_control = False
        self.page.save_calibrate_ndfilter.reset()
        self.calibrate_func = None
        self.wavelength_list = []
        self.angle_list = []
        self.power_lists = []
        if not error:
            LOGGER.reset()

    def after_complete(self):
        super().after_complete()
        UTILS.push_notification("Sweep completed!")

