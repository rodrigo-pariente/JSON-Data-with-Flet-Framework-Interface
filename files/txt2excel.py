import pandas as pd
import flet as ft

class FileInAndOut(ft.UserControl):
    def __init__(self, in_field, out_field, separator=" - "):
        super().__init__()
        self.sep = separator
        self.in_field = ft.TextField(hint_text=f"file.{in_field}", width=200)
        self.out_field = ft.TextField(hint_text=f"file.{out_field}", width=200)
        self.sep_field = ft.TextField(hint_text="sep", width=40)
        
        self.write_button = TextToExcelButton(self.in_field.value, self.out_field.value, sep=self.sep)

        self.out_field.on_change = self.value_change
        self.in_field.on_change = self.value_change
        self.sep_field.on_change = self.value_change

    
    def value_change(self, e):
        self.write_button.text_file = self.in_field.value
        self.write_button.excel_file = self.out_field.value
        self.write_button.sep = self.sep_field.value
        self.update()

    def build(self) -> ft.Column:
        return ft.Column(controls=[self.in_field,
                                self.out_field,
                                ft.Row(controls=[self.sep_field,
                                                 self.write_button]),
                                self.write_button.error_lines])
    
class TextToExcelButton(ft.ElevatedButton):
    def __init__(self, text_file, excel_file, sep=" - "):
        super().__init__(text="Write")
        self.sep = sep
        self.text_file = text_file
        self.excel_file = excel_file
        self.on_click = self.text2excel
        self.error_lines = ft.Text()

    def text2excel(self, e):
        data = []
        error_lines = []

        with open(self.text_file, 'r', encoding='utf-8') as file:
            for line in file:
                # Remover espaços em branco e quebras de linha
                line = line.strip()

                # Dividir a linha pelo separador " - "
                try:
                    codigo, quantidade, nome = line.split(self.sep)
                    data.append([codigo, quantidade, nome])

                except ValueError as e:
                    error_lines.append(line)

        # Criar um DataFrame do pandas a partir da lista de dados
        df = pd.DataFrame(data, columns=['Código', 'Quantidade', 'Nome'])

        # Escrever o DataFrame para um arquivo Excel
        df.to_excel(self.excel_file, index=False)
        self.error_lines.value = error_lines
        self.update()

def main(page: ft.Page):
    txt_and_excel_textfields = FileInAndOut("txt", "xlsx")
    page.add(ft.Row(controls=[txt_and_excel_textfields]))

if __name__=="__main__":
    ft.app(target=main)