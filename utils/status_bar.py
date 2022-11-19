import tkinter as tk
from tkinter import ttk


class StatusBar(ttk.Frame):

    def __init__(self, master, var_status):
        super().__init__(master)
        self.label = tk.Label(self, bd=1, relief=tk.SUNKEN,
                              anchor=tk.W, textvariable=var_status, padx=10)
        self.label.pack(side="left", fill="x", expand=True)
        self.label_clear = tk.Label(self, padx=10, text="Clear Log")
        self.label_clear.pack(side="left")
        self.label_clear.bind("<Button-1>", lambda _: var_status.set(""))
