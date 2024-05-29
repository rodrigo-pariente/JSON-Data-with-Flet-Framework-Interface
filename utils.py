from ui_components import ListDropdown, DictDropdown, ValueTextField
import json

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

def path_treatment(path):
    keys = path.split("/")
    for i, key in enumerate(keys):
        if starts_and_ends_with(key, "''"):
            keys[i] = key.strip("''")
        elif key.isdigit():
            keys[i] = convert_number(key)
        elif is_valid_json_list_or_dict(key):
            keys[i] = json.loads(key)
    if len(keys) == 1:
        return keys[0]
    return keys
 
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