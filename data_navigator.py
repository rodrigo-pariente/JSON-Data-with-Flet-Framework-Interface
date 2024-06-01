import flet as ft
import json
from abc import ABC, abstractmethod
from ui_components import ValueTextField, ListDropdown, DictDropdown
from utils import ui_component, is_valid_json_list_or_dict, all_options_primitive, create_child_for_dict, create_child_for_list, create_child_for_value
from data_manager import DataManager

class SaveButton(ft.IconButton):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.icon = ft.icons.SAVE

class DataNavigatorBase(ft.UserControl, ABC):
    def __init__(self, data_manager: DataManager, column=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_manager = data_manager
        self.root = ui_component(data_manager.get_data)
        self.root.on_change = self.key_change
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

    def common_next_node_logic(self, current):
        value = current.value if isinstance(current, ListDropdown) else current.dictionary[current.value]
        
        if is_valid_json_list_or_dict(value):
            parsed_value = json.loads(value)
            current.child = create_child_for_list(parsed_value) if isinstance(parsed_value, list) else create_child_for_dict(parsed_value)
        elif isinstance(current, DictDropdown) and isinstance(value, (list, dict)):
            current.child = create_child_for_list(value) if isinstance(value, list) else create_child_for_dict(value)
        else:
            current.child = create_child_for_value(value)

    @abstractmethod
    def next_node(self, current):
        pass

class SingleFieldEditor(DataNavigatorBase):
    def next_node(self, current):
        while current.child:
            self.common_next_node_logic(current)
            if not isinstance(current.child, ValueTextField):
                current.child.on_change = self.key_change
            current = current.child

class AllFieldsEditor(DataNavigatorBase):
    def next_node(self, current):
        while current.child:
            self.common_next_node_logic(current)
            if not isinstance(current.child, ValueTextField) and all_options_primitive(current.child):
                if isinstance(current.child, ListDropdown):
                    if current.child.options:
                        current.child = [ValueTextField(label=f'start_value={option.key}', value=option.key)
                                         for option in current.child.options]
                    else:
                        current.child = [ValueTextField(value="")]
                else:
                    current.child = [ValueTextField(label=option.key, value=current.child.dictionary[option.key])
                                     for option in current.child.options]
                break
            current.child.on_change = self.key_change if not isinstance(current.child, ValueTextField) else None
            current = current.child
