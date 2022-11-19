from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class Plot:
    def __init__(self, parent, figsize=(10, 4), dpi=60):
        self.parent = parent
        self.figsize = figsize
        self.dpi = dpi
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(side="left")
        self.facecolor = "#F0F0F0"
        self.ax, self.canvas = self.set_frame()

    def set_frame(self):
        fig = Figure(figsize=self.figsize, dpi=self.dpi, facecolor=self.facecolor)
        ax = fig.add_subplot(111)
        ax.set_facecolor(self.facecolor)
        canvas = FigureCanvasTkAgg(fig, master=self.parent)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, self.parent)
        toolbar.update()
        canvas.get_tk_widget().pack()
        return ax, canvas

    def plot(self, *args, **kwargs):
        self.ax.clear()
        self.ax.plot(*args, **kwargs)
        self.canvas.draw()

    def clear(self):
        self.ax.clear()
        self.canvas.draw()
