from graphviz import Digraph

from Generador import Generador

g = Digraph('finite_state_machine', filename='fsm.gv')

gr = {
    "0": ["A'", "A"],
    "1": ["A", "(A)"],
    "2": ["A", "a"]
}
obj = Generador(gr)

g.attr(rankdir='LR', size='8,5')
g.attr('node', shape='box')


# Se crean los nodos
print("Nodos a crear\n\n")
for d in obj.listaNodos:
    datos_nodo = ""
    id_nodo = ""

    for key, item in d.items():
        if key is not "_id":
            datos_nodo=datos_nodo+key+")"+item[0]+"=>"+item[1]+"\n"
        else:
            id_nodo=item

    datos_nodo = "I" + str(id_nodo) + "\n" + datos_nodo
    print("los datos son")
    print(datos_nodo)
    print("el id es")
    print(id_nodo)

    g.node(str(id_nodo), label=datos_nodo)

#Se crean las adyacencias
for key, item in obj.dicAdyacencias.items():
    for lista in item:
        print("La linea va desde "+str(key)+" hasta "+str(lista[1])+" con valor "+lista[0]+" --valor desconocido:"+lista[2])
        g.edge(str(key), str(lista[1]), label=lista[0])

g.view()
