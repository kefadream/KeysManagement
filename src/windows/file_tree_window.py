import tkinter as tk
from tkinter import messagebox, ttk
from .add_to_existing_key_window import AddToExistingKeyWindow
from .create_new_key_window import CreateNewKeyWindow
from ..logging_config import setup_logging
from ..directory_manager import DirectoryManager
import logging


class FileTreeWindow:
    def __init__(self, master, storage, groups):
        self.storage = storage
        self.groups = groups
        self.directory_manager = DirectoryManager()
        setup_logging()
        self.logger = logging.getLogger(self.__class__.__name__)

        self.window = tk.Toplevel(master)
        self.window.title("Création de clé avec fichier")

        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.window)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(self.frame)
        self.tree.heading("#0", text="Fichiers", anchor='w')
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.bind("<Button-3>", self.show_context_menu)

        self.context_menu = tk.Menu(self.window, tearoff=0)
        self.context_menu.add_command(label="Ajouter contenu à une clé existante", command=self.add_to_existing_key)
        self.context_menu.add_command(label="Créer une nouvelle clé avec ce contenu", command=self.create_new_key)

        try:
            self.load_directory(self.directory_manager.default_dir)
        except Exception as e:
            self.logger.error(f"Failed to load directory: {e}")
            messagebox.showerror("Erreur", f"Échec du chargement du répertoire: {e}")

        self.change_dir_button = ttk.Button(self.frame, text="Changer de répertoire", command=self.change_directory)
        self.change_dir_button.pack(pady=5)

    def load_directory(self, path):
        self.tree.delete(*self.tree.get_children())
        file_structure = self.directory_manager.load_directory(path)
        for file in file_structure:
            self.tree.insert('', 'end', text=file)

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def add_to_existing_key(self):
        selected_item = self.tree.selection()
        if selected_item:
            file_path = self.tree.item(selected_item[0], "text")
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                AddToExistingKeyWindow(self.window, self.storage, self.groups, content)
            except Exception as e:
                self.logger.error(f"Failed to read file '{file_path}': {e}")
                messagebox.showerror("Erreur", f"Échec de la lecture du fichier '{file_path}': {e}")

    def create_new_key(self):
        selected_item = self.tree.selection()
        if selected_item:
            file_path = self.tree.item(selected_item[0], "text")
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                CreateNewKeyWindow(self.window, self.storage, self.groups, content)
            except Exception as e:
                self.logger.error(f"Failed to read file '{file_path}': {e}")
                messagebox.showerror("Erreur", f"Échec de la lecture du fichier '{file_path}': {e}")

    def change_directory(self):
        new_dir = self.directory_manager.change_directory()
        try:
            self.load_directory(new_dir)
        except Exception as e:
            self.logger.error(f"Failed to change directory to '{new_dir}': {e}")
            messagebox.showerror("Erreur", f"Échec du changement de répertoire vers '{new_dir}': {e}")
