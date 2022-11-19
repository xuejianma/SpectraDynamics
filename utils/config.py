import configparser
import tkinter as tk
from equipments.oscilloscope import OscilloscopeSimulator
from equipments.ndfilter import NDFilterSimulator
from equipments.powermeter import PowermeterSimulator
from equipments.monochromator import MonochromatorSimulator
from equipments.actuator import ActuatorSimulator
from datetime import datetime


class Variables:
    """
    All variables that needs to be saved when closing the program. 
    """

    def initialize_vars(self):
        self.var_entry_lifetime_directory = tk.StringVar()
        self.var_entry_lifetime_filename = tk.StringVar()
        self.var_spinbox_lifetime_num = tk.StringVar(value=20)
        self.var_spinbox_lifetime_wait_time = tk.StringVar(value=6)
        self.var_entry_curr_wavelength = tk.StringVar(value=0)
        self.var_spinbox_target_wavelength = tk.StringVar(value=0)
        self.var_entry_curr_angle = tk.StringVar(value=0)
        self.var_spinbox_target_angle = tk.StringVar(value=0)
        self.var_entry_curr_power = tk.StringVar(value=0)
        self.var_entry_curr_actuator_position = tk.StringVar(value=0)
        self.var_spinbox_target_actuator_position = tk.StringVar(value=0)
        self.var_spinbox_sweep_start_wavelength = tk.StringVar(value=0)
        self.var_spinbox_sweep_end_wavelength = tk.StringVar(value=0)
        self.var_spinbox_sweep_step_size = tk.StringVar(value=0)


class Instances:
    """
    All instances used in the program should be initilized here.
    """

    def initialize_instances(self):
        self.oscilloscope = OscilloscopeSimulator()
        self.ndfilter = NDFilterSimulator()
        self.powermeter = PowermeterSimulator()
        self.monochromator = MonochromatorSimulator()
        self.actuator = ActuatorSimulator()
        self.initialize_readings() # Initialize readings from equipments after instances are created.

    def initialize_readings(self):
        try:
            VARIABLES.var_entry_curr_angle.set(round(self.ndfilter.get_angle(), 4))
            VARIABLES.var_entry_curr_wavelength.set(round(self.monochromator.get_wavelength(), 4))
            VARIABLES.var_entry_curr_actuator_position.set(round(self.actuator.get_position(), 4))
        except:
            pass


class Default:
    """
    Save and load vairable values to/from ini file.
    """

    def load_default(self):
        try:
            with open("default.ini", "r") as f:
                config = configparser.ConfigParser()
                config.read_file(f)
                for key in config["DEFAULT"]:
                    try:
                        getattr(VARIABLES, key).set(config["DEFAULT"][key])
                    except:
                        pass
        except:
            pass

    def save_default(self):
        try:
            with open("default.ini", "w") as f:
                config = configparser.ConfigParser()
                default_values = {}
                for attr in VARIABLES.__dict__:
                    default_values[attr] = getattr(VARIABLES, attr).get()
                config["DEFAULT"] = default_values
                config.write(f)
        except:
            pass


class Logger:
    def initialize_status(self):
        self.status = tk.StringVar(value="Ready.")

    def log(self, msg):
        if self.status is not None:
            self.status.set(
                f"{msg} [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")


LOGGER = Logger()
VARIABLES = Variables()
DEFAULT = Default()
INSTANCES = Instances()
