#ALTERAR O VALOR DE UM DADO COMPOSTO DE GRAU INDEFINIDO
from pprint import pprint
from utils import is_valid_json_list_or_dict
import json

dado = [
    1, 2, 3,
    [1, [2.3, 2, 0], "Red"],
    ["blue", "red"],
    4, 5, 6
]

path = "4"
new_value = "oi"

def list_item_replacer(data, path, new_value):
    keys = path.split("/")
    for key in keys:
        for i, item in enumerate(data):
            if f"{item}" == key:
                if f"{item}" == keys[-1]:
                    data[i] = new_value
                else:
                    print(keys)
                    keys.pop(0)
                    path = "/".join(keys)
                    list_item_replacer(data[i], path, new_value)
                return data

list_item_replacer(dado, path, new_value)
