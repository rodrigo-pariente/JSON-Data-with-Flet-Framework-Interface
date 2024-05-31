from data_manager import DataManager, DataManagerPoint
from pprint import pprint
# Dados complexos
dados_complexos = [
    "primeiro elemento",
    {'chave_dict_1': 'valor_dict_1'},
    [
        {'chave_dict_lista': [1, 2, 3]},
        "elemento_lista_2",
        {'outra_chave_dict_lista': {'sub_lista': [4.5, 6.7, 8.9]}},
        100,
        "último_elemento_lista"
    ],
    "último elemento"
]

# Caminho para o elemento a ser atualizado
path_4 = """[
    {'chave_dict_lista': [1, 2, 3]},
    "elemento_lista_2",
    {'outra_chave_dict_lista': {'sub_lista': [4.5, 6.7, 8.9]}},
    100,
    "último_elemento_lista"
]/{'chave_dict_lista': [1, 2, 3]}/chave_dict_lista/2"""
path_3 = """[
    {'chave_dict_lista': [1, 2, 3]},
    "elemento_lista_2",
    {'outra_chave_dict_lista': {'sub_lista': [4.5, 6.7, 8.9]}},
    100,
    "último_elemento_lista"
]/{'chave_dict_lista': [1, 2, 3]}/chave_dict_lista"""
# Novo valor a ser inserido
new_value = "MULTILAB"

# Criando uma instância do DataManager
dm = DataManager(dados_complexos)

# Atualizando o valor
dm.update_data(path_4, new_value)

# Imprimindo o dado atualizado
print("Dado atualizado:")
pprint(dm.get_data())

# Salvando os dados atualizados em um arquivo
dm.save_data("dados_atualizados.json")

# Criando uma instância do DataManagerPoint
dmp = DataManagerPoint(dm, path_3)

# Obtendo o valor no caminho especificado
print("Valor específico no caminho fornecido:")
pprint(dmp.get_value())

# Atualizando o valor usando DataManagerPoint
dmp.update_value("NOVO VALOR")

# Imprimindo o dado atualizado novamente
print("Dado atualizado após usar DataManagerPoint:")
pprint(dm.get_data())

# Salvando a parte específica dos dados em um arquivo
dmp.save("dados_ponto_atualizados.json")
