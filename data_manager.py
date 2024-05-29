import json
from utils import starts_and_ends_with, convert_number, is_valid_json_list_or_dict
from typing import Union

# Função para tratar o caminho fornecido, dividindo-o em partes e convertendo strings, números e JSON válidos
def path_treatment(path):
    keys = path.split("/")  # Divide o caminho em partes
    for i, key in enumerate(keys):
        if starts_and_ends_with(key, '"'):
            keys[i] = key.strip('"')  # Remove aspas duplas ao redor da chave
        elif starts_and_ends_with(key, "'"):
            keys[i] = key.strip("'")  # Remove aspas simples ao redor da chave
        elif key.isdigit():
            keys[i] = convert_number(key)  # Converte a chave para número, se for dígito
        elif is_valid_json_list_or_dict(key):
            keys[i] = json.loads(key)  # Converte JSON válido em objeto Python
    return keys

# Função para substituir um item em uma estrutura de dados complexa (lista, dicionário, etc.) com base no caminho fornecido
def complex_data_item_replacer(data: Union[list, str, int, float], path: str, new_value: any, false_if_not_found: bool=False):
    keys = path_treatment(path)  # Trata o caminho para obter a lista de chaves

    # Caso especial para quando a estrutura de dados é simples e corresponde à chave final
    if data == keys[-1] and len(keys) == 1:
        data = new_value
        return data
    
    # Percorre as chaves no caminho
    for key in keys:
        if isinstance(data, list):  # Se a estrutura atual for uma lista
            for i, item in enumerate(data):
                if item == key:
                    if item == keys[-1]:  # Se for a última chave, substitui o valor
                        data[i] = new_value
                    else:
                        keys.pop(0)  # Remove a primeira chave já processada
                        keys = [f"{key}" if not isinstance(key, str) else key for key in keys]  # Formata as chaves restantes
                        path = "/".join(keys)  # Recria o caminho
                        complex_data_item_replacer(data[i], path, new_value)  # Chamada recursiva para a próxima parte do caminho
                    return data
                
        elif isinstance(data, dict):  # Se a estrutura atual for um dicionário
            for dict_key, value in data.items():
                if dict_key == key:
                    if dict_key == keys[-1]:  # Se for a última chave, substitui o valor
                        data[dict_key] = new_value
                    else:
                        keys.pop(0)  # Remove a primeira chave já processada
                        keys = [f"{key}" if not isinstance(key, str) else key for key in keys]  # Formata as chaves restantes
                        path = "/".join(keys)  # Recria o caminho
                        complex_data_item_replacer(data[dict_key], path, new_value)  # Chamada recursiva para a próxima parte do caminho
                    return data
                
    if false_if_not_found:  # Se o item não for encontrado e false_if_not_found for True, retorna False
        return False
    return data  # Retorna a estrutura original se o item não for encontrado
