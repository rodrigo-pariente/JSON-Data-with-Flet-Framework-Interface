from utils import update_data_by_path, path_treatment
from typing import Union, Any
import json

class DataManager:
    def __init__(self, data: Union[list, dict, str, int, float]):
        self.original_data = data
        self.data = data

    def update_data(self, path: str, new_value: Any):
        self.data = update_data_by_path(self.data, path, new_value)
    
    def save_data(self, file_path: str, data_path: str = None):
        data_to_save = self.data if data_path is None else self.get_data(data_path)
        with open(file_path, "w", encoding="utf8") as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)

    def get_data(self, path: str = None) -> Any:
        if path is None:
            return self.data
        return self._get_data_by_path(self.data, path)

    def reset_data(self):
        self.data = self.original_data

    def _get_data_by_path(self, data: Union[list, dict], path: str) -> any:
        keys = path_treatment(path)
        current_data = data
        
        for key in keys:
            if isinstance(current_data, list):
                try:
                    key = int(key)  # Tentar converter a chave para um índice inteiro
                except (ValueError, TypeError):
                    pass  # Se não puder converter, assume que é uma string

                try:
                    current_data = current_data[key]
                except (IndexError, KeyError, TypeError):
                    return None  # Se não conseguir acessar, retorna None
            
            elif isinstance(current_data, dict):
                try:
                    current_data = current_data[key]
                except KeyError:
                    return None  # Se a chave não existir no dicionário, retorna None
            
            else:
                return None  # Se o tipo de dado não for suportado (como int, str, etc.), retorna None
        
        return current_data 

class DataManagerPoint:
    def __init__(self, data_manager: DataManager, path: str):
        self.data_manager = data_manager
        self.path = path

    def update_value(self, new_value: Any):
        self.data_manager.update_data(self.path, new_value)

    def get_value(self) -> Any:
        return self.data_manager.get_data(self.path)

    def save(self, file_path: str):
        self.data_manager.save_data(file_path, self.path)