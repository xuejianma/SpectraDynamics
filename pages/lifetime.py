import tkinter as tk
from tkinter import ttk
class Lifetime(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tmp = ttk.Frame(self)
        tmp.pack()
        ttk.Button(tmp).pack(side=tk.LEFT)
        ttk.Button(tmp).pack(side=tk.LEFT)
        ttk.Button(tmp).pack(side=tk.LEFT)
        # ttk.Button(self).pack()
        # ttk.Button(self).pack()
