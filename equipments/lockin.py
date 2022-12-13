import pyvisa as visa


class Lockin():
    def __init__(self, id_string_var=None):
        self.valid = False
        self.error_message = ""
        try:
            if id_string_var:
                id_str = id_string_var.get()
            else:
                id_str = "USB0::0xB506::0x2000::004169"
            rm = visa.ResourceManager()
            self.instrument = rm.open_resource(id_str)
            self.model = 'SR830' if 'SR830' in self.get_identification() else 'SR860'
            self.valid = True
            if self.instrument is None:
                self.valid = False
                self.error_message = "Lockin not found"
        except Exception as e:
            self.valid = False
            self.error_message = e

    def set_time_constant(self, index):
        if self.model == 'SR830':
            self.instrument.write("OFLT " + str(max(index, 0)))
        else: # SR860
            self.instrument.write("OFLT " + str(index + 2))

    def set_display(self, channel, index):
        # the last digit is ratio: 0 none, 1 Aux In 1, 2 Aus In 2
        if self.model == 'SR830':
            self.instrument.write("DDEF " + str(channel) + "," + str(index) + ",0")
        else:
            self.instrument.write("COUT " + str(channel - 1) + "," + str(index))

    def set_output(self, channel, index):
        self.instrument.write("FPOP " + str(channel) + "," + str(index))

    def set_reference_source(self, index):
        if self.model == 'SR830':
            self.instrument.write("FMOD " + str(index))
        else:
            self.instrument.write("RSRC " + str(1 - index))

    def set_frequency(self, freq):
        self.instrument.write("FREQ " + str(freq))

    def get_identification(self):
        return self.instrument.query("*IDN?")

    def get_output(self):
        ret = float(self.instrument.query("OUTP? R")) 
        return ret

class LockinSimulator():
    def __init__(self, *args, **kwargs):
        self.valid = True
        self.error_message = ""

    def set_time_constant(self, index):
        pass

    def set_display(self, channel, index):
        pass

    def set_output(self, channel, index):
        pass

    def set_reference_source(self, index):
        pass

    def set_frequency(self, freq):
        pass

    def get_identification(self):
        return "SR860"

    def get_output(self):
        from random import random
        from utils.config import VARIABLES
        return float(VARIABLES.var_entry_cwcontroller_curr_setpoint.get()) + random() * 0.1