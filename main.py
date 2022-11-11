import tkinter as tk
from tkinter import ttk
from pages.lifetime import Lifetime
from pages.test import Test

class App:
    def __init__(self, root):
        root.title("SpectraDynamics")
        tabControl = ttk.Notebook(root)
        lifetime = Lifetime(tabControl)#ttk.Frame(tabControl)
        test = Test(tabControl)
        tab1 = lifetime.frame
        tab2 = test.frame
        tabControl.add(tab1, text ='Lifetime')
        tabControl.add(tab2, text ='Test')
        tabControl.pack(expand = 1, fill ="both")
        # lifetime = Lifetime(root)
        # lifetime.pack()
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
