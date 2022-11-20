import tkinter as tk
from tkinter import ttk
from datetime import datetime
import csv
from utils.config import LOGGER

class Save:
    def __init__(self, parent, var_directory, var_filename):
        self.parent = parent
        self.var_directory = var_directory
        self.var_filename = var_filename
        self.frame = self.set_frame()
        self.data_dict = {"header": [], "data": []}
        self.now = datetime.now()

    def set_frame(self):
        frame = ttk.Frame(self.parent)
        frame.pack()
        frame_1 = ttk.Frame(frame)
        frame_1.pack(anchor="w")
        frame_2 = ttk.Frame(frame)
        frame_2.pack(anchor="w")
        frame_3 = ttk.Frame(frame)
        frame_3.pack(anchor="w")
        label_directory = ttk.Label(frame_1, text="Directory: ")
        label_directory.pack(side="left")
        entry_directory = ttk.Entry(frame_1, textvariable=self.var_directory, width=40)
        entry_directory.pack(side="left")
        button_directory = ttk.Button(frame_1, text="Select Directory...", command=self.select_directory)
        button_directory.pack()
        label_filename = ttk.Label(frame_2, text="Filename: ")
        label_filename.pack(side="left")
        entry_filename = ttk.Entry(frame_2, textvariable=self.var_filename, width=40)
        entry_filename.pack(side="left")
        button = ttk.Button(frame_2, text="Save", command=self.save)
        button.pack(side="left")
        label_note = ttk.Label(frame_3, text="Note: \"{date}\"/\"{time}\" can be replaced with the current date/time")
        label_note.pack(side="left")
        return frame

    def select_directory(self):
        directory = tk.filedialog.askdirectory()
        if directory:
            self.var_directory.set(directory)

    def update_datetime(self):
        self.now = datetime.now()

    def save(self, update_datetime=True):
        if self.var_directory.get() and self.var_filename.get():
            try:
                if update_datetime:
                    self.update_datetime()
                filename = self.var_filename.get().replace("{date}", self.now.strftime("%Y%m%d")).replace("{time}", self.now.strftime("%H%M%S"))
                with open('/'.join([self.var_directory.get(), filename]), "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(self.data_dict["header"])
                    writer.writerows(self.data_dict["data"])
                LOGGER.log("Saved to {}".format(filename))
            except Exception as e:
                LOGGER.log("Error saving to {}: ".format(filename) + str(e))
        else:
            LOGGER.log("Please select a directory and filename")
