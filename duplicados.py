class MeuObjeto:
    def __init__(self, atributo):
        self.atributo = atributo
lista_de_objetos = [MeuObjeto(1), MeuObjeto(2), MeuObjeto(3), MeuObjeto(1), MeuObjeto(2)]

atributo_map = {}

for obj in lista_de_objetos:
    if obj.atributo in atributo_map:
        atributo_map[obj.atributo].append(obj)
    else:
        atributo_map[obj.atributo] = [obj]

objetos_duplicados = []

for value in atributo_map.values():
    if len(value) > 1:
        objetos_duplicados.extend(value)

print("Objetos duplicados:")
for obj in objetos_duplicados:
    print(obj.atributo)
