import flet as ft
from data_manager import DataManager, DataManagerPoint
from data_navigator import SingleFieldEditor, AllFieldsEditor, SaveButton

def main(page: ft.Page):
    data = [[["boa tarde", "bom dia", "boa noite"], "tchau"], 0, ['True', 'False', 'None'], 2, 3]
    data_manager = DataManager(data)
    editor = AllFieldsEditor(data_manager=data_manager)
    page.add(editor)
    
if __name__ == "__main__":
    ft.app(target=main)