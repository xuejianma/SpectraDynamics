import sys
# Solve askdirectory freezing problem after converting to exe
sys.coinit_flags = 2  # COINIT_APARTMENTTHREADED
from time import sleep
import warnings
# Ignore UserWarning from pywinauto
warnings.simplefilter("ignore", UserWarning)
if sys.platform.startswith("win"):
    from pywinauto.application import Application


class Monochromator:
    def __init__(self, id_string_var=None):
        self.valid = False
        self.error_message = ""
        try:
            if id_string_var:
                id_str = id_string_var.get()
            else:
                id_str = "SciSpec 9.3.0.0"
            app = Application(backend="uia").connect(
                title=id_str, timeout=1)
            self.edit_box = app.top_window().child_window(
                auto_id="TB_input", control_type="Edit")
            self.valid = True
        except Exception as e:
            self.valid = False
            self.error_message = str(
                e) + "[Time out when trying to connect to SciSpec 9.3.0.0 window]"

    def get_wavelength(self):
        return float(self.edit_box.window_text())

    def set_wavelength(self, wavelength):
        self.edit_box.type_keys(str(wavelength) + "{ENTER}")
        while not self.edit_box.element_info.enabled:
            sleep(0.1)


class MonochromatorSimulator:
    def __init__(self, *args, **kwargs):
        self.valid = True
        self.error_message = ""
        self.wavelength = 516

    def get_wavelength(self):
        return self.wavelength

    def set_wavelength(self, wavelength):
        sleep(1)
        self.wavelength = wavelength