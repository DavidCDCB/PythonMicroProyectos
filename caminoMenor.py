import random,time

class Camino:
	
	def __init__(self,matriz):
		self.matriz = matriz
		self.var_x = [0, 0, +1, -1]
		self.var_y = [+1, -1, 0, 0]
		self.ancho = len(self.matriz[0])
		self.alto = len(self.matriz)
		
	def verM(self,m):
		print("-------")
		for i in range(len(m)):
			cad=""
			for j in range(len(m)):
				if(m[i][j]!=0):
					cad+="|"+str(m[i][j])
				else: cad+="| "
			print(cad)

	def busca_camino(self, inicio,fin):
		x = inicio[0]
		y = inicio[1]
		
		if not 0 <= x < self.ancho and not 0 <= y < self.alto :
			print("Valor erroneo")
		if self.matriz[x][y] is not 0 :
			print("La posicion no puede estar en un obstaculo")
		
		lista = [inicio]
		self.matriz[x][y] = 2
		return self.rellena_anchura(inicio,fin,lista,[])
	
	def rellena_anchura(self, inicio,fin,lista, aux, cont=3):
		x=inicio[0]
		y=inicio[1]
		xF=fin[0]
		yF=fin[1]
		vecinos = []
		
		# Busca los vecinos de la posicion
		for i in range(0, 4, 1):
			xN = x + self.var_x[i]
			yN = y + self.var_y[i]
			if 0 <= xN < self.ancho and 0 <= yN < self.alto:
				if self.matriz[xN][yN] is 0 or self.matriz[xN][yN] > cont:
					if (xN,yN) == fin:
						lista=aux.copy()
						lista.append((xN,yN))
						print(str(lista))
					vecinos.append((xN, yN))
		
		# Asigna el valor de los vecinos a la matriz
		for vecino in vecinos:

			self.matriz[vecino[0]][vecino[1]] = cont
			
		
		# Imprime cada marcado de vecinos(Para pruebas, borrar)
		#for m in self.matriz:
		#	print(*m, sep=" ")
		#print("")
		
		
		# Hace el recorrido recursivamente
		for vecino in vecinos:
			time.sleep(0.1)
			self.verM(self.matriz)
			aux.append(vecino)
			lista=self.rellena_anchura(vecino,fin,lista, aux, cont + 1)
			aux.pop()
			
		return lista

# Pruebas
""""
m1 = [[0] * 20 for i in range(20)]#matriz de pesos


for i  in range(40):
	f=random.randint(0,len(m1)-1)
	c=random.randint(0,len(m1)-1)
	if(m1[f][c]==0):
		m1[f][c]=1

camino = Camino(m1)
inicio=(0, 18)
fin=(18,0)
lista=camino.busca_camino(inicio, fin)

print("el camino mas corto de "+str(inicio)+" a "+str(fin)+" es")

# ▲ es pared,✪ es el camino y ■ es un espacio vacio


for i in range(0,len(camino.matriz),1):
	print(i, end='')
	for j in range(0,len(camino.matriz[0]),1):
		if camino.matriz[i][j] is 1:
			print("▲", end='')
		elif (i,j) in lista:
			print("✪", end='')
		else:
			print("■", end='')
		
	print("")

"""


		
def back(f,c,fd,cd,m,coo,mcoo,fi,ci):
	m[fd][cd]=5
	
	if(len(mcoo)==0): 
	
		#print(mcoo)

		#time.sleep(0.01)
		#verM(m)
		
		if(f>len(m)-1 or f<0):
			return mcoo
		
		if(c>len(m)-1 or c<0):
			return mcoo
		
		if(m[f][c] is 2 or m[f][c] is 3 or m[f][c] is 1):
			return mcoo
		
		coo.append((f,c))
		
		if(m[f][c] is 5):
			#limpiado de intentos fallidos
			for i in range(len(m)):
				for j in range(len(m)):
					if(m[i][j] is 1):m[i][j]=0
					
			#si la opcion encontrada es mas optima que la actual
			if(len(mcoo)==0 or len(coo)<len(mcoo)):
				mcoo=coo.copy()
				
			print("!!!!")
			return mcoo
			
		m[f][c]=2
		
		if(fd>=fi and cd>=ci):#abajo derecha
			mcoo=back(f+1,c+0,fd,cd,m,coo,mcoo,fi,ci);
			mcoo=back(f+0,c+1,fd,cd,m,coo,mcoo,fi,ci);

			
		if(fd>=fi and cd<=ci):#abajo izquierda
			mcoo=back(f+1,c+0,fd,cd,m,coo,mcoo,fi,ci);
			mcoo=back(f+0,c-1,fd,cd,m,coo,mcoo,fi,ci);

		if(fd<=fi and cd>=ci):#arriba derecha
			mcoo=back(f+-1,c+0,fd,cd,m,coo,mcoo,fi,ci);
			mcoo=back(f+0,c+1,fd,cd,m,coo,mcoo,fi,ci);

		
		if(fd<=fi and cd<=ci):#arriba izquierda
			mcoo=back(f+-1,c+0,fd,cd,m,coo,mcoo,fi,ci);
			mcoo=back(f+0,c+-1,fd,cd,m,coo,mcoo,fi,ci);

		
		coo.pop(-1)
		m[f][c]=1
	
	return mcoo 

#se adapta segun la coordenada inicio y destino
lc=[[(2,2),(10,10)],
	[(18,18),(12,2)],
	[(2,18),(10,2)],
	[(18,2),(12,10)]]

def verM(m):
	print("-------")
	for i in range(len(m)):
		cad=""
		for j in range(len(m)):
			if(m[i][j]!=0):
				cad+="|"+str(m[i][j])
			else: cad+="| "
		print(cad)



for i in range(4):
	
	cooI=lc[i][0]
	cooF=lc[i][1]
	
	m1=[[0] * 20 for i in range(20)]#matriz de pesos
	mcoo=[]
	
	
	#llenado de obstaculos
	for i  in range(40):
		f=random.randint(0,len(m1)-1)
		c=random.randint(0,len(m1)-1)
		if(m1[f][c]==0):
			m1[f][c]=3

	
	#coordenadas de inicio, matriz,lista de posibles caminos, futuro camino menor,coordenadas de inicio(ORIGINALES)
	coo=back(cooI[0],cooI[1],cooF[0],cooF[1],m1,[],mcoo,cooI[0],cooI[1])

	#asignacion de coordenada resultantes
	if(len(coo)==0):break
	for i,j  in coo:
		m1[i][j]=2
		
	#limpiado de intentos fallidos
	for i in range(len(m1)):
		for j in range(len(m1)):
			if(m1[i][j] is 1):m1[i][j]=0
			if(m1[i][j] is 0):m1[i][j]=" "
	verM(m1)
	#time.sleep(3)

