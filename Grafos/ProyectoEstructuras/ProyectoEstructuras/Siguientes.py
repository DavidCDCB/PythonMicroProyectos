class Gramatica():

    def __init__(self, gramatica,inicial,lista_Noterminales, lista_terminales):
        self.gramatica=gramatica
        self.inicial=inicial
        self.lista_noterminales= lista_Noterminales
        self.lista_terminales = lista_terminales

        self.primeros={}
        self.siguientes={}
        self.crea_primeros()
        self.crea_siguientes()

        print("Los primeros son")
        print(self.primeros)
        print("Los siguientes son")
        print(self.siguientes)


    def crea_primeros(self):
        """Paso 0-Se crea el diccionario de primeros"""
        for noterminal in self.lista_noterminales:
            self.primeros[noterminal] = []

        """Paso 1-Se dejan indicados los que tengan #-lambda"""
        for key,value in self.gramatica.items():
            if key is not "_id":
                elemento=value[0]
                producciones=value[1]
                lista=self.separa_producciones(producciones)

                if lista[0] == "lambda":
                    self.primeros[elemento]=self.union_listas(self.primeros[elemento],["lambda"])


        """Paso 2-Se dejan indicados si son no terminales, si es termianl se ignora"""
        for key,value in self.gramatica.items():
            if key is not "_id":
                elemento=value[0]
                producciones=value[1]
                lista=self.separa_producciones(producciones)

                """1-Primero se dejan indicados"""
                listaAux=lista[:]

                while len(listaAux)!=0:
                    elemento_aux=listaAux.pop(0)

                    if self.es_terminal(elemento_aux):
                        """Si se encuentra un terminal se agrega a la lista y se sale"""
                        if elemento_aux not in self.primeros[elemento]:
                            self.primeros[elemento] =self.union_listas(self.primeros[elemento],[elemento_aux])
                        break

                    elif self.es_noterminal(elemento_aux):
                        """Si se encuentra un no terminal se analiza"""

                        if elemento_aux not in self.primeros[elemento]:
                            """Si los primeros de yn no estan indicado en los primeros de x se agregan"""
                            self.primeros[elemento]=self.union_listas(self.primeros[elemento],[elemento_aux])

                        if "lambda" in self.primeros[elemento_aux]:
                            """Si lambda esta los primeros de yn, se analiza si es el ultimo"""
                            if len(listaAux) == 0:
                                self.primeros[elemento] = self.union_listas(self.primeros[elemento], ["lambda"])

                        else:
                            """de lo contrario, se acaba el ciclo"""
                            listaAux = ""

        """Paso 3-Se itera los primeros reemplazando los indicados hasta que ya no hayan mas de estos"""
        cambio=True

        while cambio==True:
            """Se mantiene en falso hasta que haya algun cambio, de no ser asi, el ciclo termina"""
            cambio=False

            for noterminal,primero in self.primeros.items():
                for elemento in primero:

                    if self.es_noterminal(elemento):
                        """Si se encuentra un indicado se procede a reemplazarlo"""

                        """Se elimina el indicado de los primeros"""
                        primero.remove(elemento)

                        """Se crea una lista con los primeros de Yn sin lambda"""
                        lista_aux=self.primeros[elemento][:]
                        if "lambda" in lista_aux:
                            lista_aux.remove("lambda")

                        """Se reemplaza el valor del indicado"""
                        self.primeros[noterminal]= self.union_listas(self.primeros[noterminal],lista_aux)

                        """Se indica que hubo un cambio, por lo cual hay otra iteracion"""
                        cambio=True

    def crea_siguientes(self):


        """Paso 0-Se crea el diccionario de siguientes"""
        for noterminal in self.lista_noterminales:
            self.siguientes[noterminal] = []

        self.siguientes[self.inicial]=["$"]

        """Paso 2-Se analizan los no terminales de la siguiente forma
               1-Si hay una produccion Z=>a...aXY, entonces los primeros(Y) que no sean epsilon se agregan a siguientes(X)
               2-Si hay una produccion Z=>a...aXY, se debe tener en cuenta el lambda
               3-Si hay una produccion Z=>aX, entonces los siguientes(Z) se agregan a siguientes(X)

               """

        for key,value in self.gramatica.items():
            if key is not "_id":
                elemento=value[0]
                producciones=value[1]
                lista=self.separa_producciones(producciones)

                """1-Primero se dejan indicados"""
                listaAux=lista[:]

                for i in range(len(lista)):
                    elemento_inicial = lista[i]

                    if self.es_noterminal(elemento_inicial):
                        if i + 1 < len(lista):
                            for j in range(i + 1, len(lista)):
                                elemento_sig = lista[j]

                                if self.es_terminal(elemento_sig):
                                    """Caso 1a-se agrega los primeros del elemento siguiente terminal"""
                                    self.siguientes[elemento_inicial] = self.union_listas(self.siguientes[elemento_inicial],
                                                                                  [elemento_sig])
                                    break


                                else:
                                    """Caso 1b-se agrega los primeros del elemento siguiente no terminal sin lambda"""
                                    primeros_aux = self.primeros[elemento_sig][:]
                                    if "lambda" in primeros_aux:
                                        primeros_aux.remove("lambda")

                                    self.siguientes[elemento_inicial] = self.union_listas(self.siguientes[elemento_inicial],
                                                                                  primeros_aux)

                                    """Caso 3-Los siguientes de Z se agregan a los siguientes de X
                                    ---creo que hay un error en el caso 3, luego reviso bien--
                                    """
                                    if j + 1 == len(lista):
                                        self.siguientes[elemento_inicial] = self.union_listas(self.siguientes[elemento_inicial], [elemento])

                                    """Caso 2-si no existe un lamda en los primeros del elementos siguientes se termina el ciclo"""
                                    if "lambda" not in self.primeros[elemento_sig]:
                                        break

                        """Caso 3-Los siguientes de Z se agregan a los siguientes de X"""
                        if i + 1 == len(lista) and self.es_noterminal(elemento):
                            self.siguientes[elemento_inicial] = self.union_listas(self.siguientes[elemento_inicial], [elemento])


        """Paso 3-Se itera los primeros reemplazando los indicados hasta que ya no hayan mas de estos"""
        cambio = True

        while cambio == True:
            """Se mantiene en falso hasta que haya algun cambio, de no ser asi, el ciclo termina"""
            cambio = False

            for noterminal,siguientes in self.siguientes.items():
                for elemento in siguientes:
                    if self.es_noterminal(elemento):
                        """Si se encuentra un indicado se procede a reemplazarlo"""

                        """Se elimina el indicado de los siguientes"""
                        siguientes.remove(elemento)

                        """Se crea una lista con los siguientes de Yn"""
                        lista_aux = self.siguientes[elemento][:]

                        """Se reemplaza el valor del indicado"""
                        self.siguientes[noterminal] = self.union_listas(self.siguientes[noterminal], lista_aux)

                        """Se indica que hubo un cambio, por lo cual hay otra iteracion"""
                        cambio = True

    def separa_producciones(self, derivaciones):

        """Convierte el string de producciones en una lista para facilitar su manejo"""
        lista_derivaciones=derivaciones.split(" ")
        lista_nueva = []
        elemento_aux = ""

        for derivacion in lista_derivaciones:
            if derivacion in self.lista_noterminales or derivacion in self.lista_terminales or derivacion== 'lambda':
                lista_nueva.append(derivacion)

            else:
                lista_aux = list(derivacion)
                while len(lista_aux) != 0:
                    elemento_aux = elemento_aux + lista_aux.pop(0)

                    if elemento_aux in self.lista_noterminales or elemento_aux in self.lista_terminales or elemento_aux == 'lambda':
                        lista_nueva.append(elemento_aux)
                        elemento_aux = ""

        return lista_nueva

    """
    def separa_produccionesA(self,derivaciones, lista_terminales, lista_noterminales):
        lista_aux=list(derivaciones)
        lista_nueva=[]
        elemento_aux =""

        while len(lista_aux)!=0:
            elemento_aux=elemento_aux+lista_aux.pop(0)

            if elemento_aux in lista_noterminales or elemento_aux in lista_terminales or elemento_aux=='lambda':
                lista_nueva.append(elemento_aux)
                elemento_aux=""

        return lista_nueva
    """

    def es_terminal(self,elemento):
        """Devuelve True si el dato ingresado es terminal"""

        return elemento in self.lista_terminales

    def es_noterminal(self,elemento):
        """Devuelve True si el dato ingresado es no terminal"""
        return elemento in self.lista_noterminales

    def union_listas(self,lista_a,lista_b):
        """Genera la union de dos listas sin datos repetidos"""
        return lista_a + [i for i in lista_b if i not in lista_a]

    def devuelve_primero(self, elemento, lista_noterminales):
        if elemento in lista_noterminales:
            return self.primeros[elemento]
        else:
            return [elemento]

    def devuelve_siguientes(self, elemento, lista_noterminales):
        if elemento in lista_noterminales:
            return self.siguientes[elemento]
        else:
            return [elemento]





