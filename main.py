import flet as ft
import json

def is_valid_json_list_or_dict(string: str) -> bool:
    try:
        data = json.loads(string)
        return isinstance(data, (list, dict))
    except (json.decoder.JSONDecodeError, TypeError):
        return False

def create_child_for_list(data):
    return ListDropdown(data)

def create_child_for_dict(data):
    return DictDropdown(data)

def create_child_for_value(value):
    return ValueTextField(value)

def ui_component(data):
    if isinstance(data, list):
        return create_child_for_list(data)
    elif isinstance(data, dict):
        return create_child_for_dict(data)
    return create_child_for_value(data)

class ValueTextField(ft.TextField):
    def __init__(self, start_value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = start_value
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

class LinearTree(ft.UserControl):
    def __init__(self, root, column=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = root
        self.root.on_change = self.key_change
        self.components_structure = ft.Column() if column else ft.Row()
        self.components_structure.controls = [root]
        self.next_node(self.root)
        self.components_structure_update()

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

    def key_change(self, e: ft.ControlEvent):
        self.next_node(e.control)
        self.components_structure_update()
        self.update()

    def components_structure_update(self):
        current = self.root
        self.components_structure.controls.clear()
        while current:
            self.components_structure.controls.append(current)
            current = current.child

    def build(self):
        return self.components_structure

def main(page: ft.Page):
    data = [[["boa tarde", "bom dia", "boa noite"], "tchau"], 0, [True, False, None], 2, 3]
    with open("data.json", "r", encoding="utf8") as read:
        data = json.load(read)
    root = ui_component(data)
    page.add(LinearTree(root))

if __name__ == "__main__":
    ft.app(target=main)