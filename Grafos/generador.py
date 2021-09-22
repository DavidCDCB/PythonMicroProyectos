class Generador:
	def __init__(self,gr):
		self.gr=gr	
		self.dicAdyacencias={}#Diccionario con el resultado
		self.listaNodos=[]#La lista con la estructura de todas las gramaticas de los nodos
		self.listaProcesados=[]
		self.nId=0
		self.original={}
		self.nodos=[]
		self.nodosConexos=[]

		for k in self.gr.keys():
			self.original[k]=self.gr[k].copy()

		gramatica=self.recorrerJson(self.gr)

		#el parametro n es para que la gramatica se expanda a partir del nivel 1
		gramatica.setdefault("_id",0)
		print(gramatica)

		self.copyDic(gramatica)

		self.proceso(gramatica,0)
		print("\nProcesados",self.listaProcesados)
		self.printJson("\nAdyacencia:",self.dicAdyacencias)
		
		
		#print(self.expandir([['A', '(.A)'],['A', "( .A' )"]]))


		#print(self.punto(" id ").split(" "))
		
		#Recolectado de nodos clones
		dicRep={}
		for d in self.listaNodos:
			for d1 in self.listaNodos:
				if(self.toString(d).split("_id")[0]==self.toString(d1).split("_id")[0] and self.listaNodos.index(d)!=self.listaNodos.index(d1)):
					print(self.toString(d).split("_id")[1],self.toString(d).split("_id")[0])
					print(self.toString(d1).split("_id")[1],self.toString(d).split("_id")[0])
					if(self.toString(d).split("_id")[0] not in dicRep.keys()):
						dicRep[self.toString(d).split("_id")[0]]=99999
					
					if(int(self.toString(d).split("_id")[1])<int(dicRep[self.toString(d).split("_id")[0]])):
						dicRep[self.toString(d).split("_id")[0]]=self.toString(d).split("_id")[1]
						break
			
		#Ajuste en las adyacencias
		if(len(self.dicAdyacencias.keys())>0):
			
			for k in self.dicAdyacencias:
				for l in self.dicAdyacencias[k]:
					for k1 in dicRep.keys():
						if(l[2]==k1):
							l[1]=int(dicRep[k1])
							l[2]=""

			self.printJson("\n-------------Sin clones",self.dicAdyacencias)

			limpiada={}
			remover=[]
			
			

			#Eliminado de huerfanos
			for k1 in self.dicAdyacencias:
				conPadre=False
				for k in self.dicAdyacencias:
					for l in self.dicAdyacencias[k]:
						if(k1==l[1] or k1==0):
							if(l[1] not in self.nodosConexos):
								self.nodosConexos.append(l[1])
							conPadre=True
					
				if(conPadre):
					limpiada[k1]=self.dicAdyacencias[k1].copy()

			self.printJson("\n-------------Sin huerfanos",limpiada)
			self.nodosConexos.append(0)
			
			#Eliminar los nodos que no esté entre los conexos
			for d in self.listaNodos:
				if(d["_id"] not in self.nodosConexos):
					remover.append(d)
			for d in remover:
				print("Removido:",d["_id"])
				self.listaNodos.remove(d)
				
			#print(self.expandir([['A', '.B()']]))
			
			print("\n----------Banco de Nodos")
			for d in self.listaNodos:
				print(d)
		
			
	#asigna el punto al principio donde no halla espacios------------------------------------
	def punto(self,t):
		cad=""
		puesto=False
		for c in t:
			if(c!=" " and puesto==False):
				cad+="."+c
				puesto=True
			else:
				cad+=c
		return cad
		
	def printJson(self,t,d):
		print(t)
		for k in d.keys():
			print("\n"+str(k)+":")
			print("	"+str(d[k]))
		
	#Retorna el elemnto al lado del punto que no sea un espacio
	def vecino(self,string):
		posPunto=string.index(".")
		if(posPunto==len(string)-1):
			return "reduccion"
			
		if(" " not in string):
			if(posPunto+1<len(string)):
				return string[posPunto+1]

		else:
			for dat in string.split(" "):
				if("." in dat):
					posPunto=dat.index(".")
					if(posPunto+1<len(string)):
						return dat.split(".")[1]
			
					
		#Hacer caso en que no halla vecino
			
	def moverPunto(self,string):
		posPunto=string.index(".")
		lista=[]
		indPunto=0
		
		cad=""
		if(" " in string):
			cad=string.split(" ")
			for i in range(len(cad)):
				if("." in cad[i] and cad[i]!=""):
				
					if(i<len(cad)-1):
						cad[i]=cad[i].replace(".","")
						cad[i+1]="."+cad[i+1]
						break
					elif(i==len(string.split(" "))-1):
						cad[i]=cad[i].replace(".","")
						cad[i]=cad[i]+"."
						break
			return(" ".join(cad))
		
		for i in range(len(string)):
			if(posPunto<len(string)):
				if(i==posPunto):
					continue
				elif(i==posPunto+1):
					lista.append(string[i])
					lista.append(".")
				else:
					lista.append(string[i])

		return "".join(lista)
			

		
	#Recorre la gramatica para agregar los puntos
	def recorrerJson(self,d):
		modificado=d.copy()
		for k in modificado.keys():
			modificado.get(k)[1]=self.punto(modificado.get(k)[1])
		return modificado
			
	#Recibe una lista de producciones y entrega un json con llaves enumeradas por cada elemento
	def toJson(self,l):
		diccionario={}
		nEstado=0
		
		for dat in l:
			diccionario[str(nEstado)]=dat
			nEstado=nEstado+1
		
		return diccionario
		
	#Expande la gramatica al encontrar un no terminal al lado del punto
	def expandir(self,g):
		expansion=False
		expandido=[]
		elemento=()
		
		dimencion=0
		
		while(True):
			dimencion=len(g)
			lExpander=[]
		
			for k in range(len(g)):
				if(self.vecino(g[k][1])!="reduccion"):
					for k1 in self.original.keys():
						
						if(k1!='_id'):
							if(self.original[k1][0]==self.vecino(g[k][1]) and g[k][1]!=self.original[k1][1]):
								expansion=True
								
				if(expansion):
					lExpander.append(self.vecino(g[k][1]))
					print(lExpander)
					expansion=False

			for e in lExpander:
			
				for k in range(len(g)):
					
					if(self.vecino(g[k][1])!="reduccion"):
						for k1 in self.original.keys():
							if(k1!='_id'):
								#if(self.original[k1][0]==self.vecino(g[k][1]) and g[k][1]!=self.original[k1][1]):
								if(e==self.original[k1][0]):
									#Toma una copia de los elementos de la gramatica en una tupla
									elemento=[self.original[k1].copy()[0],self.original[k1].copy()[1]]
									elemento=[elemento[0],self.punto(elemento[1])]
									
									expandido.append(elemento)
									expansion=True
					for t in expandido:
						if(t not in g):
							g.append(t)
			
			if(dimencion==len(g)):
				break
			
		return g
		
	#Disminuye el numero de clones buscando y ubicando un nodo previamente procesado
	def comparar(self,lDic,dic):
		for k in lDic.keys():
			if(len(lDic)>0):
				if(len(lDic[k])==3):
					for l in lDic[k]:
						if(l[2]==dic):
							return (1,l[1])
			
		return (0,0)
		
	def toString(self,d):
		cad=""
		for k in d.keys():
			cad+=k
			if(k!='_id'):
				for v in d[k]:
					cad+=v
			else:
				cad+=str(d['_id'])
		return cad
		
	#Se evitan los ciclos verificando la lista de procesados
	def comparar1(self,lDic,dic,tipo,indCiclo):
		lCadP=[]
		for dat in lDic:
			lCadP.append(dat)
		
		for cad in lCadP:
			if(tipo==0):
				if(cad.split("_id")[0]==self.toString(dic)):
					print(self.toString(dic),"---",cad.split("_id")[0])
					indCiclo.append(cad.split("_id")[1])
					return True
			if(tipo==1):
				if(cad.split("_id")[0]==self.toString(dic).split("_id")[0]):
					print(self.toString(dic),"---",cad.split("_id")[0])
					indCiclo.append(cad.split("_id")[1])
					return True
				
		return False
		
	def copyDic(self,d):
		dAux={}
		for k in d.keys():
			if(k!='_id'):
				dAux[k]=d[k].copy()
			else:
				dAux[k]=d["_id"]
		self.listaNodos.append(dAux)
		
		
	def proceso(self,gramatica,n):

		#Expansion de gramatica...
		
		#print("---",gramatica)
		#print("----",self.listaProcesados)

		self.listaProcesados.append(self.toString(gramatica))
	
		auxDic={}
		dicEnumerado={}
		listaTransiciones=[]
		
		print("----------------------------------")
		self.printJson(str(n)+" Entrante",gramatica)
		
		#Se crea un json que agrupa segun las transiciones
		#Clave el elmento por el que se trancisiona
		#valor una lista de produciones involucradas
		for k in gramatica.keys():
		
			if(k!='_id'):
		
				if(self.vecino(gramatica.get(k)[1])!="reduccion"):
					posK=self.vecino(gramatica.get(k)[1])
					
					if(posK not in auxDic.keys()):
						auxDic[posK]=[]
						
					gramatica.get(k)[1]=self.moverPunto(gramatica.get(k)[1])
					auxDic[posK].append(gramatica.get(k))

		
		self.printJson("Agrupados:",auxDic)
		
		if(len(auxDic.keys())>0):
		
			#Se preparan los grupos como un diccionario independiente que se va a procesar
			#Ha cada trancision se le debe asignar un id nuevo si no fue procesado antes
			#Si fue procesado se debe asignar el id del encontrado
			for k in auxDic.keys():
			
				ciclo = False
				print("Expandido",self.expandir(auxDic[k]))
				
				dicEnumerado=self.toJson(auxDic[k])
				
				indCiclo=[]
				auxInd=0
				
				if(self.comparar1(self.listaProcesados,dicEnumerado,0,indCiclo)==False):
					self.nId=self.nId+1
				else:
					ciclo = True
					auxInd=self.nId
					self.nId=int(indCiclo[0])
					print("********* CICLO EN EL",self.nId)

					
				if(gramatica.get("_id") not in self.dicAdyacencias.keys()):
					self.dicAdyacencias[gramatica.get("_id")]=[]
				
				auxIndD=0
				auxIndD=self.comparar(self.dicAdyacencias,self.toString(dicEnumerado))[1]

				if(self.comparar(self.dicAdyacencias,self.toString(dicEnumerado))[0]==0):
					self.dicAdyacencias[gramatica.get("_id")].append([k,self.nId,self.toString(dicEnumerado)])
				else:
					self.dicAdyacencias[gramatica.get("_id")].append([k,auxIndD,self.toString(dicEnumerado)])
					
				if(ciclo):
					self.nId=auxInd
				else:
					#Recolecta las proximas transiciones
					dicEnumerado.setdefault("_id",self.nId)
					listaTransiciones.append(dicEnumerado)

			
		
			print(n,"proximos:")
			for d in listaTransiciones:
				print(d)
			
			#Recolecta las trancisiones en la lista de nodos
			for transicion in listaTransiciones:
				self.copyDic(transicion)
				

			for transicion in listaTransiciones:
				#indCiclo=[]
				#auxInd=0
				#if(self.comparar1(listaProcesados,transicion,1,indCiclo)==False):
				#input()
				print("\n\n")
				self.proceso(transicion,n+1)
				print("nivel",n)
				'''
				else:
					
					print("!!!!!",dicAdyacencias)
					for k in dicAdyacencias.keys():
						
						for l in dicAdyacencias[k]:
							if(str(l[1])==indCiclo[0]):
								l[1]=transicion["_id"]
					print("!!!!!",dicAdyacencias)
				'''
					
		else:
			print("Procesados:",self.listaProcesados)
			
if(__name__=="__main__"):

	'''


	gr={
		"0" : ["A","B()"],
		"1" : ["B","C"],
		"2" : ["B","+"],
		"3" : ["C","_"],
	}

	gr={
		"0" : ["A'","A"],
		"1" : ["A","(A)"],
		"2" : ["A","a"]
	}
	
	gr={
		"0" : ["E'","E+n"],
		"1" : ["E","n"]
	}
	'''



	gr={
		"0":["E","E+T"],
		"1":["E","T"],
		"2":["T","T*F"], 
		"3":["T","F"],
		"4":["F","(E)"],
		"5":["F"," id"]
	}


	obj=Generador(gr)

