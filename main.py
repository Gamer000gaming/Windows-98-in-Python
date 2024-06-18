from Programs import *
from Programs.windows import *
import tkinter as tk
import random

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("640x480")

    taskbar = Taskbar(root, width=640, height=30, bg="gray")
    
    window1 = Window(taskbar, root, "Fenêtre 1", width=100, height=100, bg="lightblue")
    window1.place(x=50, y=50)

    window2 = Window(taskbar, root, "Fenêtre 2", width=100, height=100, bg="lightcoral")
    window2.place(x=100, y=100)
    supertext.open_editor(window2)

    window3 = Window(taskbar, root, "Fenêtre 3", width=100, height=100, bg="lightcoral")
    window3.place(x=100, y=100)
    
    root.mainloop()
