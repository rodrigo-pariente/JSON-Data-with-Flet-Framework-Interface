import json
import flet as ft
def is_valid_json_list(string: str):
    try:
        data = json.loads(string)
        if isinstance(data, list):
            return True
        return False
    
    except json.decoder.JSONDecodeError:
        return False
    
    except TypeError:
        return False

string_1 = "asdasd"
string_2 = json.dumps(3)
string_3 = json.dumps([1, 2, ["oi", "boa tarde", "tchau"]])
string_4 = '[1, 2, ["oi", "boa tarde", "tchau"]]'
lista = [1, 2, ["oi", "boa tarde", "tchau"]]

options = [ft.dropdown.Option(json.dumps(key))
           if not isinstance(key, (int, float, str, bool))
           else ft.dropdown.Option(str(key))
           for key in lista]
print(options)

