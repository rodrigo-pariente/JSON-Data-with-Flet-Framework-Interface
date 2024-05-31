from utils import update_data_by_path

class DataManager:
    def __init__(self, data):
        self.data = data
        self._modified_data = data

    def update_data(self, path, new_value):
        self._modified_data = update_data_by_path(self._modified_data, path, new_value)
    
    def get_data(self):
        