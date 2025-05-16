import json
import os

class FileHandler:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = os.path.join(self.base_dir, '../data')
        self.file_map = {
            "cars": "cars.json",
            "users": "users.json",
            "reservations": "reservations.json"
        }

    def get_path(self, data_type):
        if data_type not in self.file_map:
            raise ValueError(f"Unsupported data type: {data_type}")
        return os.path.join(self.base_dir, self.file_map[data_type])

    def load_data(self, data_type):
        path = self.get_path(data_type)
        if not os.path.exists(path):
            return []
        with open(path, "r") as file:
            return json.load(file)

    def save_data(self, data_type, data):
        path = self.get_path(data_type)
        with open(path, "w") as file:
            json.dump(data, file, indent=4)
