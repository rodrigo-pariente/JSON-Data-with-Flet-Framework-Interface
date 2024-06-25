from ui_components import ListDropdown, DictDropdown, ValueTextField
import json
from typing import Union
import flet as ft

class CustomError(Exception):
    pass

def path_treatment(path: str) -> list:
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

def update_data_by_path(data: Union[list, dict, str, int, float], path: str, new_value: any, false_if_not_found: bool=False, converted_path: bool=False) -> Union[list, dict, str, int, float]:
    def recurse_updater(data, key, keys):
        if key == keys[-1] and len(keys) == 1:
            data[key] = new_value
        else:
            keys.pop(0)
            update_data_by_path(data[key], path=keys, new_value=new_value, converted_path=True)
        return data
    
    keys = path_treatment(path) if not converted_path else path

    for key in keys:
        if isinstance(data, list) or isinstance(data, dict):
            for i in range(len(data)) if isinstance(data, list) else data.keys():
                if i == key:
                    return recurse_updater(data, key, keys)
    if not path:
        return new_value
    elif false_if_not_found:
        return False
    return data


def starts_and_ends_with(string: str, circumfix: str) -> str:
    return (string.startswith(circumfix) and string.endswith(circumfix))

def convert_number(number_str: str) -> Union[int, float, str]:
    try:
        return int(number_str)
    except ValueError:
        try:
            return float(number_str)
        except ValueError:
            return number_str
 
def all_options_primitive(dropdown: Union[ListDropdown, DictDropdown, ft.Dropdown]) -> bool: # Tem um jeito mais simples?
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

def only_one_option(list: ft.Dropdown) -> bool:
    if len(list.options) != 1:
        return False
    return True

def create_child_for_list(data: Union[str, list, dict]) -> ListDropdown: 
    return ListDropdown(data)

def create_child_for_dict(data: Union[str, list, dict]) -> DictDropdown:
    return DictDropdown(data)

def create_child_for_value(value: Union[str, list, dict]) -> ValueTextField:
    return ValueTextField(value)

def ui_component(data: Union[str, list, dict]) -> Union[ValueTextField, ListDropdown, DictDropdown]:
    if isinstance(data, list):
        return create_child_for_list(data)
    elif isinstance(data, dict):
        return create_child_for_dict(data)
    return create_child_for_value(data)