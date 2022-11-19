from tkinter import ttk
from utils.config import INSTANCES


class DeviceManager:
    def __init__(self, parent):
        self.frame = self.set_frame(parent)
    
    def set_frame(self, parent):
        frame = ttk.Frame(parent)
        frame.pack()
        Device(frame, "Powermeter", INSTANCES.powermeter)
        Device(frame, "NDFilter", INSTANCES.ndfilter)
        Device(frame, "Monochromator", INSTANCES.monochromator)
        Device(frame, "Oscilloscope", INSTANCES.oscilloscope)
        Device(frame, "Actuator", INSTANCES.actuator)
        return frame

class Device(ttk.Frame):
    def __init__(self, parent, name, instance):
        super().__init__(parent)
        self.instance = instance
        self.pack(side="top", anchor="w", padx=(100, 0), pady=(30, 0))
        ttk.Label(self, text=name).pack(side="left")
        ttk.Label(self, text="Recorded Status: ").pack(side="left", padx=10)
        self.label_status = ttk.Label(self, text="SUCCESS" if self.instance.valid else "FAIL")
        self.label_status.pack(side="left", padx=10)
        ttk.Button(self, text="Reconnect", command=self.reconnect).pack(side="left", padx=10)
        self.label_error = ttk.Label(self, text=self.instance.error_message)
        self.label_error.pack(side="left", padx=10)
    def reconnect(self):
        self.instance.__init__()
        self.label_status.config(text="SUCCESS" if self.instance.valid else "FAIL")
        self.label_error.config(text=self.instance.error_message)