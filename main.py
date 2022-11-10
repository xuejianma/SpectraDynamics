import tkinter as tk
from tkinter import ttk
from pages.lifetime import Lifetime

class App:
    def __init__(self, root):
        root.title("SpectraDynamics")
        tabControl = ttk.Notebook(root)
        tab1 = Lifetime(tabControl)#ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)
        tabControl.add(tab1, text ='Lifetime')
        tabControl.add(tab2, text ='Tab 2')
        tabControl.pack(expand = 1, fill ="both")
        # lifetime = Lifetime(root)
        # lifetime.pack()
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
