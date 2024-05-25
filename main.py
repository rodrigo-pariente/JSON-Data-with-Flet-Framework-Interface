import flet as ft
import json
from abc import ABC, abstractmethod

class ValueTextField(ft.TextField):
    def __init__(self, value='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = value
        self.child = None

class DictDropdown(ft.Dropdown):
    def __init__(self, dictionary, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dictionary = dictionary
        self.options = [ft.dropdown.Option(json.dumps(key))
                        if not isinstance(key, (int, float, str, bool))
                        else ft.dropdown.Option(str(key))
                        for key in dictionary.keys()]
        self.value = self.options[0].key
        self.child = True

class ListDropdown(ft.Dropdown):
    def __init__(self, list: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list = list
        self.options = [ft.dropdown.Option(json.dumps(key))
                        if not isinstance(key, (int, float, str, bool))
                        else ft.dropdown.Option(str(key))
                        for key in list]
        self.value = self.options[0].key
        self.child = True

class DataNavigatorBase(ft.UserControl):
    def __init__(self, data, column=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = ui_component(data)
        self.root.on_change = self.key_change
        self.components_structure = ft.Column() if column else ft.Row()
        self.components_structure.controls = [self.root]
        self.next_node(self.root)
        self.components_structure_update()

    @abstractmethod
    def next_node(self, current):
        pass

    def key_change(self, e: ft.ControlEvent):
        self.next_node(e.control)
        self.components_structure_update()
        self.update()

    def components_structure_update(self):
        current = self.root
        self.components_structure.controls.clear()
        while current:
            if not isinstance(current, list):
                self.components_structure.controls.append(current)
                current = current.child
            else:
                self.components_structure.controls.extend(current)
                break

    def build(self):
        return self.components_structure

class DataNavigator(DataNavigatorBase):
    def next_node(self, current):
        while current.child:
            value = current.value if isinstance(current, ListDropdown) else current.dictionary[current.value]
            
            if is_valid_json_list_or_dict(value):
                parsed_value = json.loads(value)
                current.child = create_child_for_list(parsed_value) if isinstance(parsed_value, list) else create_child_for_dict(parsed_value)
            elif isinstance(current, DictDropdown) and isinstance(value, (list, dict)):
                current.child = create_child_for_list(value) if isinstance(value, list) else create_child_for_dict(value)
            else:
                current.child = create_child_for_value(value)
            
            if not isinstance(current.child, ValueTextField):
                current.child.on_change = self.key_change
            
            current = current.child

def all_options_primitive(dropdown) -> bool:
    for option in dropdown.options:
        if isinstance(dropdown, ListDropdown):
            if is_valid_json_list_or_dict(option.key) or isinstance(option.key, (list, dict)):
                return False
        else:
            if is_valid_json_list_or_dict(dropdown.dictionary[option.key]) or isinstance(dropdown.dictionary[option.key], (list, dict)):
                return False
    return True

class DataNavigatorAllTextFields(DataNavigatorBase):
    def next_node(self, current):
        while current.child:
            value = current.value if isinstance(current, ListDropdown) else current.dictionary[current.value]

            if is_valid_json_list_or_dict(value):
                parsed_value = json.loads(value)
                current.child = create_child_for_list(parsed_value) if isinstance(parsed_value, list) else create_child_for_dict(parsed_value)
            elif isinstance(current, DictDropdown) and isinstance(value, (list, dict)):
                current.child = create_child_for_list(value) if isinstance(value, list) else create_child_for_dict(value)
            else:
                current.child = create_child_for_value(value)

            if not isinstance(current.child, ValueTextField):
                if all_options_primitive(current.child):
                    if isinstance(current.child, ListDropdown):
                        current.child = [ValueTextField(label=f'start_value={option.key}', value=option.key) for option in current.child.options]
                    else:
                        current.child = [ValueTextField(label=option.key, value=current.child.dictionary[option.key]) for option in current.child.options]
                    break
                current.child.on_change = self.key_change
            current = current.child
            
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

def main(page: ft.Page):
    data = [[["boa tarde", "bom dia", "boa noite"], "tchau"], 0, [True, False, None], 2, 3]
    with open("tasks.json", "r", encoding="utf8") as read:
        data = json.load(read)
    page.add(DataNavigatorAllTextFields(data))

if __name__ == "__main__":
    ft.app(target=main)