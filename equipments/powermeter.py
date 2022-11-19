from pyvisa import ResourceManager


class Powermeter:

    def __init__(self):
        self.valid = False
        self.error_message = ""
        try:
            self.rm = ResourceManager()
            self.instrument = None
            usb_list = self.rm.list_resources()
            for item in usb_list:
                if "P0016683" in item:
                    self.instrument = self.rm.open_resource(item)
                    break
            self.valid = True
        except Exception as e:
            self.valid = False
            self.error_message = e

    def set_wavelength(self, wavelength):
        self.instrument.write('CORRection:WAVelength ' + str(wavelength))

    def get_power(self):
        ret = float(self.instrument.query('Measure:Scalar:POWer?'))
        return ret

    def get_power_uW(self):
        return self.get_power() * 1e6

class PowermeterSimulator:
    def __init__(self):
        self.valid = True
        self.error_message = ""
        self.power = 1e-5

    def set_wavelength(self, wavelength):
        pass

    def get_power(self):
        return self.power

    def get_power_uW(self):
        from random import random
        from utils.config import VARIABLES
        import numpy as np
        wavelength = float(VARIABLES.var_entry_curr_wavelength.get())
        actuator_position = float(VARIABLES.var_entry_curr_actuator_position.get())
        angle = float(VARIABLES.var_entry_curr_angle.get())
        return 20 * np.exp(-0.05*abs(wavelength-actuator_position*40-400))*np.exp(-0.05*abs(angle)) + 0.1 * (random() - 0.5)