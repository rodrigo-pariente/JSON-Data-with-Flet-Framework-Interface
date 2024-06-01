from ui_components import ListDropdown, DictDropdown, ValueTextField
import json
from typing import Union

def path_treatment(path):
    # Divide o caminho em partes usando "/" como separador
    keys = path.split("/")
    
    # Itera sobre as partes do caminho
    for i, key in enumerate(keys):
        # Substitui as aspas simples por aspas duplas para garantir que o JSON seja válido
        key = key.replace("'", '"')
        
        # Remove as aspas duplas do início e do fim, se presentes
        if starts_and_ends_with(key, '"'):
            keys[i] = key.strip('"')
        
        # Converte números que estavam entre aspas em tipos numéricos
        if key.isdigit():
            keys[i] = convert_number(key)
        
        # Converte strings JSON válidas em estruturas de dados correspondentes
        if is_valid_json_list_or_dict(key):
            keys[i] = json.loads(key)
    
    return keys

def update_data_by_path(data: Union[list, dict, str, int, float], path: str, new_value: any, false_if_not_found: bool=False, converted_path: bool=False):
    keys = path_treatment(path) if not converted_path else path

    # Itera sobre as chaves no caminho
    for key in keys:
        # Verifica se a estrutura de dados atual é uma lista
        if isinstance(data, list):
            for i, item in enumerate(data):
                # Verifica se o item atual é igual à chave
                if i == key:
                    # Se o item for a chave final, substitui pelo novo valor
                    if i == keys[-1] and len(keys) == 1:
                        data[i] = new_value
                    else:
                        keys.pop(0)
                        update_data_by_path(data[i], path=keys, new_value=new_value, converted_path=True)
                    return data
                
        # Verifica se a estrutura de dados atual é um dicionário
        elif isinstance(data, dict):
            for dict_key in data.keys():
                # Verifica se a chave do dicionário atual é igual à chave
                if dict_key == key:
                    # Se a chave do dicionário for a chave final, substitui pelo novo valor
                    if dict_key == keys[-1]:
                        data[dict_key] = new_value
                    else:
                        keys.pop(0)
                        update_data_by_path(data[dict_key], path=keys, new_value=new_value, converted_path=True)
                    return data
                
    # Retorna False se a opção false_if_not_found for True e a chave não for encontrada
    if false_if_not_found:
        return False
    # Retorna a estrutura de dados original se a chave não for encontrada
    return data

def starts_and_ends_with(string: str, circumfix: str):
    return (string.startswith(circumfix) and string.endswith(circumfix))

def convert_number(number_str: str):
    try:
        return int(number_str)
    except ValueError:
        try:
            return float(number_str)
        except ValueError:
            return number_str
 
def all_options_primitive(dropdown) -> bool:
    for option in dropdown.options:
        if isinstance(dropdown, ListDropdown):
            if is_valid_json_list_or_dict(option.key) or isinstance(option.key, (list, dict)):
                return False
        else:
            if is_valid_json_list_or_dict(dropdown.dictionary[option.key]) or isinstance(dropdown.dictionary[option.key], (list, dict)):
                return False
    return True

def is_valid_json_list_or_dict(string: str) -> bool:
    try:
        data = json.loads(string)
        return isinstance(data, (list, dict))
    except (json.decoder.JSONDecodeError, TypeError):
        return False

def create_child_for_list(data) -> ListDropdown: 
    return ListDropdown(data)

def create_child_for_dict(data) -> DictDropdown:
    return DictDropdown(data)

def create_child_for_value(value) -> ValueTextField:
    return ValueTextField(value)

def ui_component(data):
    if isinstance(data, list):
        return create_child_for_list(data)
    elif isinstance(data, dict):
        return create_child_for_dict(data)
    return create_child_for_value(data)