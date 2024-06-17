import flet as ft
from data_manager import DataManager, DataManagerPoint
from data_navigator import SingleFieldEditor, AllFieldsEditor, EditorsGroup
from save_button import SaveButton

def main(page: ft.Page):
    data = [
        {'chave_dict_1': 'valor_dict_1',
        'chave': "Metalica"},
        [
            {'chave_dict_lista': [1, 2, 3]},
            "elemento_lista_2s",
            {'outra_chave_dict_lista': {'sub_lista': [4.5, 6.7, 8.9]}}, 100,
            "último_elemento_lissta"
        ],
        "último elemento"
    ]
    data_manager = DataManager(data)
    data_point = DataManagerPoint(data_manager=data_manager, path="1/0/'chave_dict_lista'/1")
    editor = SingleFieldEditor(data_manager=data_manager)
    point_editor = SingleFieldEditor(data_point)
    editors_group = EditorsGroup([editor, point_editor])
    save = SaveButton(editors_group)
    page.add(editor, point_editor)
    page.add(save)

if __name__ == "__main__":
    ft.app(target=main)

#NECESSITA A FUNCIONALIDADE DE REFRESH, PARA ATUALIZAR CAMPOS COM VALORES ALTERADOS EM OUTROS CANTOS
#INTEGRAR DATAMANAGER-DATAMANAGERPOINT-SINGLEFIELDEDITOR-ALLFIELDSEDITOR
#TRATAMENTO DE DADOS