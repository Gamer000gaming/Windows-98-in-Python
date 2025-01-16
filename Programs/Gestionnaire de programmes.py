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
        self.online_button = tk.Button(self.button_frame, text="Explorer la bibliothèque", command=self.explore_repo_folder)

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

    def explore_repo_folder(self):
        """Explore les dossiers du repo et affiche un menu avec les fichiers disponibles."""
        self.load_repo_folder()

    def load_repo_folder(self, folder_path=""):
        """Charge le contenu d'un dossier du repo et affiche les fichiers .py."""
        try:
            response = requests.get(f"{self.repo_url}{folder_path}")
            response.raise_for_status()

            items = response.json()
            files = [item["path"] for item in items if item["type"] == "file" and item["path"].endswith(".py")]
            folders = [item["path"] for item in items if item["type"] == "dir"]

            if not files and not folders:
                messagebox.showinfo("Bibliothèque", "Aucun fichier ou dossier disponible.")
                return

            self.show_folder_contents(files, folders, folder_path)

        except requests.RequestException as e:
            messagebox.showerror("Erreur", f"Impossible d'accéder au dossier du repo : {e}")

    def show_folder_contents(self, files, folders, folder_path):
        """Affiche les fichiers et dossiers d'un dossier du repo."""
        dropdown_window = tk.Toplevel(self.master)
        dropdown_window.title(f"Explorer le dossier {folder_path if folder_path else 'racine'}")
        dropdown_window.geometry("400x500")

        label = tk.Label(dropdown_window, text="Choisissez un fichier Python à télécharger ou naviguez dans un dossier :")
        label.pack(pady=5)

        selected_item = tk.StringVar(dropdown_window)
        selected_item.set("Sélectionnez un fichier")

        file_listbox = tk.Listbox(dropdown_window, selectmode=tk.SINGLE)
        file_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        for file in files:
            file_listbox.insert(tk.END, file)

        folder_listbox = tk.Listbox(dropdown_window, selectmode=tk.SINGLE)
        folder_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        for folder in folders:
            folder_listbox.insert(tk.END, folder)

        download_button = tk.Button(dropdown_window, text="Télécharger", command=lambda: self.download_file(file_listbox.get(tk.ACTIVE), dropdown_window))
        download_button.pack(pady=5)

        navigate_button = tk.Button(dropdown_window, text="Naviguer", command=lambda: self.navigate_folder(folder_listbox.get(tk.ACTIVE), dropdown_window))
        navigate_button.pack(pady=5)

    def navigate_folder(self, folder_name, dropdown_window):
        """Navigue dans un dossier sélectionné."""
        if not folder_name:
            messagebox.showwarning("Navigation", "Veuillez sélectionner un dossier.")
            return

        folder_path = folder_name
        self.load_repo_folder(folder_path)
        dropdown_window.destroy()

    def download_file(self, file_path, dropdown_window):
        """Télécharge un fichier depuis le repo."""
        if not file_path:
            messagebox.showwarning("Téléchargement", "Veuillez sélectionner un fichier.")
            return

        try:
            file_url = f"https://raw.githubusercontent.com/Gamer000gaming/Win98-app-repo/main/{file_path}"
            response = requests.get(file_url)
            response.raise_for_status()

            file_name = os.path.basename(file_path)
            dest_path = os.path.join(self.program_dir, file_name)
            with open_file(dest_path, "w", encoding="utf-8") as f:
                f.write(response.text)

            messagebox.showinfo("Téléchargement", f"Le fichier '{file_name}' a été téléchargé avec succès.")
            self.refresh_program_list()
            dropdown_window.destroy()

        except requests.RequestException as e:
            messagebox.showerror("Erreur", f"Impossible de télécharger le fichier : {e}")
        except UnicodeEncodeError as e:
            messagebox.showerror("Erreur", f"Problème d'encodage lors de l'écriture du fichier : {e}")
