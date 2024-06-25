from typing import Union
import json
from ui_components import ListDropdown, DictDropdown
import flet as ft

def data_parsing(not_parsed: str):
    pass

def convert_number(number_str: str) -> Union[int, float, str]:
    try:
        return int(number_str)
    except ValueError:
        try:
            return float(number_str)
        except ValueError:
            return number_str

def is_valid_json_list_or_dict(string: str) -> bool:
    try:
        data = json.loads(string)
        return isinstance(data, (list, dict))
    except (json.decoder.JSONDecodeError, TypeError):
        return False

def path_treatment(path: str) -> list:
    keys = path.split("/")
    
    for i, key in enumerate(keys):
        key = key.replace("'", '"')
        
        if starts_and_ends_with(key, '"'):
            keys[i] = key.strip('"')
        
        if key.isdigit():
            keys[i] = convert_number(key)
        
        if is_valid_json_list_or_dict(key):
            keys[i] = json.loads(key)
    
    return keys

def starts_and_ends_with(string: str, circumfix: str) -> str:
    return (string.startswith(circumfix) and string.endswith(circumfix))
 
def all_options_primitive(dropdown: Union[ListDropdown, DictDropdown, ft.Dropdown]) -> bool:
    if isinstance(dropdown, ListDropdown):
        options = [option.key for option in dropdown.options]
    else:
        options = [dropdown.dictionary[option.key] for option in dropdown.options]

    for option in options:
        if is_valid_json_list_or_dict(option) or isinstance(option, (list, dict)):
            return False
    return True

def only_one_option(list: ft.Dropdown) -> bool:
    if len(list.options) != 1:
        return False
    return True