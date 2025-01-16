import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import threading

text_widget = None
current_text = ""
undo_stack = []
redo_stack = []
file_path = False


def new_file():
    text_widget.delete('1.0', tk.END)
    update_text()


def open_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt"), ("Program files", "*.py"), ("No console programs", "*.pyw")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
        text_widget.delete('1.0', tk.END)
        text_widget.insert(tk.END, content)
        update_text()


def save_file():
    global file_path
    if not file_path:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("Program files", "*.py"),
                                                            ("No console programs", "*.pyw")])
    if file_path:
        content = text_widget.get('1.0', tk.END)
        with open(file_path, 'w') as file:
            file.write(content)

def undo():
    if undo_stack:
        global current_text
        redo_stack.append(current_text)
        current_text = undo_stack.pop()
        text_widget.delete('1.0', tk.END)
        text_widget.insert(tk.END, current_text)


def redo():
    if redo_stack:
        global current_text
        undo_stack.append(current_text)
        current_text = redo_stack.pop()
        text_widget.delete('1.0', tk.END)
        text_widget.insert(tk.END, current_text)


def update_text():
    global current_text
    new_text = text_widget.get('1.0', tk.END)
    if new_text != current_text:
        undo_stack.append(current_text)
        redo_stack.clear()
        current_text = new_text


def open(master=None, path=None):
    global text_widget

    master.title("Supertext Editor")
    
    frame = tk.Frame(master)
    frame.pack(fill=tk.BOTH, expand=True)

    notebook = ttk.Notebook(frame)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Création des onglets
    file_tab = ttk.Frame(notebook)
    edit_tab = ttk.Frame(notebook)
    view_tab = ttk.Frame(notebook)

    notebook.add(file_tab, text="Fichier")
    notebook.add(edit_tab, text="Éditer")
    notebook.add(view_tab, text="Affichage")

    # Boutons dans l'onglet Fichier
    new_button = tk.Button(file_tab, text="Nouveau", command=new_file)
    new_button.pack(side=tk.LEFT, padx=5, pady=5)
    open_button = tk.Button(file_tab, text="Ouvrir", command=open_file)
    open_button.pack(side=tk.LEFT, padx=5, pady=5)
    save_button = tk.Button(file_tab, text="Enregistrer", command=save_file)
    save_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Boutons dans l'onglet Éditer
    undo_button = tk.Button(edit_tab, text="Annuler", command=undo)
    undo_button.pack(side=tk.LEFT, padx=5, pady=5)
    redo_button = tk.Button(edit_tab, text="Rétablir", command=redo)
    redo_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Historique des modifications
    current_text = ""

    # Configuration des raccourcis clavier
    master.bind('<Control-z>', lambda event: undo())
    master.bind('<Control-y>', lambda event: redo)

    text_widget = tk.Text(view_tab, wrap=tk.WORD)
    text_widget.pack(expand=True, fill='both')

    if path:
        open_file(path)


def start_editor():
    root = tk.Tk()
    open(root)
    root.mainloop()


if __name__ == "__main__":
    threading.Thread(target=start_editor).start()
