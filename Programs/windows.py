import tkinter as tk
import random
import os
import importlib.util

class Taskbar(tk.Frame):
    def __init__(self, root, **kw):
        super().__init__(root, kw)
        self.pack_propagate(0)
        self.pack(side=tk.BOTTOM)

        self.root = root

        self.start_menu = None
        self.start_button = tk.Button(self, text="Démarrer", command=self.toggle_start_menu)
        self.start_button.pack(side=tk.LEFT)

    def toggle_start_menu(self):
        if self.start_menu and self.start_menu.winfo_ismapped():
            self.start_menu.place_forget()
        else:
            self.start_menu = StartMenu(self.root, self)
            self.start_menu.place(x=0, y=self.winfo_height())

    def execute_program(self, program_name):
        try:
            # Essayer d'importer et d'exécuter dynamiquement le programme
            module = importlib.import_module(f"Programs.{program_name}")
            window = Window(self, self.root, program_name, width=100, height=100, bg='red')
            module.open(window)
            window.place(x=0, y=0)
            
        except Exception as e:
            print(f"Erreur lors de l'exécution de {program_name} : {e}")


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
        x = self.winfo_x() + delta_x
        y = self.winfo_y() + delta_y
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

    def title(self, title):
        self.title_text = title


class StartMenu(tk.Frame):
    def __init__(self, root, taskbar, **kwargs):
        super().__init__(root, bg="white", **kwargs)
        self.taskbar = taskbar
        self.config(width=200, height=300)

        programs = self.get_program_list()
        for program_name in programs:
            btn = tk.Button(self, text=program_name, command=lambda name=program_name: self.taskbar.execute_program(name))
            btn.pack(fill=tk.X)

    @staticmethod
    def get_program_list():
        program_dir = "./Programs"
        if not os.path.exists(program_dir):
            return []
        programs = [f[:-3] for f in os.listdir(program_dir) if f.endswith(".py") and not f.startswith("__")]
        return programs


# Exemple d'initialisation
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    taskbar = Taskbar(root)
    root.mainloop()
