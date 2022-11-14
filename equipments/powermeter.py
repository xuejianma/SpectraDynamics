# from pyvisa import ResourceManager


class Powermeter:
    # mutex = QMutex()

    def __init__(self):
        self.rm = None#ResourceManager()
        self.instrument = None
        usb_list = self.rm.list_resources()
        # print(usb_list)
        for item in usb_list:
            if "P0016683" in item:
                self.instrument = self.rm.open_resource(item)
                break
        if self.instrument is None:
            self.error()

    def error(self):
        raise ValueError()

    def set_wavelength(self, wavelength):
        self.instrument.write('CORRection:WAVelength ' + str(wavelength))

    def get_power(self):
        ret = float(self.instrument.query('Measure:Scalar:POWer?'))
        return ret

    def get_power_uW(self):
        return self.get_power() * 1e6

class PowermeterSimulator:
    def __init__(self):
        self.power = 1e-5

    def set_wavelength(self, wavelength):
        pass

    def get_power(self):
        return self.power

    def get_power_uW(self):
        from random import random
        return self.power * 1e6 + random()