import configparser
import tkinter as tk
from equipments.oscilloscope import Oscilloscope, OscilloscopeSimulator
from equipments.ndfilter import NDFilter, NDFilterSimulator
from equipments.powermeter import Powermeter, PowermeterSimulator
from equipments.monochromator import Monochromator, MonochromatorSimulator
from equipments.actuator import Actuator, ActuatorSimulator
from datetime import datetime

TEST_MODE = True

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
        self.var_entry_curr_actuator_position = tk.StringVar(value=0)
        self.var_spinbox_target_actuator_position = tk.StringVar(value=0)
        self.var_entry_curr_angle = tk.StringVar(value=0)
        self.var_spinbox_target_angle = tk.StringVar(value=0)
        self.var_entry_curr_power = tk.StringVar(value=0)
        self.var_spinbox_background_power = tk.StringVar(value=0)
        self.var_spinbox_sweep_start_wavelength = tk.StringVar(value=0)
        self.var_spinbox_sweep_end_wavelength = tk.StringVar(value=0)
        self.var_spinbox_sweep_step_size = tk.StringVar(value=0)
        self.var_spinbox_sweep_target_power = tk.StringVar(value=0)
        self.var_spinbox_sweep_lifetime_num = tk.StringVar(value=0)
        self.var_spinbox_sweep_actuator_explore_range_negative = tk.StringVar(
            value=-0.05)
        self.var_spinbox_sweep_actuator_explore_range_positive = tk.StringVar(
            value=0.05)
        self.var_spinbox_sweep_actuator_explore_range_step_size = tk.StringVar(
            value=0.01)
        self.var_spinbox_sweep_lifetime_wait_time = tk.StringVar(value=6)
        self.var_entry_sweep_wavelength_directory = tk.StringVar()
        self.var_entry_sweep_wavelength_filename = tk.StringVar()
        self.var_spinbox_start_angle = tk.StringVar(value=0)
        self.var_spinbox_end_angle = tk.StringVar(value=90)
        self.var_spinbox_step_angle = tk.StringVar(value=1)
        self.var_spinbox_sweep_power_num = tk.StringVar(value=10)
        self.var_spinbox_sweep_power_wait_time = tk.StringVar(value=6)
        self.var_entry_sweep_power_directory = tk.StringVar()
        self.var_entry_sweep_power_filename = tk.StringVar()
        self.var_logger_status = tk.StringVar()


class Instances:
    """
    All instances used in the program should be initilized here.
    """

    def initialize_instances(self):
        self.oscilloscope = OscilloscopeSimulator() if TEST_MODE else Oscilloscope()
        self.ndfilter = NDFilterSimulator() if TEST_MODE else NDFilter()
        self.powermeter = PowermeterSimulator() if TEST_MODE else Powermeter()
        self.monochromator = MonochromatorSimulator() if TEST_MODE else Monochromator()
        self.actuator = ActuatorSimulator() if TEST_MODE else Actuator()
        # Initialize readings from equipments after instances are created.
        self.initialize_readings()

    def initialize_readings(self):
        try:
            VARIABLES.var_entry_curr_angle.set(
                round(self.ndfilter.get_angle(), 4))
            VARIABLES.var_entry_curr_wavelength.set(
                round(self.monochromator.get_wavelength(), 4))
            VARIABLES.var_entry_curr_actuator_position.set(
                round(self.actuator.get_position(), 4))
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
        VARIABLES.var_logger_status.set("Ready.")

    def log(self, msg):
        VARIABLES.var_logger_status.set(
            f"{msg} [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")

    def reset(self):
        self.initialize_status()

class Utils:
    def set_background_power(self):
        VARIABLES.var_spinbox_background_power.set(
            round(float(VARIABLES.var_entry_curr_power.get()) +
                  float(VARIABLES.var_spinbox_background_power.get()), 4))

VARIABLES = Variables()
LOGGER = Logger()
DEFAULT = Default()
INSTANCES = Instances()
UTILS = Utils()
