import flet as ft
import json

def is_valid_json_list(string: str):
    try:
        data = json.loads(string)
        if isinstance(data, (list, dict)):
            return True
        return False
    
    except json.decoder.JSONDecodeError:
        return False
    
    except TypeError:
        return False

class ValueTextField(ft.TextField):
    def __init__(self, start_value, *args, **kwargs):
        super().__init__(args, kwargs)
        self.value = start_value
        self.child = None

class ListDropdown(ft.Dropdown):
    def __init__(self, list: list, *args, **kwargs):
        super().__init__(args, kwargs)
        self.list = list
        self.options =[ft.dropdown.Option(json.dumps(key))
                        if not isinstance(key, (int, float, str, bool))
                        else ft.dropdown.Option(str(key))
                        for key in list]
        self.value = self.options[0].key
        self.child = True

class LinearTree(ft.UserControl):
    def __init__(self, root, *args, **kwargs):
        super().__init__(args, kwargs)
        self.root = root
        self.root.on_change = self.key_change
        self.components_column = ft.Column(controls=[root])
        self.next_node(self.root)
        self.components_column_update()

    def next_node(self, current):
        while current.child:
            condition_2 = isinstance(current.value, str) and is_valid_json_list(current.value)
            if condition_2:
                if isinstance(json.loads(current.value), list):
                    current.child = ListDropdown(json.loads(current.value))
                    current.child.on_change = self.key_change
            else:
                if isinstance(current, ListDropdown):
                    current.child = ValueTextField(current.value)
            current = current.child

    def key_change(self, e: ft.ControlEvent):
        self.next_node(e.control)
        self.components_column_update()
        self.update()

    def components_column_update(self):
        current = self.root
        self.components_column.controls.clear()
        while current:
            self.components_column.controls.append(current)
            current = current.child

    def build(self):
        return self.components_column
    
def main(page: ft.Page):
    data = [[["boa tarde", "bom dia", "boa noite"], "tchau"], 0, 1, 2, 3]
    root = ListDropdown(data)
    page.add(LinearTree(root))

if __name__=="__main__":
    ft.app(target=main)