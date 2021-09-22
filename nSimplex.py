from fractions import Fraction
import decimal
import os

#maxi o mini
tipo="maxi"


nCol=[]
nFil=[]
matriz=[]
		
def main():
	global matriz
	global tipo
	global nFil
	global nCol
	indfPivote=0
	indcImplicada=0
	nTabla=1
	fPivote=[]
	
	getData()
	print(nFil)
	print(nCol)
	print(matriz)
	
	open("solucion.txt","w").close()
	archivoW = open("solucion.txt","a")
	archivoW.write("Matriz Original:\n")
	verM(matriz,archivoW)

	while(verificar(matriz)):
		nl=[]
		for dat in matriz[0]:
			#verifica que el mayor no sea un cero y no cuente con el ultimo
			if(dat>0 and matriz[0].index(dat)<=len(matriz[0])-2 and tipo=="mini"):
				nl.append(dat)
				
			if(matriz[0].index(dat)<=len(matriz[0])-2 and tipo=="maxi"):
				nl.append(dat)
				
		#Retorna el indice(columna) del elemento menor de la fila de la funcion objetivo
		#Retorna el indice(columna) del elemento mayor cuando es minimizacion
		if(tipo=="mini"):
			indcImplicada=matriz[0].index(max(nl))
		else:
			indcImplicada=matriz[0].index(min(nl))
		
		#Por medio de las divisiones saca el indice(fila) de la fila pivote
		ld=getDivisiones(matriz,indcImplicada)
		indfPivote=ld.index(min(ld))+1

		#Saca la fila pivote modificada por la division del elemnto menor de la funcion objetivo
		#Como parametros el dato intercccion y la fila pivote original
		fPivote=getfPivote(matriz[indfPivote][indcImplicada],matriz[indfPivote])
		
		archivoW.write("Tabla #"+str(nTabla)+"\n")
		archivoW.write("Entrante: "+nCol[indcImplicada+1]+"\n")
		archivoW.write("Saliente: "+nFil[indfPivote]+"\n")
		archivoW.write("Fila pivote:"+str(matriz[indfPivote])+"\n")
		archivoW.write("Fila pivote dividida por: "+str(matriz[indfPivote][indcImplicada])+"\n\n")
		
		#Asigna la variable entrante como saliente
		nFil[indfPivote]=nCol[indcImplicada+1]
		
		#Inicia el proceso de modificacion de la matriz
		matriz=proceso(matriz,indfPivote,indcImplicada,fPivote,archivoW).copy()
		#Por cada iteracion muestra la matriz
		verM(matriz,archivoW)
		verM2(matriz,archivoW)
		nTabla=nTabla+1
		
	archivoW.close()
	os.system("start /MAX notepad.exe solucion.txt")
		
#Se obtienen los datos que se compiaron de un excel al archivos datos.txt
def getData():
	global matriz
	global nCol
	global nFil
	archivoR = open("datos.txt","r")
	matriz=[]
	data=archivoR.readlines()
	
	for dat in data:
		print(dat)
		fila=[]
		if(data.index(dat)==0):
			nCol=dat.split("\n")[0].split("	")
		else:
			for dat1 in dat.split("	"):
				if(dat.split("	").index(dat1)==0):
					nFil.append(dat1) 
				else:
					if("," in dat1):
						dat1=dat1.split(",")[0]+"."+dat1.split(",")[1]
						fila.append(float(dat1))
					else:
						fila.append(int(dat1))
			matriz.append(fila)
	
	archivoR.close()
		
#Verifica si en la fila de la funcion objetivo hay negativos 
def verificar(m):
	for i in range(0,len(m[0])):
		if(m[0][i]<0 and tipo=="maxi"):
			return True
		if(m[0][i]>=0 and tipo=="mini"):
			return True
	return False
		
#Saca los cocientes para elegir la fila pivote (asigna un numero grande cuando no hay restriccion)
def getDivisiones(m,cIm):
	lr=[]
	for i in range(0,len(m)):
		if(i>0):
			if(m[i][cIm]>0):
				lr.append(m[i][len(m[0])-1]/m[i][cIm])
			else:
				lr.append(999999)
	return lr
	
#Retorna la fila pivote modificada
def getfPivote(valPiv,fpiv):
	lr=[]
	for dat in fpiv:
		if(valPiv>0):
			lr.append(round(dat/valPiv,4))
		else:
			lr.append(10000000)
	return lr
	
#Crea una copia de la matriz original y va iterando para cambiar los datos
def proceso(m,indfPivote,indcImplicada,fPivote,file):
	aM=m.copy()
	valorImp=0
	auxList=[]
	
	for i in range(0,len(m)):
		if(i!=indfPivote):
			auxList=aM[i].copy()
			
			valorImp=m[i][indcImplicada]
			file.write("	"+str(valorImp*-1)+"("+nFil[i]+","+str(nCol[indcImplicada+1])+")"+" Multiplicado por: ")
			file.write(nFil[indfPivote]+", Se le suma: "+nFil[i]+"\n")
			for j in range(0,len(m[0])):
				aM[i][j]=round((-1*valorImp*fPivote[j])+auxList[j],4)
				#file.write("		"+"-1*("+str(valorImp)+"*"+str(fPivote[j])+")"+"+"+str(auxList[j])+"="+str(aM[i][j])+"\n")
		else:
			for j in range(0,len(m[0])):
				aM[i][j]=fPivote[j]
	return aM
		
#Ajusta el ancho de cada celda
def ft(string,esp):
	espacios=esp-len(string)
	for i in range(espacios):
		string=string+" "
	return string+"| "
		
#Visualizar la matriz si hay numero decimales los representa como fraccion
def verM(m,f):
	buffer=""
	for dat in nCol:
		if(nCol.index(dat)==0):
			buffer=buffer+"   | "
		else:
			buffer=buffer+ft(dat,8)
	buffer=buffer+"\n"
	for i in range(0,len(m)):
		buffer=buffer+nFil[i]+" "
		buffer=buffer+"| "
		for j in range(0,len(m[0])):
			if("." in str(str(m[i][j]))):
				buffer=buffer+ft(str(round(m[i][j],4)),8)
			else:
				buffer=buffer+ft(str(m[i][j]),8)
		buffer=buffer+"\n"
	f.write(buffer+"\n")
		
def verM2(m,f):
	buffer=""
	buffer=buffer+"\n"
	for i in range(0,len(m)):
		buffer=buffer+nFil[i]+"	"
		buffer=buffer
		for j in range(0,len(m[0])):
			if("." in str(str(m[i][j]))):
				buffer=buffer+str(round(m[i][j],4)).split(".")[0]+","+str(round(m[i][j],4)).split(".")[1]+"	"
			else:
				buffer=buffer+str(m[i][j])+"	"
		buffer=buffer+"\n"
	f.write(buffer+"\n")

if __name__ == "__main__":
	main()
