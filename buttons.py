from typing import Union, List
import flet as ft
from data_manager import minimum_data_manager
from data_navigator import EditorsGroup, SingleFieldEditor, AllFieldsEditor
from ui_components import ValueTextField

class ButtonActions:
    @staticmethod
    def save_data(editor: Union[SingleFieldEditor, AllFieldsEditor, EditorsGroup], editors: Union[List[Union[SingleFieldEditor, AllFieldsEditor]], None]=None,  filename: str="lipsum.json"):
        def get_textfields(editor) -> List[ValueTextField]:
            textfields = []
            for component in editor.components_structure.controls:
                if isinstance(component, ValueTextField):
                    textfields.append(component)
            return textfields
        
        if not editors == None:
            textfields = []
            for editor in editors:
                textfields.extend(get_textfields(editor))
        else:
            textfields = get_textfields(editor)
            
        for textfield in textfields:
            path = textfield.path
            new_value = textfield.value
            min_data_manager = minimum_data_manager(editor.data_manager)
            min_data_manager.update_data(path, new_value)
        min_data_manager.save_data(filename)

    @staticmethod
    def refresh(editor: Union[SingleFieldEditor, AllFieldsEditor, EditorsGroup], editors: Union[List[Union[SingleFieldEditor, AllFieldsEditor]], None]=None):
        if editors:
            for ed in editors:
                ed.refresh()
        else:
            editor.refresh()

class SaveButton:
    def __init__(self, editor: Union[SingleFieldEditor, AllFieldsEditor, EditorsGroup], filename: str="lipsum.json", refresh: bool=True, *args, **kwargs):
        self.editor = editor
        self.filename = filename
        self.editors = self.editor.get_editors if isinstance(self.editor, EditorsGroup) else None
        self.refresh_in_save = refresh

    def save_action(self, e: ft.ControlEvent):
        ButtonActions.save_data(self.editor, self.editors, self.filename)
        if self.refresh_in_save:
            ButtonActions.refresh(self.editor, self.editors)

class SaveIconButton(SaveButton, ft.IconButton):
    def __init__(self, editor: Union[SingleFieldEditor, AllFieldsEditor, EditorsGroup], filename: str = "lipsum.json", refresh: bool = True, icon: ft.icons = ft.icons.SAVE, *args, **kwargs):
        SaveButton.__init__(self, editor, filename, refresh)
        ft.IconButton.__init__(self, icon=icon, on_click=self.save_action, *args, **kwargs)

class SaveElevatedButton(SaveButton, ft.ElevatedButton):
    def __init__(self, editor: Union[SingleFieldEditor, AllFieldsEditor, EditorsGroup], filename: str = "lipsum.json", refresh: bool = True, text: str = "Save", *args, **kwargs):
        SaveButton.__init__(self, editor, filename, refresh)
        ft.ElevatedButton.__init__(self, text=text, on_click=self.save_action, *args, **kwargs)

class RefreshButton:
    def __init__(self, editor: Union[SingleFieldEditor, AllFieldsEditor, EditorsGroup], *args, **kwargs):
        self.editor = editor
        self.editors = self.editor.get_editors if isinstance(self.editor, EditorsGroup) else None

    def refresh_action(self, e: ft.ControlEvent):
        ButtonActions.refresh(self.editor, self.editors)

class RefreshIconButton(RefreshButton, ft.IconButton):
    def __init__(self, editor: Union[SingleFieldEditor, AllFieldsEditor, EditorsGroup], icon: ft.icons = ft.icons.REFRESH, *args, **kwargs):
        RefreshButton.__init__(self, editor)
        ft.IconButton.__init__(self, icon, on_click=self.refresh_action)
        