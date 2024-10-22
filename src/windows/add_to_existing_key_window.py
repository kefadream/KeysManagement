import tkinter as tk
from tkinter import messagebox, ttk
import logging

class AddToExistingKeyWindow:
    def __init__(self, master, storage, groups, content):
        self.storage = storage
        self.groups = groups
        self.content = content
        self.logger = logging.getLogger(self.__class__.__name__)

        self.window = tk.Toplevel(master)
        self.window.title("Add content to an existing key")

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Select a group:").pack(padx=5, pady=5)
        self.group_selector = ttk.Combobox(frame, values=list(self.groups.keys()), state="readonly")
        self.group_selector.pack(padx=5, pady=5)
        self.group_selector.bind("<<ComboboxSelected>>", self.update_key_selector)

        ttk.Label(frame, text="Select a key:").pack(padx=5, pady=5)
        self.key_selector = ttk.Combobox(frame, state="readonly")
        self.key_selector.pack(padx=5, pady=5)

        ttk.Button(frame, text="Add content", command=self.add_content).pack(padx=5, pady=5)

    def update_key_selector(self, event):
        group_name = self.group_selector.get()
        if group_name in self.groups:
            self.key_selector.config(values=list(self.groups[group_name].keys()))

    def add_content(self):
        group_name = self.group_selector.get()
        key_name = self.key_selector.get()
        if group_name and key_name:
            try:
                self.storage.modify_key(group_name, key_name, self.content)
                messagebox.showinfo("Success", f"Content added to key '{key_name}' in group '{group_name}'.")
                self.window.destroy()
            except Exception as e:
                self.logger.error(f"Failed to add content to key '{key_name}' in group '{group_name}': {e}")
                messagebox.showerror("Error", f"Failed to add content to key '{key_name}' in group '{group_name}': {e}")
        else:
            messagebox.showerror("Error", "Please select a group and a key.")
