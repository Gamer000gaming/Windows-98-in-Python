import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import requests

# Réassigner la fonction open native
open_file = open

def open(window):
    ProgramManager(window)


class ProgramManager:
    def __init__(self, master):
        self.master = master
        self.master.config(width=400, height=300)
        self.program_dir = "./Programs"
        self.repo_url = "https://api.github.com/repos/Gamer000gaming/Win98-app-repo/contents/"

        if not os.path.exists(self.program_dir):
            os.makedirs(self.program_dir)

        self.create_widgets()
        self.refresh_program_list()

    def create_widgets(self):
        self.title_label = tk.Label(self.master, text="Gestionnaire de programmes", bg="white")
        self.title_label.pack(fill=tk.X, pady=5)

        self.program_listbox = tk.Listbox(self.master, selectmode=tk.SINGLE)
        self.program_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(fill=tk.X, pady=5)

        self.install_button = tk.Button(self.button_frame, text="Installer localement", command=self.install_program)
        self.uninstall_button = tk.Button(self.button_frame, text="Désinstaller", command=self.uninstall_program)
        self.online_button = tk.Button(self.button_frame, text="Explorer la bibliothèque", command=self.explore_library)

        self.install_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        self.uninstall_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        self.online_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

    def refresh_program_list(self):
        """Recharge la liste des programmes installés."""
        self.program_listbox.delete(0, tk.END)
        programs = [f[:-3] for f in os.listdir(self.program_dir) if f.endswith(".py") and not f.startswith("__")]
        for program in programs:
            self.program_listbox.insert(tk.END, program)

    def install_program(self):
        """Permet à l'utilisateur de sélectionner et d'installer un programme."""
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers Python", "*.py")])
        if not file_path:
            return

        try:
            file_name = os.path.basename(file_path)
            dest_path = os.path.join(self.program_dir, file_name)

            if os.path.exists(dest_path):
                messagebox.showwarning("Installation", f"Le programme '{file_name}' est déjà installé.")
                return

            shutil.copy(file_path, dest_path)
            messagebox.showinfo("Installation", f"Le programme '{file_name}' a été installé avec succès.")
            self.refresh_program_list()

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'installation : {e}")

    def uninstall_program(self):
        """Désinstalle le programme sélectionné."""
        selected_index = self.program_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Désinstallation", "Veuillez sélectionner un programme à désinstaller.")
            return

        program_name = self.program_listbox.get(selected_index)
        file_path = os.path.join(self.program_dir, program_name + ".py")

        try:
            os.remove(file_path)
            messagebox.showinfo("Désinstallation", f"Le programme '{program_name}' a été désinstallé avec succès.")
            self.refresh_program_list()

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la désinstallation : {e}")

    def explore_library(self):
        """Explore la bibliothèque en ligne et affiche un menu déroulant pour sélectionner un programme."""
        try:
            response = requests.get(self.repo_url)
            response.raise_for_status()

            programs = [file["name"] for file in response.json() if file["name"].endswith(".py")]
            if not programs:
                messagebox.showinfo("Bibliothèque", "Aucun programme disponible dans la bibliothèque.")
                return

            self.show_dropdown(programs)

        except requests.RequestException as e:
            messagebox.showerror("Erreur", f"Impossible d'accéder à la bibliothèque en ligne : {e}")

    def show_dropdown(self, programs):
        """Affiche un menu déroulant pour sélectionner un programme."""
        dropdown_window = tk.Toplevel(self.master)
        dropdown_window.title("Sélectionner un programme")
        dropdown_window.geometry("300x100")

        label = tk.Label(dropdown_window, text="Choisissez un programme à installer :")
        label.pack(pady=5)

        selected_program = tk.StringVar(dropdown_window)
        selected_program.set("Sélectionnez un programme")

        dropdown = tk.OptionMenu(dropdown_window, selected_program, *programs)
        dropdown.pack(pady=5)

        install_button = tk.Button(dropdown_window, text="Installer", command=lambda: self.download_program(selected_program.get(), dropdown_window))
        install_button.pack(pady=5)

    def download_program(self, program_name, dropdown_window):
        """Télécharge un programme depuis la bibliothèque."""
        if program_name == "Sélectionnez un programme":
            messagebox.showwarning("Téléchargement", "Veuillez sélectionner un programme.")
            return

        try:
            program_url = f"https://raw.githubusercontent.com/Gamer000gaming/Win98-app-repo/main/{program_name}"
            response = requests.get(program_url)
            response.raise_for_status()

            dest_path = os.path.join(self.program_dir, program_name)
            with open_file(dest_path, "w", encoding="utf-8") as f:  # Ajout de l'encodage explicite
                f.write(response.text)

            messagebox.showinfo("Téléchargement", f"Le programme '{program_name}' a été installé avec succès.")
            self.refresh_program_list()
            dropdown_window.destroy()

        except requests.RequestException as e:
            messagebox.showerror("Erreur", f"Impossible de télécharger le programme : {e}")
        except UnicodeEncodeError as e:
            messagebox.showerror("Erreur", f"Problème d'encodage lors de l'écriture du fichier : {e}")
