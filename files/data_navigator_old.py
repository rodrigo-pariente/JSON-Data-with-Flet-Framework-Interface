import flet as ft
import json
from abc import ABC, abstractmethod
from ui_components import ValueTextField, ListDropdown, DictDropdown
from utils import ui_component, is_valid_json_list_or_dict, all_options_primitive, create_child_for_dict, create_child_for_list, create_child_for_value
from data_manager import DataManager

# Classe base para navegadores de dados, utilizando Flet para UI e seguindo o padrão de controle do usuário (UserControl)
class DataNavigatorBase(ft.UserControl, ABC):
    def __init__(self, data_manager: DataManager, column=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_manager = data_manager
        self.root = ui_component(data_manager.get_data)  # Cria o componente inicial baseado nos dados
        self.root.on_change = self.key_change  # Define a função de callback para mudanças na chave
        self.components_structure = ft.Column() if column else ft.Row()  # Define a estrutura de componentes
        self.components_structure.controls = [self.root]  # Adiciona o componente raiz na estrutura
        self.next_node(self.root)  # Navega para o próximo nó
        self.components_structure_update()  # Atualiza a estrutura dos componentes

    # Método chamado quando uma chave muda, atualizando a estrutura dos componentes
    def key_change(self, e: ft.ControlEvent):
        self.next_node(e.control)  # Navega para o próximo nó baseado no controle atual
        self.components_structure_update()  # Atualiza a estrutura dos componentes
        self.update()  # Atualiza a interface do usuário

    # Atualiza a estrutura dos componentes com base na navegação atual
    def components_structure_update(self):
        current = self.root
        self.components_structure.controls.clear()  # Limpa a estrutura atual dos componentes
        while current:
            if not isinstance(current, list):
                self.components_structure.controls.append(ft.Text(current.path))  # Adiciona o caminho atual como texto
                self.components_structure.controls.append(current)  # Adiciona o componente atual na estrutura
                current = current.child  # Avança para o próximo componente
            else:
                self.components_structure.controls.extend(current)  # Adiciona a lista de componentes
                break

    # Método obrigatório do Flet para construir a interface
    def build(self):
        return self.components_structure  # Retorna a estrutura dos componentes

    # Lógica comum para avançar para o próximo nó na navegação dos dados
    def common_next_node_logic(self, current):
        # Obtém o valor atual baseado no tipo de componente
        value = current.value if isinstance(current, ListDropdown) else current.dictionary[current.value]
        path = current.path

        # Verifica se o valor é um JSON válido
        if is_valid_json_list_or_dict(value):
            parsed_value = json.loads(value)
            # Cria o próximo nó com base no tipo de dados (lista ou dicionário)
            if isinstance(parsed_value, list):
                current.child = create_child_for_list(parsed_value)
                path += f"/{current.child.get_index}"
            else:
                current.child = create_child_for_dict(parsed_value)
                path += f"/{current.child.value}"

        elif isinstance(current, DictDropdown) and isinstance(value, (list, dict)):
            if isinstance(value, list):
                current.child = create_child_for_list(value)
                path += f"/{current.child.get_index}"
            else:
                current.child = create_child_for_dict(value)
                path += f"/{current.child.value}"
        else:
            current.child = create_child_for_value(value)
            path += f"/{current.get_index}" if isinstance(current, ListDropdown) else f"/{value}"
        path = path.replace('/', '', 1) if path.startswith("/") else path
        if isinstance(current.child, (ListDropdown, DictDropdown, ValueTextField)):
            current.child.path = path  # Atualiza o caminho do componente filho

    # Método abstrato para avançar para o próximo nó, a ser implementado nas subclasses
    @abstractmethod
    def next_node(self, current):
        pass

# Editor de campo único, uma especialização do DataNavigatorBase
class SingleFieldEditor(DataNavigatorBase):
    def next_node(self, current):
        while current.child:
            self.common_next_node_logic(current)  # Executa a lógica comum para avançar para o próximo nó
            if isinstance(current.child, (ListDropdown, DictDropdown)):
                current.child.on_change = self.key_change  # Define a função de callback para mudanças na chave
            current = current.child  # Avança para o próximo componente

# Editor de todos os campos, outra especialização do DataNavigatorBase
class AllFieldsEditor(DataNavigatorBase):
    def next_node(self, current):
        while current.child:
            self.common_next_node_logic(current)  # Executa a lógica comum para avançar para o próximo nó
            # Se todos os filhos são primitivos, cria campos de valor para todos
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
            current = current.child  # Avança para o próximo componente
