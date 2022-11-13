import tkinter as tk
from tkinter import ttk
import csv
from utils.config import LOGGER

class Save:
    def __init__(self, parent, var_directory, var_filename):
        self.parent = parent
        self.var_directory = var_directory
        self.var_filename = var_filename
        self.frame = self.set_frame()
        self.data_dict = {"header": [], "data": []}

    def set_frame(self):
        frame = ttk.Frame(self.parent)
        frame.pack()
        frame_1 = ttk.Frame(frame)
        frame_1.pack(anchor="w")
        frame_2 = ttk.Frame(frame)
        frame_2.pack(anchor="w")
        label_directory = ttk.Label(frame_1, text="Directory: ")
        label_directory.pack(side="left")
        entry_directory = ttk.Entry(frame_1, textvariable=self.var_directory, width=50)
        entry_directory.pack(side="left")
        button_directory = ttk.Button(frame_1, text="Select Directory...", command=self.select_directory)
        button_directory.pack()
        label_filename = ttk.Label(frame_2, text="Filename: ")
        label_filename.pack(side="left")
        entry_filename = ttk.Entry(frame_2, textvariable=self.var_filename, width=50)
        entry_filename.pack(side="left")
        button = ttk.Button(frame_2, text="Save", command=self.save)
        button.pack(side="left")
        return frame

    def set_filename(self, filename):
        self.var_filename.set(filename)

    def select_directory(self):
        directory = tk.filedialog.askdirectory()
        if directory:
            self.var_directory.set(directory)

    def save(self):
        if self.var_directory.get() and self.var_filename.get():
            try:
                with open('/'.join([self.var_directory.get(), self.var_filename.get()]), "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(self.data_dict["header"])
                    writer.writerows(self.data_dict["data"])
                LOGGER.log("Saved to {}".format(self.var_filename.get()))
            except Exception as e:
                LOGGER.log("Error saving to {}: ".format(self.var_filename.get()) + str(e))
        else:
            LOGGER.log("Please select a directory and filename")
