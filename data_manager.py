from utils import path_treatment, update_data_by_path
import json

class DataManager:
    def __init__(self, data):
        self.data = data
        self.modified_data = data

    def update_data(self, path, new_value):
        self.modified_data = update_data_by_path(self.modified_data, path, new_value, false_if_not_found=True)
    
    @property
    def get_data(self):
        return self.modified_data

class DataManagerPoint:
    def __init__(self, data_manager: DataManager, path: str):
        self.data_manager = data_manager
        self.path = path
    
    def update_value(self, new_value):
        self.data_manager.update_data(self.path, new_value=new_value)

    @property
    def get_value(self):
        # Mostrar somente os dados a partir do endpoint
        data = self.data_manager.get_data
        path = self.path
        data_endpoint = self._data_masker(data, path)
        return data_endpoint
    
    def _data_masker(self, data, path, false_if_not_found=True, converted_path=False):
        keys = path_treatment(path) if not converted_path else path

        for key in keys:
            # Verifica se a estrutura de dados atual é uma lista
            if isinstance(data, list):
                for i, item in enumerate(data):
                    # Verifica se o item atual é igual à chave
                    if i == key:
                        # Se o item for a chave final, substitui pelo novo valor
                        if i == keys[-1] and len(keys) == 1:
                            return data[i]
                        else:
                            keys.pop(0)
                            return self._data_masker(data[i], path=keys, converted_path=True)
                        
            # Verifica se a estrutura de dados atual é um dicionário
            elif isinstance(data, dict):
                for dict_key, value in data.items():
                    # Verifica se a chave do dicionário atual é igual à chave
                    if dict_key == key:
                        # Se a chave do dicionário for a chave final, substitui pelo novo valor
                        if dict_key == keys[-1]:
                            return data[dict_key]
                        else:
                            keys.pop(0)
                            return self._data_masker(data[dict_key], path=keys, converted_path=True)

        # Retorna False se a opção false_if_not_found for True e a chave não for encontrada
        if false_if_not_found:
            return False