from utils import path_treatment, update_data_by_path
from typing import Union
import json
import os

class DataManager:
    def __init__(self, data: Union[str, list, dict]):
        self.data = data
        self.modified_data = data

    def update_data(self, path, new_value):
        self.modified_data = update_data_by_path(self.modified_data, path, new_value, false_if_not_found=True)
    
    def save_data(self, filename, file_path=None):
        file = os.path.join(file_path, filename) if file_path else filename
        with open(file, 'w', encoding='utf8') as json_file:
            json.dump(self.modified_data, json_file, ensure_ascii=False, indent=4)
            
    @property
    def get_data(self) -> Union[str, list, dict]:
        return self.modified_data

class DataManagerPoint:
    def __init__(self, data_manager: DataManager, path: str):
        self.data_manager = data_manager
        self.path = path
    
    def update_value(self, new_value: Union[str, list, dict]):
        self.data_manager.update_data(self.path, new_value=new_value)

    def save_value(self, filename, file_path=None):
        self.data_manager.save_data(filename=filename, file_path=file_path)

    @property
    def get_value(self) -> Union[str, list, dict]:
        # Mostrar somente os dados a partir do endpoint
        data = self.data_manager.get_data
        path = self.path
        data_endpoint = self._data_masker(data, path)
        return data_endpoint
    
    def _data_masker(self, data: Union[str, list, dict], path: Union[str, list], false_if_not_found: bool=True, converted_path: bool=False) -> Union[str, list, dict]:
        def _recurse_data_masker(data, key, keys) -> Union[str, list, dict]:
            if key == keys[-1] and len(keys) == 1:
                return data[key]
            else:
                keys.pop(0)
                return self._data_masker(data[key], path=keys, converted_path=True)
                
        keys = path_treatment(path) if not converted_path else path

        for key in keys:
            if isinstance(data, list) or isinstance(data, dict):
                for i in range(len(data)) if isinstance(data, list) else data.keys():
                    if i == key:
                        return _recurse_data_masker(data, key, keys)
        if not path:
            return data
        elif false_if_not_found:
            return False
        return data

def minimum_data_manager(editor_data_manager: Union[DataManagerPoint, DataManager]) -> DataManager:
    if isinstance(editor_data_manager, DataManagerPoint):
        return editor_data_manager.data_manager
    return editor_data_manager