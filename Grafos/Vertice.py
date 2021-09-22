class Vertice:
    def __init__(self,clave):
        self.id = clave
        self.conectadoA = {}#diccionario de adyacencias con ind como obj V y commo dato la ponderacion
        self.predecesor=None#obj del v predecesor 
        self.costo=0#costo todal de llegada
        print("---")

    def __str__(self):#establece la accion al invocar el obj V
        return str(self.id) + ' conectadoA: ' + str([x.id for x in self.conectadoA])

    def agregarVecino(self,vecino,ponderacion=0):
        self.conectadoA.setdefault(vecino,ponderacion)

    def obtenerId(self):
        return self.id

    def obtenerConexiones(self):
        return self.conectadoA.keys()

    def obtenerPonderacion(self,vecino):
        return self.conectadoA.get(vecino)