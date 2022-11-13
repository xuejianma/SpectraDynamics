import tkinter  as tk
from tkinter import ttk

class StatusBar(ttk.Frame):

    def __init__(self, master, var_status):
        super().__init__(master)
        self.label = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W, textvariable=var_status, padx=10)
        self.label.pack(fill=tk.X)