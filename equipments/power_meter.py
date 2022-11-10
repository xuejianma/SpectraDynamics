from pyvisa import ResourceManager


class PowerMeter:
    # mutex = QMutex()

    def __init__(self):
        self.rm = ResourceManager()
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
        self.mutex.lock()
        ret = float(self.instrument.query('Measure:Scalar:POWer?'))
        self.mutex.unlock()
        return ret

    def get_power_uW(self):
        return self.get_power() * 1e6
