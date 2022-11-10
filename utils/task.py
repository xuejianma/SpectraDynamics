from threading import Thread
from time import sleep
from tkinter import ttk

class Task:
    def __init__(self, parent):
        self.i = 0
        self.running = False
        # self.callback = callback
        self.parent = parent
        self.frame, self.button_start, self.button_pause, self.button_terminate = self.set_frame()
    def set_frame(self):
        frame = ttk.Frame(self.parent)
        frame.pack()
        button_start = ttk.Button(frame, text="Start", command=self.start)
        button_start.pack(side="left")
        button_pause = ttk.Button(frame, text="Pause", command=self.pause)
        button_pause["state"] = "disabled"
        button_pause.pack(side="left")
        button_termiante = ttk.Button(frame, text="Terminate", command=self.terminate)
        button_termiante["state"] = "disabled"
        button_termiante.pack(side="left")
        return frame, button_start, button_pause, button_termiante
    def start(self):
        if not self.running:
            print(self.frame.children)
            self.button_start["state"] = "disabled"
            self.button_pause["state"] = "normal"
            self.button_terminate["state"] = "normal"
            self.running = True
            Thread(target=self.run_task).start()
    def task(self):
        while self.running and self.i < 5:
            self.i += 1
            print(self.i)
            sleep(1)
        # pass
    def reset(self):
        self.running = False
        self.i = 0
        self.button_terminate["state"] = "disabled"
        self.button_pause["state"] = "disabled"
        self.button_start["state"] = "normal"
        self.button_start.config(text="Start")
    def run_task(self):
        self.task()
        if self.running:
            self.reset()
    def pause(self):
        self.running = False
        self.button_pause["state"] = "disabled"
        self.button_start["state"] = "normal"
        # self.button_terminate["state"] = "normal" # redundant
        self.button_start.config(text="Resume")
    def terminate(self):
        self.running = False
        self.i = 0
        self.button_terminate["state"] = "disabled"
        self.button_pause["state"] = "disabled"
        self.button_start["state"] = "normal"
        self.button_start.config(text="Start")
