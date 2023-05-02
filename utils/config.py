import configparser
import tkinter as tk
from equipments.oscilloscope import Oscilloscope, OscilloscopeSimulator
from equipments.ndfilter import NDFilter, NDFilterSimulator
from equipments.powermeter import Powermeter, PowermeterSimulator
from equipments.monochromator import Monochromator, MonochromatorSimulator
from equipments.actuator import Actuator, ActuatorSimulator
from equipments.cwcontroller import CWController, CWControllerSimulator
from equipments.lockin import Lockin, LockinSimulator
from equipments.boxcar import Boxcar, BoxcarSimulator
from datetime import datetime

TEST_MODE = True


class Variables:
    """
    All variables that needs to be saved when closing the program. 
    """

    def initialize_vars(self):
        self.id_oscilloscope = tk.StringVar(value='DS6D150100004')
        self.id_monochromator = tk.StringVar(value='SciSpec 9.3.0.0')
        self.id_actuator = tk.StringVar(value=27264119)
        self.id_ndfilter = tk.StringVar(value=55254094)
        self.id_powermeter = tk.StringVar(value='P0016683')
        self.id_cwcontroller = tk.StringVar(value='M00460823')
        self.id_lockin_top = tk.StringVar(value='USB0::0xB506::0x2000::004169')
        self.id_lockin_bottom = tk.StringVar(
            value='USB0::0xB506::0x2000::004642')
        self.id_boxcar_niboard = tk.StringVar(value='NI6259')
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
        self.var_spinbox_ndfilter_speed = tk.StringVar(value=1)
        self.var_entry_curr_power = tk.StringVar(value=0)
        self.var_spinbox_background_power = tk.StringVar(value=0)
        self.var_spinbox_sweep_start_wavelength = tk.StringVar(value=0)
        self.var_spinbox_sweep_end_wavelength = tk.StringVar(value=0)
        self.var_spinbox_sweep_step_size = tk.StringVar(value=0)
        self.var_checkbutton_photon_flux_fixed = tk.IntVar(value=0)
        self.var_spinbox_wavelength_at_target_power = tk.StringVar(value=0)
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
        self.var_entry_calibrate_actuator_directory = tk.StringVar()
        self.var_entry_calibrate_actuator_filename = tk.StringVar()
        self.var_entry_actuator_calibration_file = tk.StringVar()
        self.var_entry_heatmap_ending_angle = tk.StringVar(value=0)
        self.var_entry_sweep_wavelength_boxcar_heatmap_directory = tk.StringVar()
        self.var_entry_sweep_wavelength_boxcar_heatmap_filename = tk.StringVar()
        self.var_spinbox_calibrate_ndfilter_starting_angle = tk.StringVar(value=0)
        self.var_spinbox_calibrate_ndfilter_ending_angle = tk.StringVar(value=180)
        self.var_spinbox_calibrate_ndfilter_steps = tk.StringVar(value=100)
        self.var_entry_calibrate_ndfilter_directory = tk.StringVar()
        self.var_entry_calibrate_ndfilter_filename = tk.StringVar()
        self.var_spinbox_single_power_ndfilter_offset_angle = tk.StringVar(value=0)
        self.var_entry_sweep_wavelength_boxcar_single_power_directory = tk.StringVar()
        self.var_entry_sweep_wavelength_boxcar_single_power_filename = tk.StringVar()
        self.var_entry_sweep_wavelength_lockin_single_power_directory = tk.StringVar()
        self.var_entry_sweep_wavelength_lockin_single_power_filename = tk.StringVar()
        self.var_spinbox_boxcar_single_power_time_interval = tk.StringVar(value=1)
        self.var_spinbox_boxcar_single_power_number_of_data_acquisitions = tk.StringVar(value=1)
        self.var_spinbox_lockin_single_power_time_interval = tk.StringVar(value=1)
        self.var_spinbox_lockin_single_power_number_of_data_acquisitions = tk.StringVar(value=1)
        self.var_entry_sweep_wavelength_lockin_heatmap_directory = tk.StringVar()
        self.var_entry_sweep_wavelength_lockin_heatmap_filename = tk.StringVar()
        self.var_spinbox_start_angle = tk.StringVar(value=0)
        self.var_spinbox_end_angle = tk.StringVar(value=90)
        self.var_spinbox_step_angle = tk.StringVar(value=1)
        self.var_spinbox_sweep_power_num = tk.StringVar(value=10)
        self.var_spinbox_sweep_power_wait_time = tk.StringVar(value=6)
        self.var_checkbutton_load_conversion = tk.IntVar(value=0)
        self.var_entry_sweep_power_directory = tk.StringVar()
        self.var_entry_sweep_power_filename = tk.StringVar()
        self.var_logger_status = tk.StringVar()
        self.var_entry_cwcontroller_status = tk.StringVar(value='OFF')
        self.var_entry_cwcontroller_curr_setpoint = tk.StringVar(value=0)
        self.var_spinbox_cwcontroller_target_setpoint = tk.StringVar(value=0)
        self.var_spinbox_cwcontroller_setpoint_limit = tk.StringVar(value=40)
        self.var_spinbox_cwcontroller_start_setpoint = tk.StringVar(value=0)
        self.var_spinbox_cwcontroller_end_setpoint = tk.StringVar(value=10)
        self.var_spinbox_cwcontroller_step_setpoint = tk.StringVar(value=0.1)
        self.var_entry_sweep_power_cw_directory = tk.StringVar()
        self.var_entry_sweep_power_cw_filename = tk.StringVar()
        self.var_spinbox_sweep_power_cw_num = tk.StringVar(value=10)
        self.var_spinbox_cwcontroller_wait_time = tk.StringVar(value=1)
        self.var_spinbox_setpoint_conversion_start_setpoint = tk.StringVar(
            value=0)
        self.var_spinbox_setpoint_conversion_end_setpoint = tk.StringVar(
            value=10)
        self.var_spinbox_setpoint_conversion_step_setpoint = tk.StringVar(
            value=0.1)
        self.var_entry_setpoint_conversion_directory = tk.StringVar()
        self.var_entry_setpoint_conversion_filename = tk.StringVar()
        self.var_entry_notification_app_token = tk.StringVar()
        self.var_entry_notification_user_key = tk.StringVar()


class Instances:
    """
    All instances used in the program should be initilized here.
    """

    def initialize_instances(self):
        self.oscilloscope = Oscilloscope(
            VARIABLES.id_oscilloscope) if not TEST_MODE else OscilloscopeSimulator()
        self.ndfilter = NDFilter(
            VARIABLES.id_ndfilter) if not TEST_MODE else NDFilterSimulator()
        self.powermeter = Powermeter(
            VARIABLES.id_powermeter) if not TEST_MODE else PowermeterSimulator()
        self.monochromator = Monochromator(
            VARIABLES.id_monochromator) if not TEST_MODE else MonochromatorSimulator()
        self.actuator = Actuator(
            VARIABLES.id_actuator) if not TEST_MODE else ActuatorSimulator()
        self.cwcontroller = CWController(
            VARIABLES.id_cwcontroller) if not TEST_MODE else CWControllerSimulator()
        self.lockin_top = Lockin(
            VARIABLES.id_lockin_top) if not TEST_MODE else LockinSimulator('top')
        self.lockin_bottom = Lockin(
            VARIABLES.id_lockin_bottom) if not TEST_MODE else LockinSimulator('bottom')
        self.boxcar = Boxcar() if not TEST_MODE else BoxcarSimulator()
        # Initialize readings from equipments after instances are created.
        self.initialize_readings()

    def initialize_readings(self):
        try:
            VARIABLES.var_entry_curr_angle.set(
                round(self.ndfilter.get_angle(), 6))
        except:
            pass
        try:
            VARIABLES.var_entry_curr_wavelength.set(
                round(self.monochromator.get_wavelength(), 6))
        except:
            pass
        try:
            VARIABLES.var_entry_curr_actuator_position.set(
                round(self.actuator.get_position(), 6))
        except:
            pass
        try:
            VARIABLES.var_entry_cwcontroller_curr_setpoint.set(
                INSTANCES.cwcontroller.get_current_setpoint_mA())
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
        VARIABLES.var_logger_status.set("Standby.")

    def log(self, msg):
        message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
        VARIABLES.var_logger_status.set(message)
        with open("log.txt", "a") as f:
            f.write(message + "\n")
        with open("log.txt", "r") as f:
            lines = f.readlines()
        if len(lines) > 1000:
            with open("log.txt", "w") as f:
                f.writelines(lines[-1000:])

    def reset(self):
        self.initialize_status()


class Utils:
    def set_background_power(self):
        VARIABLES.var_spinbox_background_power.set(
            round(float(VARIABLES.var_entry_curr_power.get()) +
                  float(VARIABLES.var_spinbox_background_power.get()), 6))

    def push_notification(self, message):
        import http.client
        import urllib
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
                     urllib.parse.urlencode({
                         "token": str(VARIABLES.var_entry_notification_app_token.get()),
                         "user": str(VARIABLES.var_entry_notification_user_key.get()),
                         "message": str(message),
                     }), {"Content-type": "application/x-www-form-urlencoded"})
        response = conn.getresponse()
        print("Sending Notification to Pushover: ",
              response.status, response.reason, response.read())
        conn.close()


class Globals:
    """
    Global non-tkinter variables.
    """

    def __init__(self):
        self.setpoints_to_convert = []
        self.powers_converted_from_setpoints = []


VARIABLES = Variables()
LOGGER = Logger()
DEFAULT = Default()
INSTANCES = Instances()
UTILS = Utils()
GLOBALS = Globals()
