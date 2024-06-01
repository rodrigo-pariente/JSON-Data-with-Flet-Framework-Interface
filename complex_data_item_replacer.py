import json
from utils import starts_and_ends_with, convert_number, is_valid_json_list_or_dict
from typing import Union

def path_treatment(path):
    # Divide o caminho em partes usando "/" como separador
    keys = path.split("/")
    
    # Itera sobre as partes do caminho
    for i, key in enumerate(keys):
        # Substitui as aspas simples por aspas duplas para garantir que o JSON seja válido
        key = key.replace("'", '"')
        
        # Remove as aspas duplas do início e do fim, se presentes
        if starts_and_ends_with(key, '"'):
            keys[i] = key.strip('"')
        
        # Converte números que estavam entre aspas em tipos numéricos
        if key.isdigit():
            keys[i] = convert_number(key)
        
        # Converte strings JSON válidas em estruturas de dados correspondentes
        if is_valid_json_list_or_dict(key):
            keys[i] = json.loads(key)
    
    return keys

def complex_data_item_replacer(data: Union[list, dict, str, int, float], path: str, new_value: any, false_if_not_found: bool=False):
    # Realiza o tratamento do caminho para garantir que seja compatível com o resto do código
    keys = path_treatment(path)

    # Itera sobre as chaves no caminho
    for key in keys:
        # Verifica se a estrutura de dados atual é uma lista
        if isinstance(data, list):
            for i, item in enumerate(data):
                # Verifica se o item atual é igual à chave
                if item == key:
                    # Se o item for a chave final, substitui pelo novo valor
                    if item == keys[-1]:
                        data[i] = new_value
                    else:
                        # Se não for a chave final, continua a busca recursivamente
                        keys.pop(0)
                        # Garante que as chaves sejam convertidas em strings válidas, se necessário
                        keys = [json.dumps(key) if not isinstance(key, str) else key for key in keys]
                        path = "/".join(keys)
                        complex_data_item_replacer(data[i], path, new_value)
                    return data
                
        # Verifica se a estrutura de dados atual é um dicionário
        elif isinstance(data, dict):
            for dict_key, value in data.items():
                # Verifica se a chave do dicionário atual é igual à chave
                if dict_key == key:
                    # Se a chave do dicionário for a chave final, substitui pelo novo valor
                    if dict_key == keys[-1]:
                        data[dict_key] = new_value
                    else:
                        # Se não for a chave final, continua a busca recursivamente
                        keys.pop(0)
                        # Garante que as chaves sejam convertidas em strings válidas, se necessário
                        keys = [json.dumps(key) if not isinstance(key, str) else key for key in keys]
                        path = "/".join(keys)
                        complex_data_item_replacer(data[dict_key], path, new_value)
                    return data
                
    # Retorna False se a opção false_if_not_found for True e a chave não for encontrada
    if false_if_not_found:
        return False
    # Retorna a estrutura de dados original se a chave não for encontrada
    return data

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

path_4 = """[
        {'chave_dict_lista': [1, 2, 3]},
        "elemento_lista_2",
        {'outra_chave_dict_lista': {'sub_lista': [4.5, 6.7, 8.9]}},
        100,
        "último_elemento_lista"
    ]/{'chave_dict_lista': [1, 2, 3]}/'chave_dict_lista'/2"""
new_value_4 = "boing 787"

dado = [{"Tenacious D": "Tribute", "Dio": "Holy Diver"},
        1, 2, {"lista": ["decoy"]}, 3, ["Angra", 27, "Lione", "Fim do dado"]]
path = "{'lista': ['decoy']}/'lista'/'decoy'"

modified = complex_data_item_replacer(dado, path, "Verdadeiro", false_if_not_found=True)
print(modified)