import tkinter as tk
from Programs import supertext
import random

class Taskbar(tk.Frame):
    def __init__(self, root, **kw):
        super().__init__(root, kw)
        self.pack_propagate(0)
        self.pack(side=tk.BOTTOM)
        
        self.start = tk.Button(self, text="Démarrer", command=self.new_window)
        self.start.pack(side=tk.LEFT)
        
        self.root = root

    def new_window(self):
        window1 = Window(self, self.root, "Fenêtre 36", width=100, height=100, bg="red")
        window1.place(x=50, y=50)
        supertext.open_editor(window1)
        if random.randint(1, 100) <= 5:
            tk.Frame(root, width=640, height=480, bg="blue").place(x=0,y=0)
            print("plantage")

    
class Window(tk.Frame):
    
    def __init__(self, taskbar: Taskbar, master=None, title_text="default", **kwargs):
        super().__init__(master, **kwargs)
        self.config(width=300, height=200)

        self.taskbar = taskbar

        self.title_text = title_text
        self.full_screen = False

        
        title = tk.Frame(self, bg="gray")
        title.pack(fill="x")

        self.title_label = tk.Label(title, text=title_text, bg="gray", padx=5)
        self.title_label.pack(side="left")
        
        title.bind("<ButtonPress-1>", self.on_press)
        title.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonPress-1>", self._lift)

        reduct = tk.Button(title, text="-", command=self.minimize_window)
        full_screen = tk.Button(title, text="[]", command=self.toggle_full_screen)
        close = tk.Button(title, text="X", command=self.close_window)

        close.pack(side=tk.RIGHT)
        full_screen.pack(side=tk.RIGHT)
        reduct.pack(side=tk.RIGHT)
                
        self.pack_propagate(0)

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.lift()

    def on_drag(self, event):
        delta_x = event.x - self.start_x
        delta_y = event.y - self.start_y
        x = self.winfo_x() + delta_x #Calcul de la différence X
        y = self.winfo_y() + delta_y #Calcul dela différence Y
        self.place(x=x, y=y)

    def minimize_window(self):
        self.place_forget()
        self.tbutton = tk.Button(self.taskbar, text=self.title_text)
        self.tbutton.pack(side=tk.LEFT)
        self.tbutton.bind("<ButtonPress-1>", self.restore)

    def toggle_full_screen(self):
        self.full_screen = not self.full_screen
        if self.full_screen:
            self.config(width=640, height=450)
            self.place(x=0, y=0)
        else:
            self.config(width=300, height=200)

    def close_window(self):
        self.destroy()
    
    def _lift(self, event):
        self.lift()

    def restore(self, event):
        self.place(x=50, y=50)
        self.tbutton.pack_forget()

class StartMenu:
    def __init__():
        pass
