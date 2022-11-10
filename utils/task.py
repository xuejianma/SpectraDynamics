from threading import Thread
from time import sleep, time
from tkinter import ttk
from datetime import timedelta


RUNNING = 0
PAUSING = 1
PAUSED = 2
TERMINATING = 3
TERMINATED = 4


class Task:
    """
    Task is a module that runs a loop in an indivisual thread that does something,
    and can be paused, resumed, and terminated. It has buttons and progress_bar
    pre-set in self.frame for easy use.
    """

    def __init__(self, parent, num):
        """
        :param parent: parent widget
        :param num: total number of iterations for self.i in task_loop to iterate
        """
        self.i = 0
        self.num = num
        self.status = TERMINATED
        self.parent = parent
        self.time_per_iteration = 0
        self.frame, self.button_start, self.button_pause, self.button_terminate, \
            self.progress_bar, self.label_remaining = self.set_frame()

    def set_frame(self):
        """
        Set up the frame with buttons and progress bar.
        """
        frame = ttk.Frame(self.parent)
        frame.pack()
        frame_upper = ttk.Frame(frame)
        frame_upper.pack()
        progress_bar = ttk.Progressbar(
            frame_upper, orient="horizontal", length=200, mode="determinate")
        progress_bar.pack(side="left")
        label_remaining = ttk.Label(
            frame_upper, text=self.get_remaining_time())
        label_remaining.pack(side="left")
        frame_lower = ttk.Frame(frame)
        frame_lower.pack()
        button_start = ttk.Button(
            frame_lower, text="Start", command=self.start)
        button_start.pack(side="left")
        button_pause = ttk.Button(
            frame_lower, text="Pause", command=self.pause)
        button_pause["state"] = "disabled"
        button_pause.pack(side="left")
        button_termiante = ttk.Button(
            frame_lower, text="Terminate", command=self.terminate)
        button_termiante["state"] = "disabled"
        button_termiante.pack(side="left")
        return frame, button_start, button_pause, button_termiante, progress_bar, label_remaining

    def get_remaining_time(self):
        """
        Get the remaining time.
        """
        remaining_time = int(self.time_per_iteration * (self.num - self.i - 1))
        if remaining_time <= 0:
            return "--:--:--"
        return str(timedelta(seconds=remaining_time))

    def start(self):
        """
        Start the task loop in a thread.
        """
        if self.status != RUNNING:
            self.status = RUNNING
            self.label_remaining.config(text=self.get_remaining_time())
            self.progress_bar["value"] = self.i / self.num * 100
            self.button_start["state"] = "disabled"
            self.button_pause["state"] = "normal"
            self.button_terminate["state"] = "normal"
            Thread(target=self.task_loop).start()

    def task_loop(self):
        """
        Loop that runs the user-customized task.
        """
        while self.status == RUNNING and self.i < self.num:
            time_start = time()
            self.task()
            time_end = time()
            self.time_per_iteration = (
                self.time_per_iteration * self.i + time_end - time_start) / (self.i + 1)
            self.label_remaining.config(text=self.get_remaining_time())
            self.i += 1
            self.progress_bar["value"] = self.i / self.num * 100
        if self.status == RUNNING:
            self.reset()
            self.label_remaining.config(text="Done!")
        elif self.status == TERMINATING:
            self.reset()
        elif self.status == PAUSING:
            self.button_start["state"] = "normal"
            self.status = PAUSED

    def task(self):
        """
        Individual task to be run in a loop. This can be customized and
        overwritten by users. Make sure to use self.i as the loop counter.
        """
        print(self.i)
        sleep(5)

    def reset(self):
        """
        Reset the task to the initial state.
        """
        self.status = TERMINATED
        self.i = 0
        self.time_per_iteration = 0
        self.button_terminate["state"] = "disabled"
        self.button_pause["state"] = "disabled"
        self.button_start["state"] = "normal"
        self.button_start.config(text="Start")
        self.progress_bar["value"] = 0
        self.label_remaining.config(text=self.get_remaining_time())

    def pause(self):
        """
        Pause the task.
        """
        self.status = PAUSING
        self.button_pause["state"] = "disabled"
        self.button_start.config(text="Resume")

    def terminate(self):
        """
        Terminate the task.
        """
        if self.status == PAUSED:
            self.reset()
        self.status = TERMINATING
        self.button_pause["state"] = "disabled"
        self.button_terminate["state"] = "disabled"
