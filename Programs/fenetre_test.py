import tkinter as tk
import subprocess

class Window(tk.Frame):
    def __init__(self, master=None, title_text="default", bg_color="white", **kwargs):
        super().__init__(master, bg=bg_color, **kwargs)
        self.config(width=300, height=200)
        
        title_height = 20  # Hauteur de la barre de titre
        title = tk.Frame(self, bg="gray", height=title_height, width = 300)  # Définir la hauteur de la barre de titre
        title.pack(fill="x")

        self.title_label = tk.Label(title, text=title_text, bg="gray", padx=5)
        self.title_label.pack(side="left")
        
        title.bind("<ButtonPress-1>", self.on_press)
        title.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonPress-1>", self._lift)

        reduct = tk.Button(title, text="-", command=pass)
        full_screen = tk.Button(title, text="[]", command=pass)
        close = tk.Button(title, text="X", command=pass)

        close.pack(side=tk.RIGHT)
        full_screen.pack(side=tk.RIGHT)
        reduct.pack(side=tk.RIGHT)

        self.program_frame = tk.Frame(self, bg=bg_color)  
        self.program_frame.place(relx=0, rely=1, relwidth=1, relheight=1, anchor='sw')  # Modification ici

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.lift()

    def on_drag(self, event):
        delta_x = event.x - self.start_x
        delta_y = event.y - self.start_y
        x = self.winfo_x()

    def _lift(self, event):
        self.lift()
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")

    window1 = Window(root, "Fenêtre 1", bg_color="lightblue")  
    window1.place(x=50, y=50)  

    window2 = Window(root, "Fenêtre 2", bg_color="lightcoral")  
    window2.place(x=100, y=100)  

    taskbar = tk.Frame(root, width=400, height=10, bg="blue")
    taskbar.pack(side=tk.BOTTOM)

    def start_menu():
        menu = tk.Menu(taskbar, tearoff=0)
        program_list = [
            ("Exemple Tkinter", example_tk_program),
            # Ajoutez d'autres programmes Tkinter ici
        ]
        for program_name, program_function in program_list:
            menu.add_command(label=program_name, command=lambda f=program_function: run_tk_program(f, window1.program_frame))
        return menu

    start_button = tk.Menubutton(taskbar, text="Démarrer", menu=start_menu())
    start_button.pack(side=tk.LEFT)

    root.mainloop()
