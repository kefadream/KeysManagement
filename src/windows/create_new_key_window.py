import tkinter as tk
from tkinter import messagebox, ttk
import logging

class CreateNewKeyWindow:
    def __init__(self, master, storage, groups, content):
        self.storage = storage
        self.groups = groups
        self.content = content
        self.logger = logging.getLogger(self.__class__.__name__)

        self.window = tk.Toplevel(master)
        self.window.title("Create a new key with content")

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Select a group:").pack(padx=5, pady=5)
        self.group_selector = ttk.Combobox(frame, values=list(self.groups.keys()), state="readonly")
        self.group_selector.pack(padx=5, pady=5)

        ttk.Label(frame, text="New key name:").pack(padx=5, pady=5)
        self.key_name_entry = ttk.Entry(frame)
        self.key_name_entry.pack(padx=5, pady=5)

        ttk.Button(frame, text="Create key", command=self.create_key).pack(padx=5, pady=5)

    def create_key(self):
        group_name = self.group_selector.get()
        key_name = self.key_name_entry.get().strip()
        if group_name and key_name:
            try:
                self.storage.add_key(group_name, key_name, self.content)
                messagebox.showinfo("Success", f"Key '{key_name}' successfully created in group '{group_name}'.")
                self.window.destroy()
            except Exception as e:
                self.logger.error(f"Failed to create key '{key_name}' in group '{group_name}': {e}")
                messagebox.showerror("Error", f"Failed to create key '{key_name}' in group '{group_name}': {e}")
        else:
            messagebox.showerror("Error", "Please select a group and enter a key name.")
