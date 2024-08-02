import os
from tkinter import filedialog

class DirectoryManager:
    def __init__(self, default_dir='work'):
        self.default_dir = default_dir
        self.ensure_default_directory()

    def ensure_default_directory(self):
        if not os.path.exists(self.default_dir):
            os.makedirs(self.default_dir)

    def load_directory(self, path):
        file_structure = []
        for root, dirs, files in os.walk(path):
            for name in files:
                file_structure.append(os.path.join(root, name))
        return file_structure

    def change_directory(self):
        new_dir = filedialog.askdirectory(initialdir=self.default_dir, title="Choose a directory")
        if new_dir:
            self.default_dir = new_dir
        return self.default_dir
