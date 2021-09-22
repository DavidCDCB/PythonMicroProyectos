from Generador2 import Generador2
from Siguientes import Gramatica
from Tabla import Graficador

class Generador:
	def __init__(self,gr,tipo):
		self.gr=gr	
		self.dicAdyacencias={}#Diccionario con el resultado
		self.limpiada={}#Resultado limpiado
		self.listaNodos=[]#La lista con la estructura de todas las gramaticas de los nodos
		self.listaProcesados=[]
		self.nId=0
		self.original={}
		self.originalPuntos={}
		self.nodos=[]
		self.nodosConexos=[]
		self.tipo=tipo;

		for k in self.gr.keys():
			self.original[k]=self.gr[k].copy()

		#Enumera la gramatica
		self.gramatica=self.recorrerJson(self.gr)
		#el parametro n es para que la gramatica se expanda a partir del nivel 1
		self.gramatica.setdefault("_id",0)
		
		for k in self.gramatica.keys():
			if(k!="_id"):
				self.originalPuntos[k]=self.gramatica[k].copy()
		
		if(self.tipo=='lr1'):
			print("--->",self.originalPuntos)
			obj=Generador2(self.originalPuntos)
			#Si es lr1 debe generar el estado 0 a partir del original
			self.generar0(self.gramatica)
			print("--->",self.gramatica)
			print(obj.start("$",self.gramatica))
			print("--->",self.gramatica)
			
			

		#Recolecta el estado 0 en el banco de nodos
		self.copyDic(self.gramatica)
		
		self.proceso(self.gramatica,0)
		print("\nProcesados",self.listaProcesados)
		self.printJson("\nAdyacencia:",self.dicAdyacencias)
		
		
		#print(self.expandir([['A', '(.A)'],['A', "( .A' )"]]))

		#print("--->",self.gramatica["0"])
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
					self.limpiada[k1]=self.dicAdyacencias[k1].copy()

			self.printJson("\n-------------Sin huerfanos",self.limpiada)
			self.nodosConexos.append(0)

			#Eliminar los nodos que no esté entre los conexos
			for d in self.listaNodos:
				if(d["_id"] not in self.nodosConexos or "lambda" in d["0"][1]):
					remover.append(d)
			for d in remover:
				print("Removido:",d["_id"])
				self.listaNodos.remove(d)
				
			#print(self.expandir([['A', '.B()']]))
			
			proLambda=[]
			for k in self.limpiada:
				for l in self.limpiada[k]:
					if(l[0]=='lambda'):
						proLambda.append((k,l))
						
			for l in proLambda:
				 self.limpiada[l[0]].remove(l[1])
			
			
			print("\n----------Banco de Nodos")
			for d in self.listaNodos:
				print(d)
		
	def tabla(self):
		m=[]
		Nt=[]
		T=[]
		caracteres=[]
		elementos=[]
		nNodos=[]
		reducidos=[]
		nNodos.append(0)
		
		for k in self.original.keys():
			if(k!='_id'):
				if(len(Nt)==0 or self.original[k][0] not in Nt):
					Nt.append(self.original[k][0])

		for k in self.original.keys():
			if(k!="_id"):
				if(" " not in self.original[k][1]):
					caracteres[:0]=self.original[k][1]
					for i in range(len(caracteres)):
						if(caracteres[i] not in Nt):
							if(len(T)==0 or caracteres[i] not in T):
								if(caracteres[i]!="" and caracteres[i]!=" " and caracteres[i]!="lambda"):
									T.append(caracteres[i])
				else:
					caracteres=self.original[k][1].split(" ")
					for i in range(len(caracteres)):
						if(caracteres[i] not in Nt):
							if(len(T)==0 or caracteres[i] not in T):
								if(caracteres[i]!="" and caracteres[i]!=" " and caracteres[i]!="lambda"):
									T.append(caracteres[i])
		Nt.append("$")
		elementos=Nt+T
		for k in self.limpiada.keys():
			for di in self.limpiada[k]:
				if(len(nNodos)==0 or di[1] not in nNodos):
					nNodos.append(di[1])
					
		print("Terminos: ",elementos)
		print("Nodos",nNodos)
		
		m=[[""] * len(elementos) for x in range(len(nNodos))]
		
		for k in self.limpiada.keys():
			for di in self.limpiada[k]:
				if(di[0] not in Nt):
					m[nNodos.index(k)][elementos.index(di[0])]=str(di[1])
				else:
					m[nNodos.index(k)][elementos.index(di[0])]="D"+str(di[1])
				
		
		for i in range(len(m)):
			cad=""
			for j in range(len(m[0])):
				cad=cad+"  "+str(m[i][j])
			print(cad)
			
		for k in self.limpiada.keys():
			for di in self.limpiada[k]:
				if(di[1] not in self.limpiada.keys()):
					if(len(reducidos)==0 or di[1] not in reducidos):
						reducidos.append(di[1])
					
		print("REDUCIDOS:",reducidos)
		

		print("Original",self.original)
		print("Terminales",T)
		print("NO Terminales",Nt)
		print("inicial",self.original["0"][0])
		
		ls=Nt[:]
		ls.remove("$")
		print("---",ls)
		obj=Gramatica(self.original,self.original["0"][0],ls,T)
		siguientes=obj.siguientes
		
		print("SIGUIENTES",siguientes)
		
		for r in reducidos:
			for d in self.listaNodos:
				if(r==d["_id"]):
					print(d['0'][0],r)
					for s in siguientes[d['0'][0]]:
						if(s=='$' and reducidos.index(r)==0):
							m[nNodos.index(r)][elementos.index(s)]='Acep.'
						else:
							m[nNodos.index(r)][elementos.index(s)]='R'+str(r)
							
		
		
		
		'''
		open("solucion.txt","w").close()
		archivoW = open("solucion.txt","a")
		archivoW.write("TABLA DE SOLUCION:\n\n")
		self.verM(m,archivoW,nNodos,elementos)
		archivoW.close()
		'''
		
		tab=Graficador(m,elementos,nNodos)
		
		
		
		
		
	#matriz,archivo,etiquetasFilas,etiquetasColumnas
	def verM(self,m,f,fil,col):
		buffer=""
		for dat in col:
			if(col.index(dat)==0):
				buffer=buffer+"    |"+self.ft(str(dat),5)
			else:
				buffer=buffer+self.ft(str(dat),4)
		buffer=buffer+"\n"
		
		for i in range(0,len(m)):
			buffer=buffer+self.ft(str(fil[i]),4)
			for j in range(0,len(m[0])):
				buffer=buffer+self.ft(str(m[i][j]),4)
			buffer=buffer+"\n"
		f.write(buffer+"\n")
		
	#Asigna espacios uniformes a un String
	def ft(self,string,esp):
		espacios=esp-len(string)
		for i in range(espacios):
			string=string+" "
		return string+"| "
		
	def generar0(self,gr):
		producciones=[]
		for k in gr.keys():
			if(gr[k] not in self.expandir([gr["0"]])):
				producciones.append(k)
		for e in producciones:
			if(e!="_id"):
				del self.gramatica[e]
	
			
	#busca la R equivalente a la gramatica
	def buscarR(self,nt,t):
		for k in self.original.keys():
			if(k!='_id'):
				if(nt==self.original[k][0] and t.split(".")[0] == self.original[k][1]):
					print("****************************")
					return "-R"+str(list(self.original.keys()).index(k));
					
					
		return ""

			
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
					#print(lExpander)
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
					
					#if(d[k].index(v)<2):
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
				#print("COMPARANDO\n",cad.split("_id")[0],"\n",self.toString(dic))
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
		
		
	def conGramatica(self,gr):
		valor=True
		for k in gr.keys():
			if(k!='_id'):
				if(len(gr[k])==2):
					return False
		return valor
		
	def proceso(self,gramatica,n):
		obj=Generador2(self.originalPuntos)
		#Expansion de gramatica...
		
		#print("---",gramatica)
		#print("----",self.listaProcesados)

		self.listaProcesados.append(self.toString(gramatica))
	
		auxDic={}
		dicEnumerado={}
		listaTransiciones=[]
		
		print("----------------------------------")
		self.printJson(str(n)+" Entrante",gramatica)
		#input()
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
				
				print(auxDic[k],"Expandido",self.expandir(auxDic[k]))
				
				dicEnumerado=self.toJson(auxDic[k])
				
				if(self.tipo=='lr1'):
					if(self.conGramatica(dicEnumerado)==False):
						print("------------->",dicEnumerado)
						print("<-------------",obj.start(dicEnumerado["0"][2],dicEnumerado))
				
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
				if(self.tipo=='lr1'):
					if(self.conGramatica(d)==False):
						print("--->",d)
						print("<--",obj.start(d["0"][2],d))
			
			#Recolecta las trancisiones en la lista de nodos
			for transicion in listaTransiciones:
				self.copyDic(transicion)
				

			for transicion in listaTransiciones:
				#indCiclo=[]
				#auxInd=0
				#if(self.comparar1(listaProcesados,transicion,1,indCiclo)==False):
				#input()
				print("\n\n")
				
				print(transicion["0"][1])
				if('lambda' not in transicion["0"][1]):
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
			
			
			
			
''''
	def setAcom(self,gOriginal,gr,aIni):
		caracteres=[]
		nt=[]
		for k in gr.keys():
			if(k!="_id"):
				nt.append(gr[k][0])
		
		elemento=""
		
		for k in gr.keys():
			if(k!="_id"):
				if(" " not in gr[k][1]):
					caracteres[:0]=gr[k][1]
					for i in range(len(caracteres)):
						if(caracteres[i]=="." and i<len(caracteres)-1):
							
							if(caracteres[i+1] in nt):
								elemento=caracteres[i+1]
						
							if(i==len(caracteres)-2):
								gr[k].append(aIni)
								break;
							elif(i<len(caracteres)-2):
								gr[k].append(caracteres[i+2])
								break;
								print("------")
								
'''