from pyvisa import ResourceManager


class CWController:
    def __init__(self, id_string_var=None):
        self.valid = False
        self.error_message = ""
        try:
            if id_string_var:
                id_str = id_string_var.get()
            else:
                id_str = "M00460823"
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
                self.error_message = "CWController not found"
        except Exception as e:
            self.valid = False
            self.error_message = e
    
    def set_current_setpoint(self, current_setpoint):
        self.instrument.write("SOUR:CURR {}".format(float(current_setpoint) / 1e3))
    
    def get_current_setpoint(self):
        return float(self.instrument.query("SOUR:CURR?"))

    def get_current_setpoint_mA(self):
        return self.get_current_setpoint() * 1e3
    
    def set_on(self):
        self.instrument.write("OUTP ON")
    
    def set_off(self):
        self.instrument.write("OUTP OFF")
    
    def get_status(self):
        return 'ON' if '1' in self.instrument.query("OUTP?") else 'OFF'

class CWControllerSimulator:
    def __init__(self, *args, **kwargs):
        self.valid = True
        self.error_message = ""
        self.current_setpoint = 0
        self.status = "OFF"
    
    def set_current_setpoint(self, current_setpoint):
        self.current_setpoint = float(current_setpoint) / 1e3
    
    def get_current_setpoint(self):
        return self.current_setpoint
    
    def get_current_setpoint_mA(self):
        return self.current_setpoint * 1e3
    
    def set_on(self):
        self.status = "ON"
    
    def set_off(self):
        self.status = "OFF"
    
    def get_status(self):
        return self.status
