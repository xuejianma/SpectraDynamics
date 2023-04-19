from pyvisa import ResourceManager
from time import sleep, time
from threading import Lock


class Powermeter:

    def __init__(self, id_string_var=None):
        self.valid = False
        self.error_message = ""
        self.max_period = 0.2
        self.num = 50
        self.lock = Lock()
        try:
            if id_string_var:
                id_str = id_string_var.get()
            else:
                id_str = "P0016683"
            self.rm = ResourceManager()
            self.instrument = None
            usb_list = self.rm.list_resources()
            for item in usb_list:
                if id_str in item:
                    self.instrument = self.rm.open_resource(item)
                    break
            self.valid = True
            if self.instrument is None:
                self.valid = False
                self.error_message = "Powermeter not found"
        except Exception as e:
            self.valid = False
            self.error_message = e

    def set_wavelength(self, wavelength):
        self.instrument.write('CORRection:WAVelength ' + str(wavelength))

    def get_power(self):
        self.lock.acquire()
        try:
            power_sum = 0
            t1 = time()
            for _ in range(self.num):
                power_sum += float(self.instrument.query('Measure:Scalar:POWer?'))
                sleep(1e-6)
            ret = power_sum / self.num
            t2 = time()
            self.num = int(self.num * (self.max_period / (t2 - t1)))
        except Exception as e:
            raise e
        finally:
            self.lock.release()
        return ret

    def get_power_uW(self):
        return self.get_power() * 1e6


class PowermeterSimulator:
    def __init__(self, *args, **kwargs):
        self.valid = True
        self.error_message = ""
        self.max_period = 0.4

    def set_wavelength(self, wavelength):
        pass

    def get_power(self):
        return self.get_power_uW() * 1e-6

    def get_power_uW(self):
        from random import random
        from utils.config import VARIABLES
        import numpy as np
        wavelength = float(VARIABLES.var_entry_curr_wavelength.get())
        actuator_position = float(
            VARIABLES.var_entry_curr_actuator_position.get())
        angle = float(VARIABLES.var_entry_curr_angle.get())
        sleep(self.max_period)
        return 20 * np.exp(-0.25*abs(wavelength-actuator_position*40-400))*np.exp(-0.05*abs(angle)) + 0.01 * (random() - 0.5) + 0.1 + float(VARIABLES.var_entry_cwcontroller_curr_setpoint.get()) * 0.05
