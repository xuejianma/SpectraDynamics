import sys
if sys.platform.startswith("win"):
    import nidaqmx
import time

class Boxcar():
    def __init__(self, id_string_var=None):
        self.valid = False
        self.error_message = ""
        try:
            if id_string_var:
                id_str = id_string_var.get()
            else:
                id_str = "NI6259"
            self.task = nidaqmx.Task()
            self.task.ai_channels.add_ai_voltage_chan(id_str + '/ai0')
            self.valid = True
        except Exception as e:
            self.valid = False
            self.error_message = e
    def get_voltage(self):
        return self.task.read()
        
class BoxcarSimulator():
    def __init__(self):
        self.valid = True
        self.error_message = ""
        self.voltage = 0
    def get_voltage(self):
        self.voltage += 0.001
        return self.voltage