import json
import os
import logging

class StorageManager:
    def __init__(self, filepath='data.json'):
        self.filepath = filepath
        self.logger = logging.getLogger(self.__class__.__name__)
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as file:
                    self.logger.info("Loading data from JSON file.")
                    return json.load(file)
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON decode error: {e}")
                return {}
        self.logger.info("No existing data file found, starting with empty data.")
        return {}

    def save_data(self):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
                self.logger.info("Data saved to JSON file.")
        except Exception as e:
            self.logger.error(f"Failed to save data: {e}")

    def add_group(self, group_name):
        if group_name not in self.data:
            self.data[group_name] = {}
            self.save_data()
            self.logger.info(f"Group '{group_name}' added.")
            return True
        self.logger.warning(f"Group '{group_name}' already exists.")
        return False

    def delete_group(self, group_name):
        if group_name in self.data:
            del self.data[group_name]
            self.save_data()
            self.logger.info(f"Group '{group_name}' deleted.")
            return True
        self.logger.error(f"Group '{group_name}' not found for deletion.")
        return False

    def add_key(self, group_name, key_name, key_value):
        if group_name in self.data and key_name not in self.data[group_name]:
            self.data[group_name][key_name] = key_value
            self.save_data()
            self.logger.info(f"Key '{key_name}' added to group '{group_name}'.")
            return True
        self.logger.error(f"Failed to add key '{key_name}' to group '{group_name}'.")
        return False

    def delete_key(self, group_name, key_name):
        if group_name in self.data and key_name in self.data[group_name]:
            del self.data[group_name][key_name]
            self.save_data()
            self.logger.info(f"Key '{key_name}' deleted from group '{group_name}'.")
            return True
        self.logger.error(f"Failed to delete key '{key_name}' from group '{group_name}'.")
        return False

    def modify_key(self, group_name, key_name, new_value):
        if group_name in self.data and key_name in self.data[group_name]:
            self.data[group_name][key_name] = new_value
            self.save_data()
            self.logger.info(f"Key '{key_name}' in group '{group_name}' modified.")
            return True
        self.logger.error(f"Failed to modify key '{key_name}' in group '{group_name}'.")
        return False

    def get_data(self):
        return self.data

    def generate_unique_key_name(self, group_name):
        i = 1
        while f"key_{i}" in self.data.get(group_name, {}):
            i += 1
        return f"key_{i}"

    def add_auto_key(self, group_name):
        if group_name in self.data:
            key_name = self.generate_unique_key_name(group_name)
            self.data[group_name][key_name] = ""
            self.save_data()
            self.logger.info(f"Automatically generated key '{key_name}' added to group '{group_name}'.")
            return key_name
        self.logger.error(f"Failed to add auto key to group '{group_name}'. Group does not exist.")
        return None
