import flet as ft
import json
from typing import Union

class ValueTextField(ft.TextField):
    def __init__(self, value='', path='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = value
        self.child = None
        self.path = path
        
class DictDropdown(ft.Dropdown):
    def __init__(self, dictionary, path='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dictionary = dictionary
        self.options = [ft.dropdown.Option(json.dumps(key))
                        if not isinstance(key, (int, float, str, bool))
                        else ft.dropdown.Option(str(key))
                        for key in dictionary.keys()]
        self.value = self.options[0].key if self.options else " "
        self.child = True
        self.path = path

class ListDropdown(ft.Dropdown):
    def __init__(self, list: list, path='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list = list
        self.options = [ft.dropdown.Option(json.dumps(key))
                        if not isinstance(key, (int, float, str, bool))
                        else ft.dropdown.Option(str(key))
                        for key in list]
        self.value = self.options[0].key if self.options else " "
        self.child = True
        self.path = path
    
    @property
    def get_index(self) -> int:
        for i, option in enumerate(self.options):
            if self.value == option.key:
                return i
        return -1

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