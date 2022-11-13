import tkinter as tk
from tkinter import ttk
from pages.lifetime import Lifetime
from pages.test import Test
from utils.status_bar import StatusBar
from utils.config import LOGGER, VARIABLES, DEFAULT


class App:
    def __init__(self, root):
        VARIABLES.initialize_vars()
        LOGGER.initialize_status()
        DEFAULT.load_default()
        self.root = root
        self.root.title("SpectraDynamics")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        tabControl = ttk.Notebook(self.root)
        lifetime = Lifetime(tabControl)
        test = Test(tabControl)
        tab1 = lifetime.frame
        tab2 = test.frame
        tabControl.add(tab1, text='Lifetime')
        tabControl.add(tab2, text='Test')
        tabControl.pack(expand=1, fill="both")
        self.status_bar = StatusBar(self.root, LOGGER.status)
        self.status_bar.pack(side="bottom", fill="x")

    def on_closing(self):
        DEFAULT.save_default()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
