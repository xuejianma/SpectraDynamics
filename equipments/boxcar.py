import nidaqmx
import time

class Boxcar():
    def __init__(self):
        self.valid = False
        self.error_message = ""
        try:
            self.task = nidaqmx.Task()
            self.task.ao_channels.add_ai_voltage_chan('/ai4')
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