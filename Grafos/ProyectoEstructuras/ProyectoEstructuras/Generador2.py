import json


class Generador2():
    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.gramaticaExpandida = {}
        self.indexPunto = 0
        self.key = 0

    """Ejecuta los metodos necesarios para hacer la tarea"""
    def start(self,primeros, gramaticaExpandida):
        gramaticaExpandida = self.colocadaDeComas(gramaticaExpandida)
        gramaticaExpandida = self.correccionIncertidumbre(primeros, gramaticaExpandida)
        self.gramaticaExpandida = gramaticaExpandida
        return self.analizarProducciones(primeros,gramaticaExpandida)

    """Apartir de una gramatica extendida se colocan los primeros"""

    def analizarProducciones(self, primeros, gramaticaExpandida):
        for key in gramaticaExpandida:
            if key != "_id":
                self.key = key #Que hacia esto? ya lo olvide
                self.indexPunto = gramaticaExpandida[key][1].find(".")
                esCompuesta = False
                indexDerecha = self.indexPunto + 1
                if gramaticaExpandida[key][1].find(" ") != -1: #Significa que hay una produccion compuesta
                    esCompuesta = True
                    llavesProducciones = self.esNoTerminalProd(self.produccionConPunto(gramaticaExpandida[key][1]))
                else:
                    llavesProducciones = self.esNoTerminalProd(gramaticaExpandida[key][1][indexDerecha])  # llaves de las producciones a las que hay que colocarle acompañante
                    indexDobleDerecha = self.indexPunto + 2
                if gramaticaExpandida[key][1][indexDerecha] != ",":  # Si la derecha no es coma
                    if llavesProducciones != False and esCompuesta == True: #Si es produccion compuesta
                        if self.produccionLadoPunto(gramaticaExpandida[key][1]) == ",":
                            for llave in llavesProducciones:
                                if llave > key:  # Solo si estan abajo
                                    if self.hayAcompañantesYa(gramaticaExpandida[llave][1]):
                                        gramaticaExpandida[llave][1] += "|" + self.getAcompañantesDeLaLLave(key, gramaticaExpandida)
                                    else:
                                        gramaticaExpandida[llave][1] += self.getAcompañantesDeLaLLave(key, gramaticaExpandida)
                        else: #Se colocan los primeros
                            llavesPrimeros = self.esNoTerminalPrim(self.produccionLadoPunto(gramaticaExpandida[key][1]))  # Llaves donde se sacan los primeros
                            if llavesPrimeros != False:  # Si es nt se procede a colocar los primeros
                                gramaticaExpandida = self.colocarPrimeros(llavesPrimeros, llavesProducciones, gramaticaExpandida)
                            else:  # Si es un terminal se le colocan a las producciones
                                for llavesitas in llavesProducciones:
                                    if self.hayAcompañantesYa(gramaticaExpandida[llavesitas][1]):
                                        gramaticaExpandida[llavesitas][1] += "|" + self.produccionLadoPunto(gramaticaExpandida[key][1])
                                    else:
                                        gramaticaExpandida[llavesitas][1] += self.produccionLadoPunto(gramaticaExpandida[key][1])
                    elif llavesProducciones != False and gramaticaExpandida[key][1][indexDobleDerecha] == ",":  # Si encuentra los acompañantes los coloca
                        for llave in llavesProducciones:
                            if llave > key: #Solo si estan abajo
                                if self.hayAcompañantesYa(gramaticaExpandida[llave][1]):
                                    gramaticaExpandida[llave][1] += "|" + self.getAcompañantesDeLaLLave(key,gramaticaExpandida)
                                else:
                                    gramaticaExpandida[llave][1] += self.getAcompañantesDeLaLLave(key,gramaticaExpandida)
                    elif llavesProducciones != False and gramaticaExpandida[key][1][indexDobleDerecha] != ",":
                        llavesPrimeros = self.esNoTerminalPrim(gramaticaExpandida[key][1][indexDobleDerecha])  # Llaves donde se sacan los primeros
                        if llavesPrimeros != False:  # Si es nt se procede a colocar los primeros
                            gramaticaExpandida = self.colocarPrimeros(llavesPrimeros, llavesProducciones, gramaticaExpandida)
                        else:  # Si es un terminal se le colocan a las producciones
                            for llavesitas in llavesProducciones:
                                if self.hayAcompañantesYa(gramaticaExpandida[llavesitas][1]):
                                    gramaticaExpandida[llavesitas][1] += "|" + gramaticaExpandida[key][1][indexDobleDerecha]
                                else:
                                    gramaticaExpandida[llavesitas][1] += gramaticaExpandida[key][1][indexDobleDerecha]
                else:  # Si el punto esta al lado de la coma
                    pass
        gramaticaExpandida = self.correrAcompañantes(gramaticaExpandida)
        gramaticaExpandida = self.quitarAcompañantesRepetidos(gramaticaExpandida)
        return gramaticaExpandida

    """Devuelve la produccion al lado del punto, usar solo en producciones compuestas"""
    def produccionConPunto(self, producido):
        producido = producido[0:producido.find(",")]
        producido = producido.split(" ")
        for simbolo in producido:
            if simbolo.find(".") != -1:
                return simbolo.replace('.','')

    """usar solo en producciones compuestas"""
    def produccionLadoPunto(self, producido):
        if producido.find(".,") != -1:
            return ","
        producido = producido[0:producido.find(",")]
        producido = producido.split(" ")
        for index in range(len(producido)):
            if producido[index].find(".") != -1:
                if index + 1 == len(producido): #Si ya era lo ultimo
                    return ","
                else:
                    return producido[index+1] #si hay otro simbolo

    def quitarAcompañantesRepetidos(self, gramaticaExpandida):
        for key in gramaticaExpandida:
            if key != "_id":
                acompañante = gramaticaExpandida[key][2].split("|")
                for posI in range(len(acompañante)-1):
                    for posF in range(len(acompañante)-1):
                        if posI < posF:
                            if acompañante[posI] == acompañante[posF]:
                                acompañante.pop(posF)
                acompañanteAux = ""
                for pos in range(len(acompañante)): #Volvemos a convertir la list a string
                    acompañanteAux += acompañante[pos] + "|"
                acompañanteAux = acompañanteAux[0:len(acompañanteAux)-1]
                gramaticaExpandida[key][2] = acompañanteAux
        return gramaticaExpandida

    def colocarPrimeros(self, llavesPrimeros, llavesProducciones, gramaticaExpandida):
        primeros = self.buscarPrimeros(llavesPrimeros)
        print(primeros)
        if primeros[len(primeros)-1] == "|": #Quita un simbolo que resulta sobrando aveces
            primeros = primeros[0:len(primeros)-1]
        if primeros.find("lambda") != -1: #Este aplica para caso lambda nada mas
            print(gramaticaExpandida[self.key][1])
            llavesProduccionesAux = self.esNoTerminalPrim(gramaticaExpandida[self.key][1][self.indexPunto + 3])
            if not llavesProduccionesAux:
                primeros = "$|" + gramaticaExpandida[self.key][1][self.indexPunto + 3]
            else:
                primeros = "$|" + self.buscarPrimeros(llavesProduccionesAux)
        for llave in llavesProducciones:
            if self.hayAcompañantesYa(gramaticaExpandida[llave][1]): #aqui revisamos si ya hay algo
                gramaticaExpandida[llave][1] += "|" + primeros
            else:
                gramaticaExpandida[llave][1] += primeros
        return gramaticaExpandida

    """Retorna true o false dependiendo si hay o no acompañantes"""
    def hayAcompañantesYa(self, producido):
        tamaño = len(producido)
        posComa = producido.find(",") + 1
        if posComa == tamaño:
            return False
        else:
            return True

    def buscarPrimeros(self, llavesPrimeros):
        terminales = ""
        for llave in llavesPrimeros:  # Reviso cada llave
            if self.gramatica[llave][1].find("lambda") != -1: #si lo producido es lambda no se analiza
                letra = "lambda"
                noTerminal = self.esNoTerminalPrim(letra)
            elif self.gramatica[llave][1].find(" ") != -1:
                letra = self.gramatica[llave][1].split(" ")[0]
                noTerminal = self.esNoTerminalPrim(letra)
            else:
                letra = self.gramatica[llave][1][0]  # Reviso cada producido su primer caracter
                noTerminal = self.esNoTerminalPrim(letra)
            if noTerminal == False:  # Si es terminal lo guardo
                terminales += letra + "|"
            else:  # Encontro otro nt osea que hay que iterar
                terminales += self.buscarPrimeros(self.esNoTerminalPrim(letra))
        return terminales

    """Devuelve las llaves donde esta esos nt en la gramatica expandida o false si es terminal"""

    def esNoTerminalProd(self, simbolo):
        encontrada = False
        producciones = []
        for key in self.gramaticaExpandida:
            if key != "_id" and self.gramaticaExpandida[key][0] == simbolo:
                encontrada = True
                producciones.append(key)
        if encontrada:
            return producciones
        else:
            return False

    """Devuelve las llaves donde estan las prod en la gramatica original a las que se le sacan los primeros"""
    def esNoTerminalPrim(self, simbolo):
        encontrada = False
        producciones = []
        for key in self.gramatica:
            if key != "_id" and self.gramatica[key][0] == simbolo:
                encontrada = True
                producciones.append(key)
        if encontrada:
            return producciones
        else:
            return False

    def correccionIncertidumbre(self, primeros, gramaticaExpandida):
        # Corrige la incertidumbre de saber si tiene el acompañante#
        posicionComa = gramaticaExpandida["0"][1].find(",")
        gramaticaExpandida["0"][1] = gramaticaExpandida["0"][1][0:posicionComa + 1] + primeros
        return gramaticaExpandida

    def colocadaDeComas(self,gramaticaExpandida):
        for key in gramaticaExpandida:
            if key != "_id":
                if gramaticaExpandida[key][1].find(",") == -1:
                    gramaticaExpandida[key][1] = gramaticaExpandida[key][1] + ","
                if key == "0" and len(gramaticaExpandida[key]) > 2:
                    gramaticaExpandida[key][1] += gramaticaExpandida[key][2]
                    gramaticaExpandida[key].pop(2)
        return gramaticaExpandida

    def correrAcompañantes(self, gramaticaExpandida):
        for key in gramaticaExpandida:
            if key != "_id" and len(gramaticaExpandida[key]) < 3:
                tam = len(gramaticaExpandida[key][1])
                acompañante = gramaticaExpandida[key][1][gramaticaExpandida[key][1].find(",") + 1 : tam]
                gramaticaExpandida[key][1] = gramaticaExpandida[key][1][0:gramaticaExpandida[key][1].find(",")]
                gramaticaExpandida[key].append(acompañante)
        return gramaticaExpandida

    """Apartir de una llave obtiene los acompañantes puestos"""
    def getAcompañantesDeLaLLave(self,key, gramaticaExtendida):
        return gramaticaExtendida[key][1][gramaticaExtendida[key][1].find(",")+1:len(gramaticaExtendida[key][1])]

    def print(self,respuesta):
        for key in respuesta:
            print(key, " : ", respuesta[key])