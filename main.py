import tkinter as tk
from tkinter import ttk
from pages.lifetime import Lifetime
from pages.sweep_power_cw import SweepPowerCW
from pages.sweep_wavelength import SweepWavelength
from pages.device_manager import DeviceManager
from pages.sweep_power import SweepPower
from utils.status_bar import StatusBar
from utils.config import LOGGER, VARIABLES, DEFAULT, INSTANCES


class App:
    def __init__(self, root):
        VARIABLES.initialize_vars()
        DEFAULT.load_default()
        LOGGER.initialize_status()
        INSTANCES.initialize_instances()
        self.root = root
        self.root.title('SpectraDynamics')
        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)
        tabControl = ttk.Notebook(self.root)
        tab1 = SweepWavelength(tabControl).frame
        tab2 = Lifetime(tabControl).frame
        tab3 = SweepPower(tabControl).frame
        tab4 = SweepPowerCW(tabControl).frame
        tab5 = DeviceManager(tabControl).frame
        tabControl.add(tab1, text='Sweep Wavelength')
        tabControl.add(tab2, text='Lifetime')
        tabControl.add(tab3, text='Sweep Power')
        tabControl.add(tab4, text='Sweep Power (CW)')
        tabControl.add(tab5, text='Device Manager')
        tabControl.pack(expand=1, fill='both')
        self.status_bar = StatusBar(self.root, VARIABLES.var_logger_status)
        self.status_bar.pack(side='bottom', fill='x')

    def on_closing(self):
        DEFAULT.save_default()
        self.root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.iconphoto(False, tk.PhotoImage(file='utils/icon.png'))
    root.mainloop()
