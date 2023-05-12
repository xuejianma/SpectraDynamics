from threading import Thread
from time import sleep
from utils.config import VARIABLES, INSTANCES, LOGGER

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
        try:
            trials = 0
            while abs(INSTANCES.monochromator.get_wavelength() - float(VARIABLES.var_spinbox_target_wavelength.get())) > 0.1:
                if trials > 1:
                    sleep(1)
                INSTANCES.monochromator.set_wavelength(
                    float(VARIABLES.var_spinbox_target_wavelength.get()))
                VARIABLES.var_entry_curr_wavelength.set(
                    round(INSTANCES.monochromator.get_wavelength(), 6))
                trials += 1
                if trials > 10:
                    raise Exception("Failed to set wavelength.")
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