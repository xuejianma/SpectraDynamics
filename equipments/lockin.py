import pyvisa as visa


class Lockin():
    def __init__(self, top_or_bottom):
        self.valid = False
        self.error_message = ""
        name_dict = {
            'top': "USB0::0xB506::0x2000::004169", # Currently SR860, but can be changed to "GPIB0::9" for SR830
            'bottom': "USB0::0xB506::0x2000::004642" # Currently SR860, but can be changed to "GPIB0::8" for SR830
        }
        try:
            rm = visa.ResourceManager()
            tempstr = name_dict[top_or_bottom]
            self.instrument = rm.open_resource(tempstr)
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
    def __init__(self, top_or_bottom):
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