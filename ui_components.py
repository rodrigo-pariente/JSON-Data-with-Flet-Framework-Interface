import flet as ft
import json

class ValueTextField(ft.TextField):
    def __init__(self, value='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = value
        self.child = None
        self.path = ''
        
class DictDropdown(ft.Dropdown):
    def __init__(self, dictionary, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dictionary = dictionary
        self.options = [ft.dropdown.Option(json.dumps(key))
                        if not isinstance(key, (int, float, str, bool))
                        else ft.dropdown.Option(str(key))
                        for key in dictionary.keys()]
        self.value = self.options[0].key if self.options else " "
        self.child = True
        self.path = ''

class ListDropdown(ft.Dropdown):
    def __init__(self, list: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list = list
        self.options = [ft.dropdown.Option(json.dumps(key))
                        if not isinstance(key, (int, float, str, bool))
                        else ft.dropdown.Option(str(key))
                        for key in list]
        self.value = self.options[0].key if self.options else " "
        self.child = True
        self.path = ''
    
    @property
    def get_index(self):
        for i, option in enumerate(self.options):
            if self.value == option.key:
                print('aqui', i)
                return i
        return -1
