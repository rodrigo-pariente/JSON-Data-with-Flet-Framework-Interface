from typing import Union
import flet as ft
from data_manager import minimum_data_manager
from data_navigator import EditorsGroup, SingleFieldEditor, AllFieldsEditor
from ui_components import ValueTextField

class SaveButton(ft.IconButton):
    def __init__(self, editor: Union[SingleFieldEditor, AllFieldsEditor, EditorsGroup], filename: str="lipsum.json", refresh: bool=True, icon: ft.icons=ft.icons.SAVE, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = icon
        self.editor = editor
        self.filename = filename
        self.on_click = self.save_data
        self.editors = self.editor.get_editors if isinstance(self.editor, EditorsGroup) else None
        self.refresh_in_save = refresh

    def save_data(self, e: ft.ControlEvent):
        def get_textfields(editor) -> ValueTextField:
            textfields = []
            for component in editor.components_structure.controls:
                if isinstance(component, ValueTextField):
                    textfields.append(component)
            return textfields
        
        if not self.editors == None:
            textfields = []
            for editor in self.editors:
                textfields.extend(get_textfields(editor))
        else:
            textfields = get_textfields(self.editor)
            
        for textfield in textfields:
            path = textfield.path
            new_value = textfield.value
            min_data_manager = minimum_data_manager(self.editor.data_manager)
            min_data_manager.update_data(path, new_value)
        min_data_manager.save_data(self.filename)
        if self.refresh_in_save:
            self.refresh()

    def refresh(self):
        if self.editors:
            for editor in self.editors:
                editor.refresh()
        else:
            self.editor.refresh()