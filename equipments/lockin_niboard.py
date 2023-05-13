import pyvisa as visa
import sys
import numpy as np
if sys.platform.startswith("win"):
    import nidaqmx
    from nidaqmx.stream_readers import AnalogMultiChannelReader


class LockinNIBoard():
    def __init__(self, id_string_var=None):
        self.valid = False
        self.error_message = ""
        try:
            if id_string_var:
                id_str = id_string_var.get()
            else:
                id_str = "NI6259"
            self.task = nidaqmx.Task()
            self.task.ai_channels.add_ai_voltage_chan(id_str + "/ai1")
            self.task.ai_channels.add_ai_voltage_chan(id_str + "/ai2")
            self.reader = AnalogMultiChannelReader(self.task.in_stream)
            self.valid = True
            if self.task is None:
                self.valid = False
                self.error_message = "Lockin NIBoard not found"
        except Exception as e:
            self.valid = False
            self.error_message = e

    def get_outputs(self, sampling_num=3000):
        ret = np.zeros((2, sampling_num))
        self.reader.read_many_sample(
            data=ret, number_of_samples_per_channel=sampling_num, timeout=1)
        return np.mean(ret[0]), np.mean(ret[1])


class LockinNIBoardSimulator():
    def __init__(self, *args, **kwargs):
        self.valid = True
        self.error_message = ""

    def get_outputs(self, sampling_num=3000):
        from random import random
        from utils.config import VARIABLES
        return float(VARIABLES.var_entry_cwcontroller_curr_setpoint.get()) + random() * 0.1,\
            float(VARIABLES.var_entry_cwcontroller_curr_setpoint.get()) + random() * 0.1
