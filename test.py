from tkinter import *
from threading import Thread
from time import sleep

def hello(event):
    t = Thread(target=task)
    t.start()
    print("Single Click, Button-l") 
def task():
    sleep(0.5)
    widget.event_generate("<<Hello>>")
def quit(event):                           
    print("Double Click, so let's stop") 
    import sys; sys.exit() 

root = Tk()

widget = Button(root, text='Mouse Clicks')
widget.pack()
widget.bind('<Button-1>', hello)
widget.bind('<Double-1>', quit) 
root.bind('<<Hello>>', lambda e: print('Hello World!'))
widget.mainloop()