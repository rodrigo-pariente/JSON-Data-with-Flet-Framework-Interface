import flet as ft
from data_manager import DataManager, DataManagerPoint
from data_navigator import SingleFieldEditor, AllFieldsEditor, SaveButton, PathInText

def main(page: ft.Page):
    data = [
        {'chave_dict_1': 'valor_dict_1',
        'chave': "Metalica"},
        [
            {'chave_dict_lista': [1, 2, 3]},
            "elemento_lista_2",
            {'outra_chave_dict_lista': {'sub_lista': [4.5, 6.7, 8.9]}}, 100,
            "último_elemento_lissta"
        ],
        "último elemento"
    ]
    data_manager = DataManager(data)
    data_point = DataManagerPoint(data_manager=data_manager, path="1/0/'chave_dict_lista'/1")
    editor = SingleFieldEditor(data_manager=data_manager)
    page.add(editor)
    save = SaveButton(editor)
    page.add(save)
    point_editor = SingleFieldEditor(data_point)
    page.add(point_editor)

if __name__ == "__main__":
    ft.app(target=main)