import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from .storage import StorageManager
from .windows.file_tree_window import FileTreeWindow
from .create_example_files import create_example_files
from .logging_config import setup_logging
import logging

class GroupManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Group and Key Management")

        self.style = ttk.Style()
        self.style.theme_use('clam')  # Initial theme

        setup_logging()
        self.logger = logging.getLogger(self.__class__.__name__)

        try:
            self.storage = StorageManager()
            self.groups = self.storage.get_data()
            create_example_files()  # Create example files in 'work' directory
            self.create_widgets()
            self.update_group_listboxes()
        except Exception as e:
            self.logger.error(f"Error during initialization: {e}")
            messagebox.showerror("Error", "An error occurred during the initialization of the application.")

    def create_widgets(self):
        self.create_theme_selector()
        self.create_group_frame()
        self.create_key_frame()
        self.create_management_frame()

    def create_theme_selector(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill=tk.X)

        ttk.Label(frame, text="Choose a theme:").pack(side=tk.LEFT, padx=5)
        self.theme_selector = ttk.Combobox(frame, values=self.style.theme_names(), state="readonly")
        self.theme_selector.set(self.style.theme_use())
        self.theme_selector.pack(side=tk.LEFT, padx=5)
        self.theme_selector.bind("<<ComboboxSelected>>", self.change_theme)

    def change_theme(self, event):
        selected_theme = self.theme_selector.get()
        self.logger.info(f"Changing theme to: {selected_theme}")
        self.style.theme_use(selected_theme)

    def create_group_frame(self):
        frame1 = ttk.LabelFrame(self.root, text="Create a group", padding="10")
        frame1.pack(padx=10, pady=10, fill=tk.X)

        ttk.Label(frame1, text="Group name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.group_name_entry = ttk.Entry(frame1)
        self.group_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(frame1, text="Create group", command=self.create_group).grid(row=0, column=2, padx=5, pady=5)

    def create_key_frame(self):
        frame2 = ttk.LabelFrame(self.root, text="Create key", padding="10")
        frame2.pack(padx=10, pady=10, fill=tk.X)

        ttk.Label(frame2, text="Group:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.group_listbox = tk.Listbox(frame2, height=5)
        self.group_listbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.EW)
        self.add_scrollbar(self.group_listbox, frame2, 1, 2)

        ttk.Label(frame2, text="Key name:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.key_name_entry = ttk.Entry(frame2)
        self.key_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)
        ttk.Label(frame2, text="Text value:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.key_value_entry = ttk.Entry(frame2)
        self.key_value_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)
        ttk.Button(frame2, text="Create key", command=self.create_key).grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        ttk.Button(frame2, text="Create key with file", command=self.open_file_tree_window).grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        ttk.Button(frame2, text="Create an auto key", command=self.create_auto_key).grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    def create_management_frame(self):
        frame3 = ttk.LabelFrame(self.root, text="Group and key management", padding="10")
        frame3.pack(padx=10, pady=10, fill=tk.X)

        ttk.Label(frame3, text="Groups:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.manage_group_listbox = tk.Listbox(frame3, height=5)
        self.manage_group_listbox.grid(row=1, column=0, padx=5, pady=5, sticky=tk.EW)
        self.add_scrollbar(self.manage_group_listbox, frame3, 1, 1)
        self.manage_group_listbox.bind("<<ListboxSelect>>", self.display_keys)
        ttk.Button(frame3, text="Delete group", command=self.delete_group).grid(row=2, column=0, padx=5, pady=5)

        ttk.Label(frame3, text="Keys in the selected group:").grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.key_listbox = tk.Listbox(frame3, height=5)
        self.key_listbox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        self.add_scrollbar(self.key_listbox, frame3, 1, 2)
        self.key_listbox.bind("<<ListboxSelect>>", self.display_key_value)
        ttk.Button(frame3, text="Delete key", command=self.delete_key).grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(frame3, text="Modify key", command=self.modify_key).grid(row=3, column=1, padx=5, pady=5)

    def add_scrollbar(self, listbox, frame, row, col):
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=listbox.yview)
        scrollbar.grid(row=row, column=col, sticky="ns")
        listbox.config(yscrollcommand=scrollbar.set)

    def create_group(self):
        group_name = self.group_name_entry.get().strip()
        if not group_name:
            self.logger.warning("Group name cannot be empty.")
            messagebox.showerror("Error", "Group name cannot be empty.")
            return

        if self.storage.add_group(group_name):
            self.groups = self.storage.get_data()
            self.update_group_listboxes()
            self.logger.info(f"Group '{group_name}' created successfully.")
            messagebox.showinfo("Success", f"Group '{group_name}' created successfully.")
        else:
            self.logger.error(f"Group '{group_name}' already exists.")
            messagebox.showerror("Error", f"Group '{group_name}' already exists.")

    def create_key(self):
        group_name = self.group_listbox.get(tk.ACTIVE)
        key_name = self.key_name_entry.get().strip()
        key_value = self.key_value_entry.get().strip()
        if not group_name or not key_name or not key_value:
            self.logger.warning("All fields must be filled to create a key.")
            messagebox.showerror("Error", "Please fill in all fields correctly.")
            return

        if self.storage.add_key(group_name, key_name, key_value):
            self.groups = self.storage.get_data()
            self.display_keys()
            self.logger.info(f"Key '{key_name}' created successfully in group '{group_name}'.")
            messagebox.showinfo("Success", f"Key '{key_name}' created successfully in group '{group_name}'.")
        else:
            self.logger.error(f"Key '{key_name}' already exists in group '{group_name}'.")
            messagebox.showerror("Error", f"Key '{key_name}' already exists in group '{group_name}'.")

    def create_auto_key(self):
        group_name = self.group_listbox.get(tk.ACTIVE)
        if not group_name:
            self.logger.warning("Group must be selected to create an auto key.")
            messagebox.showerror("Error", "Please select a group.")
            return

        key_name = self.storage.add_auto_key(group_name)
        if key_name:
            self.groups = self.storage.get_data()
            self.display_keys()
            self.logger.info(f"Automatically generated key '{key_name}' created successfully in group '{group_name}'.")
            messagebox.showinfo("Success", f"Automatically generated key '{key_name}' created successfully in group '{group_name}'.")
        else:
            self.logger.error(f"Failed to create an automatically generated key in group '{group_name}'.")

    def open_file_tree_window(self):
        FileTreeWindow(self.root, self.storage, self.groups)

    def delete_group(self):
        group_name = self.manage_group_listbox.get(tk.ACTIVE)
        if not group_name:
            self.logger.warning("No group selected for deletion.")
            messagebox.showerror("Error", "Please select a group.")
            return

        if messagebox.askyesno("Confirmation", f"Do you really want to delete the group '{group_name}'?"):
            if self.storage.delete_group(group_name):
                self.groups = self.storage.get_data()
                self.update_group_listboxes()
                self.key_listbox.delete(0, tk.END)
                self.logger.info(f"Group '{group_name}' deleted successfully.")
                messagebox.showinfo("Success", f"Group '{group_name}' deleted successfully.")
            else:
                self.logger.error(f"Group '{group_name}' not found for deletion.")
                messagebox.showerror("Error", f"Group '{group_name}' not found.")

    def delete_key(self):
        group_name = self.manage_group_listbox.get(tk.ACTIVE)
        key_name = self.key_listbox.get(tk.ACTIVE)
        if not group_name or not key_name:
            self.logger.warning("No group or key selected for deletion.")
            messagebox.showerror("Error", "Please select a group and a key.")
            return

        if messagebox.askyesno("Confirmation", f"Do you really want to delete the key '{key_name}'?"):
            if self.storage.delete_key(group_name, key_name):
                self.groups = self.storage.get_data()
                self.display_keys()
                self.logger.info(f"Key '{key_name}' deleted successfully from group '{group_name}'.")
                messagebox.showinfo("Success", f"Key '{key_name}' deleted successfully.")
            else:
                self.logger.error(f"Key '{key_name}' not found for deletion in group '{group_name}'.")
                messagebox.showerror("Error", f"Key '{key_name}' not found.")

    def modify_key(self):
        group_name = self.manage_group_listbox.get(tk.ACTIVE)
        key_name = self.key_listbox.get(tk.ACTIVE)
        if not group_name or not key_name:
            self.logger.warning("No group or key selected for modification.")
            messagebox.showerror("Error", "Please select a group and a key.")
            return

        new_value = simpledialog.askstring("Modify key", f"New value for key '{key_name}':")
        if new_value is None:
            self.logger.info("Modification of key cancelled by user.")
            return  # The user canceled the input.

        if not new_value.strip():
            self.logger.warning("Key value cannot be empty.")
            messagebox.showerror("Error", "Key value cannot be empty.")
            return

        if self.storage.modify_key(group_name, key_name, new_value.strip()):
            self.groups = self.storage.get_data()
            self.display_key_value()
            self.logger.info(f"Key '{key_name}' in group '{group_name}' modified successfully.")
            messagebox.showinfo("Success", f"Key '{key_name}' modified successfully.")
        else:
            self.logger.error(f"Failed to modify key '{key_name}' in group '{group_name}'.")
            messagebox.showerror("Error", f"Failed to modify key '{key_name}'.")

    def display_keys(self, event=None):
        self.key_listbox.delete(0, tk.END)
        group_name = self.manage_group_listbox.get(tk.ACTIVE)
        if group_name in self.groups:
            for key in self.groups[group_name]:
                self.key_listbox.insert(tk.END, key)

    def display_key_value(self, event=None):
        group_name = self.manage_group_listbox.get(tk.ACTIVE)
        key_name = self.key_listbox.get(tk.ACTIVE)
        if group_name in self.groups and key_name in self.groups[group_name]:
            key_value = self.groups[group_name][key_name]
            messagebox.showinfo("Key value", f"Key: {key_name}\nValue: {key_value}")

    def update_group_listboxes(self):
        self.group_listbox.delete(0, tk.END)
        self.manage_group_listbox.delete(0, tk.END)
        for group in self.groups:
            self.group_listbox.insert(tk.END, group)
            self.manage_group_listbox.insert(tk.END, group)

if __name__ == "__main__":
    root = tk.Tk()
    app = GroupManagerApp(root)
    root.mainloop()
