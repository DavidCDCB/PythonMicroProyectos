#AGREGUÉ el metodo de prim(Requiere de revision)
import time,math


class Arista:
    def __init__(self, destino, peso, camino=[], bool_ruta=False):
        self.destino = destino      # Donde termina la tuberia
        self.peso= peso            # Peso de la tuberia
        self.bool_ruta = bool_ruta   # Determina si la ruta esta activa
        self.camino = camino

        
    def __str__(self):
        if self.bool_ruta is False:
            return str(">"+str(self.destino)+",capacidad"+str(self.capacidad)+"(Inactiva)")
        else:
            return str(">"+str(self.destino)+",capacidad"+str(self.capacidad))


class Grafo:
	def __init__(self):
		self.listaVertices = {}
		self.numVertices = 0
		self.aristas_eliminadas=[]
	
	def __str__(self):
		return str(self.vertices)
	
	def __iter__(self):  # Crear invocacion iterable del obj
		# retorna un obj iterable con los vertices
		return iter(self.listaVertices.keys())
	
	def __contains__(self, n):  # para usa el in obj
		return n in self.listaVertices
	
	def agregar_vertice(self, dato):
			self.listaVertices.update({dato: []})

	
	def obtener_aristas(self, n):  # obtiene la lista de aristas de un vertice respectivo
		if (n in self.listaVertices):
			return self.listaVertices.get(n)
		else:
			return None
	
	def obtener_vertices(self):
		return self.listaVertices.keys()
	
	def agregar_arista_d(self, origen, destino, peso, camino, bool_ruta):
		if origen in self.listaVertices and destino in self.listaVertices:
			self.listaVertices[origen].append(Arista(destino, peso, camino, bool_ruta))
	
	def agregar_arista(self, inicio, fin, peso=1, camino=[], bool_ruta=True):
		self.agregar_arista_d(inicio, fin, peso, camino, bool_ruta)
		self.agregar_arista_d(fin, inicio, peso, camino[::-1], not bool_ruta)
		
	def camino_arista(self,v1,v2):
		for arista in self.listaVertices[v1]:
			if arista.destino is v2:
				return arista.camino
		return None
	
	def elimina_arista(self,v1,v2):
		camino=None
		
		for arista in self.listaVertices[v1]:
			if arista.destino is v2:
				camino=arista.camino
				self.listaVertices[v1].remove(arista)
				
		for arista in self.listaVertices[v2]:
			if arista.destino is v1:
				camino = arista.camino
				self.listaVertices[v2].remove(arista)
				
		self.aristas_eliminadas.append((v1,v2,camino))
		
		
	def cambia_ruta_arista(self,v1,v2):
		a1,a2=(None,None)
		
		for arista in self.listaVertices[v1]:
			if arista.destino is v2:
				a1=arista
		
		for arista in self.listaVertices[v2]:
			if arista.destino is v1:
				a2=arista
				
		if a1.bool_ruta is False:
			a1.bool_ruta=True
			a2.bool_ruta = False
			
		else:
			a1.bool_ruta=False
			a2.bool_ruta = True
		
	def devuelve_vertice_num(self,num):
		for vertice in self.listaVertices:
			if vertice.num is num:
				return vertice
			
		return None

	

	def recorrer(self, inicial, tip):  # tip: 0 anchura -1 profundidad
		visitados = []
		lista = []  # funciona como pila o cola segun la posicion 0 el primero -1 el ultimo
		capturados = []
		lista.append(inicial)
		visitados.append(inicial)
		
		if (inicial in self):
			while (lista):
				capturados.append(lista[tip])
				
				for a in self.listaVertices.get(lista.pop(tip)):
					if (a.destino not in visitados):
						visitados.append(a.destino)
						lista.append(a.destino)
		
		return str(capturados)
	
	
	# se requiere la clase math
	def masCercano(self, coo=(5, 5), lista=[(2, 7), (3, 1), (5, 8)]):
		cMenor, aMenor = (None, None)
		
		def cercania(a, b):
			return int(math.sqrt(math.pow((b[0] - a[0]), 2) + math.pow((b[1] - a[1]), 2)))
		
		for c in lista:
			print(cercania(coo, c))
			if (aMenor is None or cercania(coo, c) < aMenor):
				aMenor = cercania(coo, c)
				cMenor = c
		
		return cMenor
	
	
	def caminos(self, va, vb, visitados):
		if (va == vb):
			print(visitados)
			return visitados
		
		for a in self.listaVertices.get(va):
			print(a.destino)
			
			if (a.destino not in visitados):
				visitados.append(a.destino)
				self.caminos(a.destino, vb, visitados)
				visitados.pop(-1)
	
	
	def verM(self, m):
		print("-------")
		for i in range(len(m)):
			cad = ""
			for j in range(len(m)):
				cad += "|" + str(m[i][j])
			print(cad)
	
	
	def back(self, f, c, m, coo, mcoo):
		# print(mcoo)
		
		# time.sleep(0.1)
		self.verM(m)
		
		if (f > len(m) - 1 or f < 0):
			return mcoo
		
		if (c > len(m) - 1 or c < 0):
			return mcoo
		
		if (m[f][c] is 2 or m[f][c] is 3 or m[f][c] is 1):
			return mcoo
		
		coo.append((f, c))
		
		if (m[f][c] is 5):
			for i in range(len(m)):
				for j in range(len(m)):
					if (m[i][j] is 1): m[i][j] = 0
			
			if (len(mcoo) == 0 or len(coo) < len(mcoo)):
				mcoo = coo.copy()
			
			print("!!!!")
			return mcoo
		
		m[f][c] = 2
		
		mcoo = self.back(f + 1, c, m, coo, mcoo);
		mcoo = self.back(f, c + 1, m, coo, mcoo);
		mcoo = self.back(f - 1, c, m, coo, mcoo);
		mcoo = self.back(f, c - 1, m, coo, mcoo);
		coo.pop(-1)
		m[f][c] = 1
		
		return mcoo
	
	
	def prim(self, inicial):  # resive el dato del Vertice inicial
		visitados = []
		aristas = []  # aristas recolectadas
		cMayor = 0  # costo MAYOR de los ad
		menor = None
		
		vertice = inicial  # se concidera el vertice como el dato
		visitados.append(vertice)
		
		while (len(visitados) <= len(self.listaVertices.keys()) - 1):
			for v in visitados:
				# se optiene la lista de aristas de un vertice determinado
				for a in self.listaVertices[v]:
					if (a.destino not in visitados):
						if (cMayor == 0 or a.peso >= cMayor):
							menor = a
							cMayor = a.peso
							vertice = v
			

			aristas.append((vertice, menor.destino))
			visitados.append(menor.destino)
			vertice = menor.destino  # se optiene siguiente a revisar
			
			cMayor = 0
		
		#for i in aristas:
		#	print(i[0], "--", i[1])
		
		return aristas  # entrega una lista de las aristas optimas
	
	
	# dada la coordenada(tupla x,y) inicial y final escoje el camino segun el tipo
	# tipo 0 primero vertical, tipo 1 primero horizontal
	def conexion(self, ci, cf, tip=0):
		camino = []
		
		# ci,cf=(5,5),(2,8)
		
		if (cf[0] >= ci[0] and cf[1] >= ci[1]):  # abajo derecha
			sentido1 = 1
			sentido2 = 1
		
		if (cf[0] >= ci[0] and cf[1] <= ci[1]):  # abajo izquierda
			sentido1 = 1
			sentido2 = -1
		
		if (cf[0] <= ci[0] and cf[1] >= ci[1]):  # arriba derecha
			sentido1 = -1
			sentido2 = 1
		
		if (cf[0] <= ci[0] and cf[1] <= ci[1]):  # arriba izquierda
			sentido1 = -1
			sentido2 = -1
		
		if (tip == 0):
			coo1 = 0
			recorrido1 = range(ci[coo1], cf[coo1] + sentido1, sentido1)
			ci = (cf[0], ci[1])
			coo2 = 1
			recorrido2 = range(ci[coo2], cf[coo2] + sentido2, sentido2)
			
			for i in recorrido1:
				camino.append((i, ci[1]))
				print("-", (i, ci[1]))
			
			for j in recorrido2:
				camino.append((ci[0], j))
				print((ci[0], j))
		
		if (tip == 1):
			coo1 = 1
			recorrido1 = range(ci[coo1], cf[coo1] + sentido2, sentido2)
			ci = (ci[0], cf[1])
			coo2 = 0
			recorrido2 = range(ci[coo2], cf[coo2] + sentido1, sentido1)
			
			for j in recorrido1:
				camino.append((ci[0], j))
				print((ci[0], j))
			
			for i in recorrido2:
				camino.append((i, ci[1]))
				print("-", (i, ci[1]))
		
		return camino
	
	
	def floyd(self):  # Resive los id de dos vertices especificos
		lCo = []
		dim = len(self.listaVertices.keys())  # numero de vertices
		m1 = [[0] * dim for i in range(dim)]  # matriz de pesos
		m2 = [[" "] * dim for i in range(dim)]  # matriz de vertices
		lv = list(self.listaVertices.keys())  # lista de objetos
		piv = 0  # Pivote
		
		def verM(m):
			print("-------")
			for i in range(len(m)):
				cad = ""
				for j in range(len(m)):
					cad += "|" + str(m[i][j])
				print(cad)
		
		def mayorCamino(m):
			mayor, inicio, fin = 0, 0, 0
			
			for i in range(len(m)):
				for j in range(len(m)):
					if (m[i][j] != "X"):
						if (int(m[i][j]) >= mayor):
							inicio = i
							fin = j
							mayor = int(m[i][j])
			
			return (inicio, fin)
		
		def buscarPorId(n):
			for dat in lv:
				if (dat.num == n): return dat
		
		# llenado de letras en vertical
		"""
		for i in range(len(m2)):
			for j in range(len(m2)):
				m2[i][j]=lv[j].id
		"""
		# asignacion de alcanze de aristas por cada V
		for v, la in self.listaVertices.items():
			for a in la:
				m1[lv.index(v)][lv.index(a.destino)] = a.peso
		
		# Asignacion de no alcanzados y deagonal
		for i in range(len(m1)):
			for j in range(len(m1)):
				if (i == j):
					m1[i][j] = "X"
				elif (m1[i][j] == 0):
					m1[i][j] = -1
		
		verM(m1)
		
		while (piv < dim):
			for f in range(len(m1)):
				for c in range(len(m1)):
					# si su equivalente pivote no es -1 ni X y la actual a analizar no es X
					if (m1[piv][c] is not -1 and m1[f][piv] is not -1):
						if (m1[f][c] is not "X" and (f is not piv and c is not piv) and (
								m1[piv][c] is not "X" and m1[f][piv] is not "X")):
							if (m1[f][piv] + m1[piv][c] > m1[f][c]):  # si encunetra un camino mayor
								m1[f][c] = (m1[f][piv] + m1[piv][c])  # lo reasigna a la matriz de pesos
								m2[f][c] = lv[piv].num  # y el pivote a la matriz de vertices
			piv += 1
			print("Pivote:", piv)
			verM(m1)
			verM(m2)
		
		# establece el punto A Y B
		A = lv[mayorCamino(m1)[0]].num
		B = lv[mayorCamino(m1)[1]].num
		
		lCo.append(buscarPorId(A))  # agrega el inicio del camino
		
		for v in m2[lv.index(buscarPorId(A))]:  # agrega los intermedios
			if (v != " "):
				lCo.append(buscarPorId(v))
		
		lCo.append(buscarPorId(B))  # y el final del camino
		
		# Entrega la lista de vertices que conforman el camino mayor
		for i in list(set(lCo)):
			print("---", i.num)
		
		lPar = []
		
		for x in list(set(lCo)):  # recorro los implicados(objetos)
			for i in self.listaVertices.get(buscarPorId(x.num)):  # recorro sus adyacentes de cada implicado
				
				for j in list(set(lCo)):
					if (i.destino.num == j.num):  # si su adyacente esta en los implicados
						lPar.append((x, i.destino))
		
		for i in lPar:
			print(i[0], "-", i[1])
		
		return lPar
	
	
	def floydE(self, A="A", B="D"):  # Resive los id de dos vertices especificos
		lCo = []
		dim = len(self.listaVertices.keys())  # numero de vertices
		m1 = [[0] * dim for i in range(dim)]  # matriz de pesos
		m2 = [[" "] * dim for i in range(dim)]  # matriz de vertices
		lv = list(self.listaVertices.keys())  # lista de objetos
		piv = 0  # Pivote
		
		def verM(m):
			print("-------")
			for i in range(len(m)):
				cad = ""
				for j in range(len(m)):
					cad += "|" + str(m[i][j])
				print(cad)
		
		def buscarPorId(n):
			for dat in lv:
				if (dat == n): return dat
		
		# llenado de letras en vertical
		"""
		for i in range(len(m2)):
			for j in range(len(m2)):
				m2[i][j]=lv[j].id
		"""
		# asignacion de alcanze de aristas por cada V
		for v, la in self.listaVertices.items():
			for a in la:
				m1[lv.index(v)][lv.index(a.destino)] = a.peso
		
		# Asignacion de no alcanzados y deagonal
		for i in range(len(m1)):
			for j in range(len(m1)):
				if (i == j):
					m1[i][j] = "X"
				elif (m1[i][j] == 0):
					m1[i][j] = -1
		
		verM(m1)
		
		while (piv < dim):
			for f in range(len(m1)):
				for c in range(len(m1)):
					# si su equivalente pivote no es -1 ni X y la actual a analizar no es X
					if (m1[piv][c] is not -1 and m1[f][piv] is not -1):
						if (m1[f][c] is not "X" and (f is not piv and c is not piv) and (
								m1[piv][c] is not "X" and m1[f][piv] is not "X")):
							if (m1[f][piv] + m1[piv][c] > m1[f][c]):  # si encunetra un camino mayor
								m1[f][c] = (m1[f][piv] + m1[piv][c])  # lo reasigna a la matriz de pesos
								m2[f][c] = lv[piv]  # y el pivote a la matriz de vertices
			piv += 1
			print("Pivote:", piv)
			verM(m1)
			verM(m2)
		
		lCo.append(buscarPorId(A))
		
		for v in m2[lv.index(buscarPorId(A))]:
			if (v != " "):
				lCo.append(buscarPorId(v))
		
		lCo.append(buscarPorId(B))
		
		# Entrega la lista de vertices que conforman el camino mayor
		return lCo
	
	
	def ver(self):
		for V in self:  # itera sobre los vertices del obj G iterable
			print("VERTICE-->PESO>ADYACENTES")
			print(V, "-->", [str(x.peso) + ">" + str(x.destino) for x in self.listaVertices.get(V)])
	
	
	
	
	
