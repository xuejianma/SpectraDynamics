import warnings
warnings.simplefilter("ignore", UserWarning) # Ignore UserWarning from pywinauto
from pywinauto.application import Application
from time import sleep


class Monochromator:
    def __init__(self):
        self.edit_box = Application(backend="uia").connect(title="SciSpec 9.3.0.0", timeout=10).top_window(
        ).child_window(auto_id="TB_input", control_type="Edit")

    def get_wavelength(self):
        return float(self.edit_box.window_text())

    def set_wavelength(self, wavelength):
        self.edit_box.type_keys(str(wavelength) + "{ENTER}")
        while not self.edit_box.element_info.enabled:
            sleep(0.1)


class MonochromatorSimulator:
    def __init__(self):
        self.wavelength = 516

    def get_wavelength(self):
        return self.wavelength

    def set_wavelength(self, wavelength):
        sleep(1)
        self.wavelength = wavelength
