import datetime
import configparser
import tkinter as tk


class Variables:
    """
    All variables that needs to be saved when closing the program. 
    """

    def initialize_vars(self):
        self.var_entry_lifetime_directory = tk.StringVar()
        self.var_entry_lifetime_filename = tk.StringVar()
        self.var_spinbox_lifetime_num = tk.StringVar(value=20)
        self.var_spinbox_lifetime_wait_time = tk.StringVar(value=6)


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
                f"{msg} [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")


LOGGER = Logger()
VARIABLES = Variables()
DEFAULT = Default()
