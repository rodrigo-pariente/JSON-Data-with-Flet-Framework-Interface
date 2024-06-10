#DataTree
from utils import path_treatment

class Data:
    def __init__(self, data, path=""):
        self.data = data
        self.path = path
        self.child_generate()
    
    def child_generate(self, i=0):
        if isinstance(self.data, list):
            self.child = Data(self.data[i], path=f"{self.path}/{i}")
        elif isinstance(self.data, dict):
            i = next(iter(self.data)) if i == 0 else i
            self.child = Data(self.data[i], path=f"{self.path}/{i}")
        else:
            self.child = None

class DataTree:
    def __init__(self, data_root):
        self.root = data_root
    
    def traverse(self):
        current = self.root

        while current:
            print(current.data)
            print(current.path)
            print()
            current = current.child

dado = [{"banda preferida": ["Angra", "Death", "Pantera"], "idade": 19}, "Metallica", "Anthrax", "Slayer", "Megadeth", 2, 0]
dado_classe = Data(dado)
data_tree = DataTree(dado_classe)
data_tree.traverse()