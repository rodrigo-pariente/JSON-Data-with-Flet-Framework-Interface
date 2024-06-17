from utils import path_treatment, update_data_by_path
import json
import os

class DataManager:
    def __init__(self, data):
        self.data = data
        self.modified_data = data

    def update_data(self, path, new_value):
        self.modified_data = update_data_by_path(self.modified_data, path, new_value, false_if_not_found=True)
    
    def save_data(self, filename, file_path=None):
        file = os.path.join(file_path, filename) if file_path else filename
        with open(file, 'w', encoding='utf8') as json_file:
            json.dump(self.modified_data, json_file, ensure_ascii=False, indent=4)
            
    @property
    def get_data(self):
        return self.modified_data

class DataManagerPoint:
    def __init__(self, data_manager: DataManager, path: str):
        self.data_manager = data_manager
        self.path = path
    
    def update_value(self, new_value):
        self.data_manager.update_data(self.path, new_value=new_value)

    def save_value(self, filename, file_path=None):
        self.data_manager.save_data(filename=filename, file_path=file_path)

    @property
    def get_value(self):
        # Mostrar somente os dados a partir do endpoint
        data = self.data_manager.get_data
        path = self.path
        data_endpoint = self._data_masker(data, path)
        return data_endpoint
    
    def _data_masker(self, data, path, false_if_not_found=True, converted_path=False):
        # Função recursiva auxiliar para mascarar os dados no caminho especificado
        def _recurse_data_masker(data, key, keys):
            # Se a chave atual for a última chave do caminho e não houver mais chaves
            if key == keys[-1] and len(keys) == 1:
                # Retorna o valor no caminho especificado
                return data[key]
            else:
                # Remove a chave atual e continua a busca recursiva
                keys.pop(0)
                return self._data_masker(data[key], path=keys, converted_path=True)
                
        # Trata o caminho, dividindo-o em chaves
        keys = path_treatment(path) if not converted_path else path

        # Itera sobre as chaves do caminho
        for key in keys:
            if isinstance(data, list) or isinstance(data, dict):
                # Itera sobre os índices se for uma lista, ou sobre as chaves se for um dicionário
                for i in range(len(data)) if isinstance(data, list) else data.keys():
                    if i == key:
                        return _recurse_data_masker(data, key, keys)

        # Retorna False se a opção false_if_not_found for True e a chave não for encontrada
        if false_if_not_found:
            return False
        # Retorna a estrutura de dados original se a chave não for encontrada
        return data

def minimum_data_manager(editor_data_manager):
    if isinstance(editor_data_manager, DataManagerPoint):
        return editor_data_manager.data_manager
    return editor_data_manager