from threading import Thread
from utils.config import VARIABLES, INSTANCES, LOGGER, UTILS
from utils.task import Task, RUNNING, PAUSED
from equipments.powermeter import MAX_PERIOD
# from pages.sweep_wavelength import SweepWavelength
from time import sleep, time
import numpy as np
import csv
from scipy.interpolate import interp1d


class SweepWavelengthBoxcarTask(Task):
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
        self.ndfilter_direction_positive = True
        self.calibrate_func = None
        self.wavelength_list = []
        self.power_map = []
        self.ch1_map = []

    def task(self):
        VARIABLES.var_spinbox_target_wavelength.set(self.curr_wavelength)
        self.page.set_wavelength_task.task_loop()
        VARIABLES.var_spinbox_target_actuator_position.set(
            self.calibrate_func(self.curr_wavelength))
        self.page.set_actuator_position_task.task_loop()
        if self.ndfilter_direction_positive:
            if abs(float(VARIABLES.var_entry_curr_angle.get())) > 0.1:
                VARIABLES.var_spinbox_target_angle.set(0)
                self.page.set_angle_task.task_loop()
            VARIABLES.var_spinbox_target_angle.set(
                float(VARIABLES.var_entry_boxcar_ending_angle.get()))
        else:
            if abs(float(VARIABLES.var_entry_curr_angle.get()) - float(VARIABLES.var_entry_boxcar_ending_angle.get())) > 0.1:
                VARIABLES.var_spinbox_target_angle.set(
                    VARIABLES.var_entry_boxcar_ending_angle.get())
                self.page.set_angle_task.task_loop()
            VARIABLES.var_spinbox_target_angle.set(0)
        self.page.set_angle_task.start()
        # Below has to follow the set_angle_task.start() function for stop and resume to work properly
        self.ndfilter_direction_positive = not self.ndfilter_direction_positive
        start_time = time()
        power_list = []
        ch1_list = []
        sleep(MAX_PERIOD*2)
        while self.page.set_angle_task.is_running:
            if self.check_stopping():
                return
            power_list.append(float(VARIABLES.var_entry_curr_power.get()))
            ch1_list.append(float(INSTANCES.boxcar.get_voltage()))
            sleep(MAX_PERIOD)
            curr_time = time()
            print(curr_time)
            if curr_time - start_time > 30:
                LOGGER.log(
                    f"[Sweeping - {VARIABLES.var_entry_curr_wavelength.get()} nm] Set angle task timeout.")
                self.page.set_angle_task.reset()
                self.reset()
                return
        if self.check_stopping():
            return
        # Reverse the list if the ndfilter is moving in the negative direction. Notice ndfilter_direction_positive was flipped already.
        if self.ndfilter_direction_positive:
            power_list = power_list[::-1]
            ch1_list = ch1_list[::-1]
        self.wavelength_list.append(self.curr_wavelength)
        self.power_map.append(power_list)
        self.ch1_map.append(ch1_list)
        print(self.wavelength_list, self.power_map, self.ch1_map)
        self.page.plot_boxcar_curve.plot(self.power_map[-1], self.ch1_map[-1])
        self.page.plot_boxcar_heatmap.pcolormesh(
            *self.pad_heatmap(self.wavelength_list, self.power_map, self.ch1_map))
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
        self.page.save_oscilloscope.reset()
        self.wavelength_list = []
        self.power_map = []
        self.ch1_map = []
        self.ndfilter_direction_positive = True
        LOGGER.reset()

    def after_complete(self):
        super().after_complete()
        UTILS.push_notification("Sweep completed!")

    def pad_heatmap(self, wavelength_list, power_map, signal_map):
        max_length = max([len(sublist) for sublist in power_map])
        if power_map[0][0] < power_map[0][-1]:
            edge_power = max([max(sublist) for sublist in power_map])
        else:
            edge_power = min([min(sublist) for sublist in power_map])
        power_map_padded = [np.concatenate((sublist, np.full(
            max_length - len(sublist), edge_power))) for sublist in power_map]
        signal_map_padded = [np.concatenate((sublist, np.full(
            max_length - len(sublist), np.nan))) for sublist in signal_map]
        power_map_padded = np.array(power_map_padded)
        wavelength_lists_padded = np.array(
            [wavelength_list]*len(power_map_padded[0])).T
        signal_map_padded = np.array(signal_map_padded)
        xx, yy, z = wavelength_lists_padded, power_map_padded, signal_map_padded
        return xx, yy, z
