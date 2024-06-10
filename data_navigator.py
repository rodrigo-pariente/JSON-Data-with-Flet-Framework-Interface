import flet as ft
import json
from ui_components import ValueTextField, DictDropdown, ListDropdown
from utils import ui_component, is_valid_json_list_or_dict, all_options_primitive, create_child_for_dict, create_child_for_list, create_child_for_value
from data_manager import DataManager, DataManagerPoint
from abc import ABC, abstractmethod
from typing import Union

class DataNavigator(ft.UserControl, ABC):
    def __init__(self, data_manager: Union[DataManager, DataManagerPoint], column=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_manager = data_manager

        if isinstance(data_manager, DataManager):
            self.root = ui_component(data_manager.get_data)
        else:
            self.root = ui_component(data_manager.get_value)

        self.root.on_change = self.key_change
        self.path = None

        self.components_structure = ft.Column() if column else ft.Row()
        self.components_structure.controls = [self.root]
        self.next_node(self.root)
        self.components_structure_update()
    
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
    
    def next_node(self, current):
        while not isinstance(current, list) and current.child:
            path = current.path
            if isinstance(current, ListDropdown):
                value = current.value
                path += f"/{current.get_index}"
            else:
                value = current.dictionary[current.value]
                path += f"/{current.value}"

            if is_valid_json_list_or_dict(value):
                value = json.loads(value)

            if isinstance(value, list):
                current.child = create_child_for_list(value)
            elif isinstance(value, dict):
                current.child = create_child_for_dict(value)
            else:
                current.child = create_child_for_value(value)
            
            self.custom_logic(current)
            
            if isinstance(current, (ListDropdown, DictDropdown, ValueTextField)):
                if not isinstance(current, ValueTextField):
                    current.on_change = self.key_change
            current = current.child
            path = path.replace('/', '', 1) if path.startswith("/") else path
            current.path = path
        self.path = current.path

    @abstractmethod
    def custom_logic(self, current):
        pass
    
class SingleFieldEditor(DataNavigator):
    def custom_logic(self, current):
        pass

class AllFieldsEditor(DataNavigator):
    def custom_logic(self, current):
        if not isinstance(current.child, ValueTextField) and all_options_primitive(current.child):
            if current.child.options:
                if isinstance(current.child, ListDropdown):
                    current.child = [ValueTextField(label=f'start_value={option.key}', value=option.key)
                                        for option in current.child.options]
                elif isinstance(current.child, DictDropdown):
                    current.child = [ValueTextField(label=option.key, value=current.child.dictionary[option.key])
                                        for option in current.child.options]
            else:
                current.child = [ValueTextField(value='')]

class SaveButton(ft.IconButton):
    def __init__(self, publisher: Union[SingleFieldEditor, AllFieldsEditor],*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = ft.icons.SAVE
        self.publisher = publisher
        self.on_click = self.update_data

    def update_data(self, e: ft.ControlEvent):
        path = self.publisher.path
        new_value = self.publisher.components_structure.controls[-1].value
        self.publisher.data_manager.update_data(path, new_value)
        self.publisher.data_manager.save_data("arquivo.json")