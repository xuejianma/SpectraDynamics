from time import sleep
import numpy as np
from utils.config import INSTANCES, LOGGER, VARIABLES, UTILS
from utils.task import Task, PAUSED
# from pages.sweep_wavelength import SweepWavelength


class CalibrateActuatorTask(Task):
    def __init__(self, parent, page):
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
        self.save_wavelength_list = []
        self.save_actuator_position_list = []

    
    def task(self):
        VARIABLES.var_spinbox_target_wavelength.set(self.curr_wavelength)
        self.page.set_wavelength_task.task_loop()
        self.find_max_power_by_actuator()
        if self.check_stopping():
            return
        if not self.check_devices_valid():
            LOGGER.log(
                f"[Sweeping - {VARIABLES.var_entry_curr_wavelength.get()} nm] Invalid device(s).")
            self.pause()
            UTILS.push_notification("Paused due to invalid device(s).")
            return
        self.save_wavelength_list.append(self.curr_wavelength)
        self.save_actuator_position_list.append(
            float(VARIABLES.var_entry_curr_actuator_position.get()))
        self.page.plot_calibrate_actuator.plot(
            self.save_wavelength_list, self.save_actuator_position_list)
        if float(VARIABLES.var_spinbox_sweep_start_wavelength.get()) <= float(VARIABLES.var_spinbox_sweep_end_wavelength.get()):
            self.curr_wavelength += float(
                VARIABLES.var_spinbox_sweep_step_size.get())
        else:
            self.curr_wavelength -= float(
                VARIABLES.var_spinbox_sweep_step_size.get())
        self.curr_wavelength = round(self.curr_wavelength, 6)
    
    def task_loop(self):
        try:
            if VARIABLES.var_entry_curr_angle.get() != "0":
                VARIABLES.var_spinbox_target_angle.set(0)
                self.page.set_angle_task.task_loop()
            super().task_loop()
        except Exception as e:
            LOGGER.log(e)
            self.reset()
            raise e          
    
    def find_max_power_by_actuator(self):
        if self.check_stopping():
            return
        LOGGER.log(
            f"[Calibrating - {VARIABLES.var_entry_curr_wavelength.get()} nm] Finding max power by actuator...")
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
        # self.page.save_calibrate_actuator
        # wait for var_entry_curr_power to update before getting power in find_target_power_by_ndfilter
        sleep(INSTANCES.powermeter.max_period + 0.2)
    
    def save_data(self):
        if self.check_stopping():
            return
        if not self.page.save_calibrate_actuator.data_dict["header"]:
            self.page.save_calibrate_actuator.data_dict["header"] = [
                "Wavelength (nm)", "Actuator Position (mm)"]
        self.page.save_calibrate_actuator.data_dict["data"] = [
            self.save_wavelength_list, self.save_actuator_position_list]
        self.page.save_calibrate_actuator.save()

    def check_devices_valid(self):
        return INSTANCES.oscilloscope.valid and INSTANCES.monochromator.valid and INSTANCES.actuator.valid \
            and INSTANCES.ndfilter.valid and INSTANCES.powermeter.valid and INSTANCES.boxcar.valid
        
    def start(self):
        if not self.check_devices_valid():
            LOGGER.log(
                "Not all devices are connected! Please connect all devices in Device Manager page before starting a calibration.")
            return
        if self.page.set_wavelength_task.is_running:
            LOGGER.log(
                "Please wait for the monochromator to finish setting wavelength before starting a calibration.")
            return
        if self.page.set_actuator_position_task.is_running:
            LOGGER.log(
                "Please wait for the actuator to finish setting position before starting a calibration.")
            return
        if self.page.set_angle_task.is_running:
            LOGGER.log(
                "Please wait for the NDFilter to finish setting angle before starting a calibration.")
            return
        if self.page.home_actuator_task.is_running:
            LOGGER.log(
                "Please wait for the actuator to finish homing before starting a calibration.")
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
            self.page.save_calibrate_actuator.update_datetime()
        super().start()
    

    def paused(self):
        super().paused()
        for widget in self.on_off_widgets:
            widget.config(state="normal")
        for external_button_control in self.external_button_control_list:
            external_button_control.external_button_control = False

    def reset(self):
        super().reset()
        for widget in self.on_off_widgets:
            widget.config(state="normal")
        for external_button_control in self.external_button_control_list:
            external_button_control.external_button_control = False
        self.save_data()
        self.save_wavelength_list = []
        self.save_actuator_position_list = []
        self.page.save_calibrate_actuator.reset()
        LOGGER.reset()