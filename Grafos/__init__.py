from Grafo import Grafo

import json

if(__name__=="__main__"):
	print("hola")
	#m=[[0] * 3 for i in range(3)]
	
	nV=list("ABCDE")
	
	m=[[0,2,0,5,0],#dfd
	   [0,0,14,5,0],
	   [0,0,0,0,34],
	   [0,0,0,0,58],
	   [0,0,34,0,0]]
	
	
	g=Grafo()#Un obj Grafo contiene un diccionario {"DATO",objV("DATO",{adyacente-objV,ponderación})}
	
	g.matrisAd(m, nV)

	#g.ver()
	#print(g.recorrer("A", 0))#0 anchura -1 profundidad
	#print(g.recorrer("A", -1))
		
	
	
	#for dat in g.Dijkstra("A","E"):
	 #   print(dat.id)
	
	#print([x for x in iter([1,2,3])])
	
	
	dicAdyacencias={}
	listaProcesados=[]
	listaNodos=[]
	nId=0
	
	'''



	gr={
		"0" : ["A'","A"],
		"1" : ["A","(A)"],
		"2" : ["A","a"]
	}


	gr={
		"0" : ["A","B()"],
		"1" : ["B","C"],
		"2" : ["B","+"],
		"3" : ["C","_"],
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


	
	def punto(t):
		cad=""
		puesto=False
		for c in t:
			if(c!=" " and puesto==False):
				cad+="."+c
				puesto=True
			else:
				cad+=c
		return cad
		
	def printJson(t,d):
		print(t)
		for k in d.keys():
			print("\n"+str(k)+":")
			print("	"+str(d[k]))
		
	def vecino(string):
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
			
	def moverPunto(string):
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
			
		#Hacer caso en que el punto esté al final
		
	#Recorre la gramatica para agregar los puntos
	def recorrerJson(d):
		modificado=d.copy()
		for k in modificado.keys():
			modificado.get(k)[1]=punto(modificado.get(k)[1])
		return modificado
			
	#Recibe una lista de producciones y entrega un json con llaves enumeradas por cada elemento
	def toJson(l):
		diccionario={}
		nEstado=0
		
		for dat in l:
			diccionario[str(nEstado)]=dat
			nEstado=nEstado+1
		
		return diccionario
		
	def expandir(g):
		global original
		expansion=False
		expandido=[]
		elemento=()
		
		dimencion=0
		
		while(True):
			dimencion=len(g)
			lExpander=[]
		
			for k in range(len(g)):
				if(vecino(g[k][1])!="reduccion"):
					for k1 in original.keys():
						
						if(k1!='_id'):
							#print(original[k1][0],'_______________________________',vecino(g[k][1]))
							if(original[k1][0]==vecino(g[k][1]) and g[k][1]!=original[k1][1]):
								expansion=True
								
				if(expansion):
					lExpander.append(vecino(g[k][1]))
					expansion=False

			#print('_______________________________',lExpander)
			
			for e in lExpander:
			
				for k in range(len(g)):
					
					if(vecino(g[k][1])!="reduccion"):
						for k1 in original.keys():
							if(k1!='_id'):
								#if(original[k1][0]==vecino(g[k][1]) and g[k][1]!=original[k1][1]):
								if(e==original[k1][0]):
									#Toma una copia de los elementos de la gramatica en una tupla
									elemento=[original[k1].copy()[0],original[k1].copy()[1]]
									elemento=[elemento[0],punto(elemento[1])]
									
									expandido.append(elemento)
									expansion=True
					for t in expandido:
						if(t not in g):
							g.append(t)
			
			if(dimencion==len(g)):
				break
			
		return g
		
		
	def comparar(lDic,dic):
		for k in lDic.keys():
			if(len(lDic)>0):
				if(len(lDic[k])==3):
					for l in lDic[k]:
						if(l[2]==dic):
							return (1,l[1])
			
		return (0,0)
		
	def toString(d):
		cad=""
		for k in d.keys():
			cad+=k
			if(k!='_id'):
				for v in d[k]:
					cad+=v
			else:
				cad+=str(d['_id'])
		return cad
		
	def comparar1(lDic,dic,tipo,indCiclo):
		lCadP=[]
		for dat in lDic:
			lCadP.append(dat)
		
		for cad in lCadP:
			if(tipo==0):
				if(cad.split("_id")[0]==toString(dic)):
					print(toString(dic),"---",cad.split("_id")[0])
					indCiclo.append(cad.split("_id")[1])
					return True
			if(tipo==1):
				if(cad.split("_id")[0]==toString(dic).split("_id")[0]):
					print(toString(dic),"---",cad.split("_id")[0])
					indCiclo.append(cad.split("_id")[1])
					return True
				
		return False
		
	def copyDic(d):
		dAux={}
		for k in d.keys():
			if(k!='_id'):
				dAux[k]=d[k].copy()
			else:
				dAux[k]=d["_id"]
		listaNodos.append(dAux)
		
		
	def proceso(gramatica,n):
		global nId
		global dicAdyacencias
		
		#Expansion de gramatica...
		
		#print("---",gramatica)
		#print("----",listaProcesados)

		listaProcesados.append(toString(gramatica))
	
		auxDic={}
		dicEnumerado={}
		listaTransiciones=[]
		
		print("----------------------------------")
		printJson(str(n)+" Entrante",gramatica)
		
		#Se crea un json que agrupa segun las transiciones
		#Clave el elmento por el que se trancisiona
		#valor una lista de produciones involucradas
		for k in gramatica.keys():
		
			if(k!='_id'):
		
				if(vecino(gramatica.get(k)[1])!="reduccion"):
					posK=vecino(gramatica.get(k)[1])
					
					if(posK not in auxDic.keys()):
						auxDic[posK]=[]
						
					gramatica.get(k)[1]=moverPunto(gramatica.get(k)[1])
					auxDic[posK].append(gramatica.get(k))

		
		printJson("Agrupados:",auxDic)
		
		if(len(auxDic.keys())>0):
		
			#Se preparan los grupos como un diccionario independiente que se va a procesar
			#Ha cada trancision se le debe asignar un id nuevo si no fue procesado antes
			#Si fue procesado se debe asignar el id del encontrado
			for k in auxDic.keys():
			
				ciclo = False
				print("Expandido",expandir(auxDic[k]))
				
				dicEnumerado=toJson(auxDic[k])
				
				indCiclo=[]
				auxInd=0
				
				if(comparar1(listaProcesados,dicEnumerado,0,indCiclo)==False):
					nId=nId+1
				else:
					ciclo = True
					auxInd=nId
					nId=int(indCiclo[0])
					print("********* CICLO EN EL",nId)

					
				if(gramatica.get("_id") not in dicAdyacencias.keys()):
					dicAdyacencias[gramatica.get("_id")]=[]
				
				auxIndD=0
				auxIndD=comparar(dicAdyacencias,toString(dicEnumerado))[1]

				if(comparar(dicAdyacencias,toString(dicEnumerado))[0]==0):
					dicAdyacencias[gramatica.get("_id")].append([k,nId,toString(dicEnumerado)])
				else:
					dicAdyacencias[gramatica.get("_id")].append([k,auxIndD,toString(dicEnumerado)])
					
				if(ciclo):
					nId=auxInd
				else:
					#Recolecta las proximas transiciones
					dicEnumerado.setdefault("_id",nId)
					listaTransiciones.append(dicEnumerado)

			
		
			print(n,"proximos:")
			for d in listaTransiciones:
				print(d)
			
			#Recolecta las trancisiones en la lista de nodos
			for transicion in listaTransiciones:
				copyDic(transicion)
				

			for transicion in listaTransiciones:
				#indCiclo=[]
				#auxInd=0
				#if(comparar1(listaProcesados,transicion,1,indCiclo)==False):
				#input()
				print("\n\n")
				proceso(transicion,n+1)
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
			print("Procesados:",listaProcesados)

	
	original={}
	
	for k in gr.keys():
		original[k]=gr[k].copy()
	
	gramatica=recorrerJson(gr)
	
	#el parametro n es para que la gramatica se expanda a partir del nivel 1
	gramatica.setdefault("_id",0)
	print(gramatica)
	
	copyDic(gramatica)
	
	proceso(gramatica,0)
	print("\nProcesados",listaProcesados)
	
	printJson("\nAdyacencia:",dicAdyacencias)
	#Recolectado de nodos clones
	dicRep={}
	for d in listaNodos:
		for d1 in listaNodos:
			if(toString(d).split("_id")[0]==toString(d1).split("_id")[0] and listaNodos.index(d)!=listaNodos.index(d1)):
				print(toString(d).split("_id")[1],toString(d).split("_id")[0])
				print(toString(d1).split("_id")[1],toString(d).split("_id")[0])
				if(toString(d).split("_id")[0] not in dicRep.keys()):
					dicRep[toString(d).split("_id")[0]]=99999
				
				if(int(toString(d).split("_id")[1])<int(dicRep[toString(d).split("_id")[0]])):
					dicRep[toString(d).split("_id")[0]]=toString(d).split("_id")[1]
					break
		
	#Ajuste en las adyacencias
	if(len(dicAdyacencias.keys())>0):
		
		for k in dicAdyacencias:
			for l in dicAdyacencias[k]:
				for k1 in dicRep.keys():
					if(l[2]==k1):
						l[1]=int(dicRep[k1])
						l[2]=""
	
	#print(expandir([['A', '.B()']]))
	#print(expandir([['A', '(.A)'],['A', "( .A' )"]]))
	
	
	#print(punto(" id ").split(" "))
	

	
	printJson("\n-------------Sin clones",dicAdyacencias)
	
	limpiada={}
	
	#Eliminado de huerfanos
	
	
	for k1 in dicAdyacencias:
		conPadre=False
		for k in dicAdyacencias:
			for l in dicAdyacencias[k]:
				if(k1==l[1] or k1==0):
					conPadre=True
			
		if(conPadre):
			limpiada[k1]=dicAdyacencias[k1].copy()
	
	printJson("\n-------------Sin huerfanos",limpiada)
	
	print("\n----------Banco de Nodos")
	
	for d in listaNodos:
		print(d)
	
	
	
	
	
	