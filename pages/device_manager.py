from tkinter import ttk
import tkinter as tk
from utils.config import INSTANCES, VARIABLES, LOGGER
from datetime import datetime
from pyvisa import ResourceManager


class DeviceManager:
    def __init__(self, parent):
        self.frame = self.set_frame(parent)
        self.get_resources()

    def set_frame(self, parent):
        frame = ttk.Frame(parent)
        frame.pack()
        Device(frame, "Oscilloscope", INSTANCES.oscilloscope, VARIABLES.id_oscilloscope)
        Device(frame, "Monochromator", INSTANCES.monochromator, VARIABLES.id_monochromator)
        Device(frame, "Actuator", INSTANCES.actuator, VARIABLES.id_actuator)
        Device(frame, "NDFilter", INSTANCES.ndfilter, VARIABLES.id_ndfilter)
        Device(frame, "Powermeter", INSTANCES.powermeter, VARIABLES.id_powermeter)
        Device(frame, "CWController", INSTANCES.cwcontroller, VARIABLES.id_cwcontroller)
        Device(frame, "Lockin (Top)", INSTANCES.lockin_top, VARIABLES.id_lockin_top)
        Device(frame, "Lockin (Bottom)", INSTANCES.lockin_bottom, VARIABLES.id_lockin_bottom)
        Device(frame, "Boxcar", INSTANCES.boxcar, None)
        ttk.Label(frame, text="Detected hardware Ports/Ids:").pack(side="top", anchor="w", padx=(100, 0), pady=(30, 0))
        ttk.Button(frame, text="Refresh Ports/Ids", command=self.refresh).pack(side="top", anchor="w", padx=(100, 0), pady=(0, 0))
        self.text_resources = tk.Text(frame)
        self.text_resources.pack(side="left", anchor="w", padx=(100, 0), pady=(0, 0))
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.text_resources.yview)
        scrollbar.pack(side="left", fill="y")
        self.text_resources.configure(yscrollcommand=scrollbar.set)
        ttk.Label(frame, text="Notification APP Token:").pack(side="top", anchor="w", padx=(100, 0), pady=(30, 0))
        ttk.Entry(frame, textvariable=VARIABLES.var_entry_notification_app_token, width=50).pack(side="top", anchor="w", padx=(100, 0), pady=(0, 0))
        ttk.Label(frame, text="Notification User Key:").pack(side="top", anchor="w", padx=(100, 0), pady=(30, 0))
        ttk.Entry(frame, textvariable=VARIABLES.var_entry_notification_user_key, width=50).pack(side="top", anchor="w", padx=(100, 0), pady=(0, 0))
        from utils.config import UTILS
        ttk.Button(frame, text="Test Notification", command=lambda: UTILS.push_notification("Hello World!")).pack(side="top", anchor="w", padx=(100, 0), pady=(30, 0))
        return frame
    
    def get_resources(self):
        try:
            resource_list = ResourceManager().list_resources() #["abc", "def", "34dfgdgs"] #
            self.text_resources.delete(1.0, tk.END)
            for resource in resource_list:
                self.text_resources.insert(tk.END, resource + "\n")
        except Exception as e:
            LOGGER.log(e)

    def refresh(self):
        LOGGER.log("Detected hardware Ports/Ids refreshed.")
        self.get_resources()
        

class Device(ttk.Frame):
    def __init__(self, parent, name, instance, id_string_var):
        super().__init__(parent)
        self.instance = instance
        self.id_string_var = id_string_var
        self.pack(side="top", anchor="w", padx=(100, 0), pady=(17, 0))
        ttk.Label(self, text=name).pack(side="left")
        ttk.Label(self, text="Recorded Status: ").pack(side="left", padx=10)
        self.label_status = ttk.Label(
            self, text="SUCCESS" if self.instance.valid else "FAIL")
        self.label_status.pack(side="left", padx=10)
        ttk.Label(self, text="Id：").pack(side="left", padx=(10, 0))
        if self.id_string_var:
            ttk.Entry(self, textvariable=self.id_string_var).pack(side="left", padx=10)
        else:
            ttk.Label(self, text='N/A', state='disabled').pack(side="left", padx=10)
        ttk.Button(self, text="Reconnect", command=self.reconnect).pack(
            side="left", padx=10)
        self.label_error = ttk.Label(
            self, text=f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {self.instance.error_message}"
            if self.instance.error_message else "")
        self.label_error.pack(side="left", padx=10)

    def reconnect(self):
        if self.id_string_var:
            self.instance.__init__(id_string_var=self.id_string_var)
        else:
            self.instance.__init__()
        self.label_status.config(
            text="SUCCESS" if self.instance.valid else "FAIL")
        self.label_error.config(
            text=f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {self.instance.error_message}"
            if self.instance.error_message else "")
