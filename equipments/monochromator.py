from time import sleep

class MonochromatorSimulator:
    def __init__(self):
        self.wavelength = 516
    def get_wavelength(self):
        return self.wavelength
    def set_wavelength(self, wavelength):
        sleep(1)
        self.wavelength = wavelength