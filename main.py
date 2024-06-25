import flet as ft
from data_manager import DataManager, DataManagerPoint
from data_navigator import SingleFieldEditor, AllFieldsEditor, EditorsGroup
from buttons import SaveIconButton, SaveElevatedButton, RefreshIconButton
import json

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

    with open('data.json', 'r', encoding='utf8') as file:
        data = json.load(file)

    data_manager = DataManager(data)
    editor_allfields = AllFieldsEditor(data_manager=data_manager)
    editor_simple = SingleFieldEditor(data_manager=data_manager)

    data_manager_point = DataManagerPoint(data_manager=data_manager, path="")
    point = AllFieldsEditor(data_manager_point)

    editors_group = EditorsGroup([editor_simple, point, editor_allfields])
    save = SaveIconButton(editor=editors_group, filename="data.json")
    refresh = RefreshIconButton(editors_group)
    page.add(ft.Row(controls=[editor_allfields, point, editor_simple, ]), ft.Row(controls=[save, refresh]))

if __name__ == "__main__":
    ft.app(target=main)

#FEITO - NECESSITA A FUNCIONALIDADE DE REFRESH, PARA ATUALIZAR CAMPOS COM VALORES ALTERADOS EM OUTROS CANTOS
#FEITO - INTEGRAR DATAMANAGER-DATAMANAGERPOINT-SINGLEFIELDEDITOR-ALLFIELDSEDITOR
#FEITO - PERMITIR QUE O DATAMANAGER POINT POSSA MÁSCARAR QUALQUER NÍVEL DE PROFUNDIDADE
#TRATAMENTO DE DADOS
#PERMITIR ADIÇÃO E REMOÇÃO DE DADOS