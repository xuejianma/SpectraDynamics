from time import sleep
import numpy as np
from pyvisa import ResourceManager

class Oscilloscope():
    def __init__(self):
        self.rm = ResourceManager()
        self.instrument = None
        usb_list = self.rm.list_resources()
        print(usb_list)
        for item in usb_list:
            if "DS6D150100004" in item:
                self.instrument = self.rm.open_resource(item)
                break
        if self.instrument is None:
            self.error()
        self.x_scale = None
        self.y_scale = None
    
    def error(self):
        raise ValueError()

    def start(self):
        self.instrument.write(":RUN")
    
    def stop(self):
        self.instrument.write(":STOP")
    
    def get_data(self, loading_time, label_oscilloscope_error, start=1, points=70000000,):
        try:
            self.start()
            sleep(loading_time)
            self.stop()
            wt = 0.01
            self.instrument.write(":WAV:MODE NORM")  # RAW means deeper raw data. NORM means displayed data
            sleep(wt)
            self.instrument.write(":WAV:STAR " + str(start))
            sleep(wt)
            self.instrument.write(":WAV:STOP " + str(points + start))
            sleep(wt)
            self.instrument.write(":WAV:POIN " + str(points))
            sleep(wt)
            self.instrument.write(":WAV:SOUR CHAN1")
            sleep(wt)
            self.instrument.write(":WAV:RES")
            sleep(wt)
            self.instrument.write(":WAV:BEG")
            sleep(wt)          
            rawdata_ch1 = self.instrument.query_binary_values(':WAV:DATA?', datatype='B', is_big_endian=False)
            sleep(wt)
            self.instrument.write(":WAV:SOUR CHAN2")
            sleep(wt)
            self.instrument.write(":WAV:RES")
            sleep(wt)
            self.instrument.write(":WAV:BEG")
            sleep(wt)          
            rawdata_ch2 = self.instrument.query_binary_values(':WAV:DATA?', datatype='B', is_big_endian=False)
            sleep(wt)            
            self.x_scale = float(self.instrument.query(':TIM:SCAL?'))
            sleep(wt)
            self.y_scale = float(self.instrument.query(':CHAN1:SCAL?'))
            return np.linspace(0, self.x_scale * 14, len(rawdata_ch1), endpoint=False), (np.asarray(rawdata_ch1) - 128) * (self.y_scale/(256/8)), (np.asarray(rawdata_ch2) - 128) * (self.y_scale/(256/8))
        except Exception as e:
            print(e)
            self.instrument = None
            # label_oscilloscope_error.setText(label_error_text)
    

class OscilloscopeSimulator:
    def __init__(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def get_data(self, loading_time, label_oscilloscope_error, start=1, points=70000000,):
        sleep(loading_time)
        X = np.linspace(0, 0.0001 * 14, 1400, endpoint=False)
        return (X, np.sin(10000 * X) + np.random.random(1400))