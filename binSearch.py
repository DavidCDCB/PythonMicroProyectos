#https://www.youtube.com/watch?v=LqmdoBJwzkw
nTo=10#nuero de discos
from datetime import datetime
import os
import sys
nmov=0
niv=0
buffer=[]
#numero de disco, etiqueta origen, etiqueta auxiliar, etiquta destino, arreglo orige, arreglo auxiliar, arreglo destino
def Hanoi(n,o,a,d,lA,lB,lC,nm):

	#buffer.append(str(nm)+"-Mover "+str(n)+" de "+str(o)+" a "+str(d)+"\n")
	
	if(n==1):
		Mov(o,d)
		#print(str(niv)+"-Mover ",n," de ",o," a ",d)
		
		mArr(len(lA)-1)
		#input()
	else:
		Hanoi(n-1,o,d,a,lA,lC,lB,nm+1)
		#print(str(nm)+"-Mover ",n," de ",o," a ",d)
		Mov(o,d)
		
		mArr(len(lA)-1)
		#input()
		Hanoi(n-1,a,o,d,lB,lA,lC,nm+1)

def Mov(ori,des):#movimiento de dato segun el origen y el final
	if(ori=="A" and des=="C"):
		lC[rArr(lC,0)]=(lA[rArr(lA,0)-1])
		lA[rArr(lA,0)-1]=0
	if(ori=="A" and des=="B"):
		lB[rArr(lB,0)]=(lA[rArr(lA,0)-1])
		lA[rArr(lA,0)-1]=0
	if(ori=="B" and des=="A"):
		lA[rArr(lA,0)]=(lB[rArr(lB,0)-1])
		lB[rArr(lB,0)-1]=0
	if(ori=="B" and des=="C"):
		lC[rArr(lC,0)]=(lB[rArr(lB,0)-1])
		lB[rArr(lB,0)-1]=0
	if(ori=="C" and des=="A"):
		lA[rArr(lA,0)]=(lC[rArr(lC,0)-1])
		lC[rArr(lC,0)-1]=0
	if(ori=="C" and des=="B"):
		lB[rArr(lB,0)]=(lC[rArr(lC,0)-1])
		lC[rArr(lC,0)-1]=0
		
def cArr(size,cer):#Creacion de arreglo con los discos
	if(cer==False):
		dat=size
		arr=[]
		for i in range(size):
			arr.append(dat)
			dat=dat-1
	else:
		arr=[]
		for i in range(size):
			arr.append(0)
	return arr

def disco(may,num):#arreglos con asteriscos
	arr=[]
	text=""
	for i in range(0,num):
		arr.append("*")
	#for i in range(0,may-num):
	#		arr.append(" ")
		
	for i in range(len(arr)):
		text=text+arr[i]
	if(str(len(arr)) != "0"):
		if(len(arr)<10):
			return " "+str(len(arr))
		else:
			return str(len(arr))
	else: return "  "

def mArr(ind):#imprimir arreglos
	limpiar()
	buf=""
	while(ind>=0):
		buf=buf+"\n|"+disco(len(lA),lA[ind])+"|"+disco(len(lA),lB[ind])+"|"+disco(len(lA),lC[ind])+"|"
		ind=ind-1
	print(buf)
		
def rArr(arr,ind):#busqueda numero a desapilar
	if(ind<len(arr) and arr[ind]!=0):
		num=rArr(arr,ind+1)
	else:
		num=ind
	return num

def limpiar():
	if(sys.platform.startswith('linux')):
		os.system("clear")
	else:
		os.system("cls")

#asignacion de arreglos
lA=cArr(nTo,False)
lB=cArr(nTo,True)
lC=cArr(nTo,True)

archivo = open("solucion.txt", "a")

mArr(len(lA)-1)
input("Enter para iniciar")


ini=datetime.now()
Hanoi(nTo,"A","B","C",lA,lB,lC,nmov)
print("Tiempo usado:")
print(datetime.now()-ini)
listToStr = ' '.join([str(elem) for elem in buffer]) 
archivo.write(listToStr)
archivo.close()
input()