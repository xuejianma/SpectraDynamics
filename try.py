import tkinter as tk
from tkinter import ttk


class main(tk.Tk):

    def get_txt(self):
        self.lab2.config(text=self.ent.get())

    def __init__(self):
        super().__init__()
        self.x = tk.StringVar()
        self.x.set("default entry text")

        self.y = tk.StringVar()
        self.y.set("default combo option")

        self.ent = ttk.Entry(self, textvariable=self.x)
        lab = ttk.Label(self, textvariable=self.x)
        self.lab2 = ttk.Label(self)
        buttn = ttk.Button(self, text='GET TEXT', command=self.get_txt)
        combo = ttk.Combobox(self, values=['dog', 'cat', 'goldfish'], textvariable=self.y)
        lab3 = ttk.Label(self, textvariable=self.y)

        self.ent.grid()
        lab.grid()
        self.lab2.grid()
        buttn.grid()
        combo.grid()
        lab3.grid()

root = main()
root.mainloop()