from data_manager import DataManager, DataManagerPoint
from pprint import pprint
# Dados complexos
dados = [
    "primeiro elemento",
    {'chave_dict_1': 'valor_dict_1'},
    [
        {'chave_dict_lista': [1, 2, 3]},
        "elemento_lista_2",
        {'outra_chave_dict_lista': {'sub_lista': [4.5, 6.7, 8.9]}}, 100,
        "último_elemento_lista"
    ],
    "último elemento"
]

# Caminho para o elemento a ser atualizado
path_1 = '2/2/"outra_chave_dict_lista"'
path_2 = '2/2/"outra_chave_dict_lista"/"sub_lista"/1'
# Novo valor a ser inserido
new_value = "QUE QUE É MEU??"

# Criando uma instância do DataManager
dm = DataManager(dados)
dmp = DataManagerPoint(dm, path_1)
pprint(dmp.get_value)
print()

dm.update_data(path_2, new_value)
pprint(dmp.get_value)
print()

dmp.update_value(["eu descasco", "banana", "com as mãos"])
pprint(dm.get_data)

dm.save_data("biroliro.json")
dmp.update_value("SURF ROCK!!!")
dm.save_data("you.json")