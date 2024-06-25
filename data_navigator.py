import flet as ft
import json
from ui_components import ValueTextField, DictDropdown, ListDropdown
from utils import CustomError, path_treatment, ui_component, is_valid_json_list_or_dict, all_options_primitive, only_one_option, create_child_for_dict, create_child_for_list, create_child_for_value
from data_manager import DataManager, DataManagerPoint, minimum_data_manager
from abc import ABC, abstractmethod
from typing import Union

class DataNavigator(ft.UserControl, ABC):
    def __init__(self, data_manager: Union[DataManager, DataManagerPoint], column=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_manager = data_manager
        self.components_structure = ft.Column() if column else ft.Row()
        self.set_root()
        self.next_node(self.root)
        self.components_structure_update()
    
    def set_root(self):
        if isinstance(self.data_manager, DataManager):
            self.root = ui_component(self.data_manager.get_data)
            self.path = ""
        else:
            self.root = ui_component(self.data_manager.get_value)
            self.path = self.data_manager.path
        self.root.path = self.path
        if not isinstance(self.root, ValueTextField):
            self.root.on_change = self.key_change

    def key_change(self, e: ft.ControlEvent):
        self.next_node(e.control)
        self.components_structure_update()
        self.update()

    def refresh(self):
        path = self.path
        self.set_root()
        self.next_node(self.root)
        self.set_selection_by_path(path) 
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

    def build(self) -> Union[ft.Column, ft.Row]:
        return self.components_structure
    
    def next_node(self, current: Union[ValueTextField, ListDropdown, DictDropdown]):
        while not isinstance(current, list) and current.child:
            current = self.dropdown_iterator(current)
        if isinstance(current, list):
            keys = path_treatment(current[0].path)
            keys.pop()
            keys = [f'{key}' for key in keys]
            self.path = '/'.join(keys)
        else:
            self.path = current.path
            
    def dropdown_iterator(self, current: Union[ValueTextField, ListDropdown, DictDropdown]) -> Union[ValueTextField, ListDropdown, DictDropdown]:
        path = current.path
        if isinstance(current, ListDropdown):
            value = current.value
            path += f"/{current.get_index}"
        else:
            value = current.dictionary[current.value]
            path += f"/{current.value}"
        if path.startswith("/"):
            path = path.replace('/', '', 1)

        if is_valid_json_list_or_dict(value):
            value = json.loads(value)

        if isinstance(value, list):
            current.child = create_child_for_list(value)
        elif isinstance(value, dict):
            current.child = create_child_for_dict(value)
        else:
            current.child = create_child_for_value(value)
        
        self.custom_logic(current, path)
        
        if isinstance(current, (ListDropdown, DictDropdown)):
            current.on_change = self.key_change
        return current.child
    
    @abstractmethod
    def custom_logic(self, current: Union[ValueTextField, ListDropdown, DictDropdown], path: str=''):
        pass

    def set_selection_by_path(self, path_to_set: str):
        keys = path_treatment(path_to_set)
        current = self.root
        if isinstance(self.data_manager, DataManagerPoint):
            minimum_component = len(path_treatment(self.data_manager.path)) + 1
        elif isinstance(self.data_manager, DataManager):
            minimum_component = 0
        for n in range(minimum_component, (len(keys) + 1)): #Isso é melhor que o while?
            if isinstance(current, list) or not current.child:
                break
            if not n == 0:
                current = self.dropdown_iterator(current)
            if isinstance(current, ListDropdown):

                current.value = current.options[keys[n]].key
            elif isinstance(current, DictDropdown):
                for option in current.options:
                    if option.key == keys[n]:
                        current.value = option.key
        if isinstance(current, list):
            keys = path_treatment(current[0].path)
            keys.pop()
            keys = [f'{key}' for key in keys]
            self.path = '/'.join(keys)
        else:
            self.path = current.path

class SingleFieldEditor(DataNavigator):
    def custom_logic(self, current: Union[ValueTextField, ListDropdown, DictDropdown], path: str=''):
        current.child.path = path

class AllFieldsEditor(DataNavigator):
    def custom_logic(self, current: Union[ValueTextField, ListDropdown, DictDropdown], path: str=''):
        if not isinstance(current.child, ValueTextField) and all_options_primitive(current.child):
            if current.child.options:
                if isinstance(current.child, ListDropdown):
                    current.child = [ValueTextField(label=f'start_value={option.key}', value=option.key,
                                                    path=f'{path}/{i}')
                                        for i, option in enumerate(current.child.options)]
                elif isinstance(current.child, DictDropdown):
                    current.child = [ValueTextField(label=option.key, value=current.child.dictionary[option.key],
                                                    path=f'{path}/{option.key}')
                                        for option in current.child.options]
            else:
                current.child = [ValueTextField(value='')]
            for textfield in current.child:
                if textfield.path.startswith("/"):
                    textfield.path = textfield.path.replace('/', '', 1)
        else:
            current.child.path = path

class EditorsGroup:
    def __init__(self, list_of_editors: list=[]):
        self._editors_group = list_of_editors
        self.editors_data_manager_check()
    
    def add_editors(self, *args: Union[SingleFieldEditor, AllFieldsEditor]):
        self._editors_group.append(args)
        self.editors_data_manager_check()
        
    def editors_data_manager_check(self):
        current = minimum_data_manager(self._editors_group[0].data_manager)
        for editor in self._editors_group:
            if current != minimum_data_manager(editor.data_manager):
                raise CustomError(f"Error: editors data_manager are not uniform.")
            current = minimum_data_manager(editor.data_manager)
    
    @property
    def get_editors(self) -> list:
        return self._editors_group
    
    @property
    def data_manager(self) -> DataManager:
        return minimum_data_manager(self._editors_group[0].data_manager)