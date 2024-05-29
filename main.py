import flet as ft
from data_navigator import SingleFieldEditor, AllFieldsEditor

def main(page: ft.Page):
    data = [[["boa tarde", "bom dia", "boa noite"], "tchau"], 0, [True, False, None], 2, 3]
    page.add(SingleFieldEditor(data))

if __name__ == "__main__":
    ft.app(target=main)