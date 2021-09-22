#https://sites.google.com/site/programacioniiuno/temario/unidad-5---grafos/rboles
#https://sites.google.com/site/programacioniiuno/temario/unidad-5---grafos/rboles-binarios

import pygame
from tkinter import *
from pygame.locals import *
import sys
import time
listaN=[]
pygame.font.init()
fuente = pygame.font.Font(None, 30)

class ArbolBinario:
	def __init__( self, esMenorFunction = lambda x,y: x < y ):
		self.raiz = None
		self.esMenor = esMenorFunction

	def getR(self):
		return self.raiz
	def setR(self,r):
		self.raiz=r
	def getCo(self):
		return self.esMenor
	def setCo(self,dat):
		self.esMenor=dat

class NodoBinario:
	def __init__( self, elemento,padre):
		self.elemento = elemento
		self.izquierda = None
		self.derecha = None
		self.padre = padre

	def getD(self):
		return self.derecha
	def setD(self,d):
		self.derecha=d

	def getI(self):
		return self.izquierda
	def setI(self,i):
		self.izquierda=i

	def getE(self):
		return self.elemento
	def setE(self,dat):
		self.elemento=dat

	def getP(self):
		return self.padre
	def setP(self,dat):
		self.padre=dat

def profundidad(arbol):
	return profundidadDeNodo(arbol.getR())

def profundidadDeNodo(nodo):
	if nodo == None:
		return 0
	return 1 + max([profundidadDeNodo(nodo.izquierda), profundidadDeNodo(nodo.derecha) ])

def agregarElementoB(arbol, elemento):
	if (arbol.getR() == None):
		arbol.setR(NodoBinario(elemento, None))
	else:
		subAgregarElementoEnNodo(arbol.getR(), elemento, arbol.getCo())

def subAgregarElementoEnNodo(nodo, elemento, funcionEsMenor):
	if (funcionEsMenor(elemento, nodo.elemento)):
		agregarIzquierda(nodo, elemento, funcionEsMenor)
	else:
		agregarDerecha(nodo, elemento, funcionEsMenor)

def agregarIzquierda(nodo, elemento, funcionEsMenor):
	if (nodo.getI() == None):
		nodo.setI(NodoBinario(elemento, nodo))
	else:
		subAgregarElementoEnNodo(nodo.getI(), elemento,funcionEsMenor)

def agregarDerecha(nodo, elemento, funcionEsMenor):
	if (nodo.getD() == None):
		nodo.setD(NodoBinario(elemento, nodo))
	else:
		subAgregarElementoEnNodo(nodo.getD(), elemento,funcionEsMenor)
#-----------------------------------------------------------
def ejecutarPreOrden(arbol, funcion):
	subEjecutarPreOrden(arbol.getR(), funcion)

def subEjecutarPreOrden(nodo, funcion):
	if (nodo != None):
		funcion(nodo.getE())
		subEjecutarPreOrden(nodo.getI(), funcion)
		subEjecutarPreOrden(nodo.getD(), funcion)

def ejecutarInOrden(arbol, funcion):
	subEjecutarInOrden(arbol.getR(), funcion)

def subEjecutarInOrden(nodo, funcion):
	if (nodo != None):
		
		subEjecutarInOrden(nodo.getI(), funcion)
		funcion(nodo.getE())
		subEjecutarInOrden(nodo.getD(), funcion)

def ejecutarPostOrden(arbol, funcion):
	subEjecutarPostOrden(arbol.getR(), funcion)

def subEjecutarPostOrden(nodo, funcion):
	if (nodo != None):
		subEjecutarPostOrden(nodo.getI(), funcion)
		subEjecutarPostOrden(nodo.getD(), funcion)
		funcion(nodo.getE())
#----------------------------------------------------------
def eliminar(arbol, element):
	eliminarNodo(arbol, buscarNodo(arbol.raiz, element, arbol.esMenor))

def eliminarNodo(arbol, nodo):
	if not tieneHijos(nodo):
		eliminarSinHijos(arbol, nodo)
	elif tieneAmbosHijos(nodo):
		eliminarConAmbosHijos(arbol, nodo)
	elif tieneHijoDerecho(nodo):
		eliminarCon1Hijo(arbol, nodo, nodo.derecha)
	else:
		eliminarCon1Hijo(arbol, nodo, nodo.izquierda)


def tieneHijoDerecho(nodo): return nodo.derecha != None
def tieneHijoIzquierdo(nodo): return nodo.izquierda != None
def tieneHijos(nodo): return tieneHijoDerecho(nodo) or tieneHijoIzquierdo(nodo)
def tieneAmbosHijos(nodo): return tieneHijoDerecho(nodo) and tieneHijoIzquierdo(nodo)
def esHijoIzquierdo(nodo): return nodo.padre.izquierda == nodo
def esRaiz(nodo): return nodo.padre == None

def eliminarSinHijos(arbol, nodo):
	if esRaiz(nodo):
		arbol.raiz = None
	elif esHijoIzquierdo(nodo):
		nodo.padre.izquierda = None
	else:
		nodo.padre.derecha = None


def eliminarCon1Hijo(arbol, nodo, hijo):
	if esRaiz(nodo):
		arbol.raiz = hijo
		arbol.raiz.padre = None
	elif esHijoIzquierdo(nodo):
		nodo.padre.izquierda = hijo
		hijo.padre = nodo.padre
	else:
		nodo.padre.derecha = hijo
		hijo.padre = nodo.padre

def eliminarConAmbosHijos(arbol, nodo):
	menorHijoRamaDerecha = buscarNodoMenorValor(nodo.derecha)
	eliminarNodo(arbol, menorHijoRamaDerecha)
	nodo.elemento = menorHijoRamaDerecha.elemento

def buscarNodoMenorValor(nodo):
	return nodo if nodo.izquierda == None else buscarNodoMenorValor(nodo.izquierda)

def buscarNodo(nodo, elemento, funcionEsMenor):
	if nodo.elemento == elemento:
		return nodo
	elif funcionEsMenor(elemento, nodo.elemento):
		return buscarNodo(nodo.izquierda, elemento, funcionEsMenor)
	else:
		return buscarNodo(nodo.derecha, elemento, funcionEsMenor)
#
# Existe
#

def existe(arbol, elemento):
	return existeEnNodo(arbol.raiz, elemento, arbol.esMenor)

def existeEnNodo(nodo, elemento, esMenor):
	if nodo == None:
		return False
	elif nodo.elemento == elemento:
		return True
	elif esMenor(elemento, nodo.elemento):
		return existeEnNodo(nodo.izquierda, elemento, esMenor)
	else:
		return existeEnNodo(nodo.derecha, elemento, esMenor)


class Arbol:
	def __init__(self, elemento):
		self.coor=(0,0)
		self.hijos = []
		self.elemento = elemento
		self.padre=None

	def setElem(self,dat):
		self.elemento=dat
	def getElem(self):
		return self.elemento

	def getH(self):
		return self.hijos
	def setH(self,dat):
		return self.hijos.append(dat)

	def getCo(self):
		return self.coor
	def setCo(self,dat):
		self.coor=dat

	def getP(self):
		return self.padre
	def setP(self,dat):
		self.padre=dat

def verA(a,n):
	print(a.getElem())
	for h in a.getH():
		verA(h,n)

def verH(a):
	for h in a.getH():
		print(h.getElem())
def recN(a,n):
	verH(a)
	for h in a.getH():
		recA(h,n)

def recA(a,n):
	listaN.append(a)
	for h in a.getH():
		recA(h,n)

def agregarElemento(arbol, elemento, elementoPadre):
	print("-->",elemento)
	subarbol = buscarSubarbol(arbol, elementoPadre,0);
	nA=Arbol(elemento)
	nA.setP(subarbol)
	subarbol.setH(nA)

def buscarSubarbol(arbol, elemento,niv):
	if arbol.getElem() == elemento:
		print("--",arbol.getElem(),"-",niv)
		return arbol
	for subarbol in arbol.getH():
		print(subarbol.getElem(),"-",niv)
		arbolBuscado = buscarSubarbol(subarbol, elemento,niv+1)
		if (arbolBuscado != None):
			return arbolBuscado
	return None


def colicion(obj1,obj2):
	return obj1.colliderect(obj2)

def gameLoop(arbol):

	gameExit = False
	clock = pygame.time.Clock()
	superficie=pygame.display.set_mode((600,600))#Crea el fondo
	pygame.display.set_caption('Arbol PyGame')
	superficie.fill((250,250,250))#color del fondo RGB

	def vPos(dat):
		est=True
		for i in range(len(listaC)):
			if(listaC[i]==dat):
				est=False
				break
		return est


	while not gameExit:
		clock.tick(60)
		superficie.fill((250,250,250))
		esp=80
		listaC=[]

		for i in range(len(listaN)):
			if(i==0):
				listaN[i].setCo((300,50))
				listaC.append((300,50))
			else:
				#print "--->", listaN[i].getElem()
				nPos=((listaN[i].getP().getCo()[0]-esp),(listaN[i].getP().getCo()[1]+esp))
				#print nPos
				if(vPos(nPos)==True):
					listaN[i].setCo(nPos)
					listaC.append(nPos)
					continue

				nPos=((listaN[i].getP().getCo()[0]+esp),(listaN[i].getP().getCo()[1]+esp))
				if(vPos(nPos)==True):
					listaN[i].setCo(nPos)
					listaC.append(nPos)
					continue

				nPos=((listaN[i].getP().getCo()[0]+esp),(listaN[i].getP().getCo()[1]-esp))
				if(vPos(nPos)==True):
					listaN[i].setCo(nPos)
					listaC.append(nPos)
					continue

				nPos=((listaN[i].getP().getCo()[0]-esp),(listaN[i].getP().getCo()[1]-esp))
				if(vPos(nPos)==True):
					listaN[i].setCo(nPos)
					listaC.append(nPos)
					continue

		for i in range(len(listaN)):
			for x in range(len(listaN[i].getH())):
				pygame.draw.line(superficie, (0, 0, 0), listaN[i].getCo(), listaN[i].getH()[x].getCo(), 3)
		for i in range(len(listaN)):
			if(i==0):
				pygame.draw.circle(superficie, (255,0,0), listaN[i].getCo(), 20)
				superficie.blit(fuente.render(listaN[i].getElem(),True, (0, 0, 0)),(listaN[i].getCo()[0]-10,listaN[i].getCo()[1]-10))
			else:
				pygame.draw.circle(superficie, (0,255,0), listaN[i].getCo(), 20)
				superficie.blit(fuente.render(listaN[i].getElem(),True, (0, 0, 0)),(listaN[i].getCo()[0]-10,listaN[i].getCo()[1]-10))


		for event in pygame.event.get():
			if(event.type==pygame.QUIT):
				gameExit=True

		pygame.display.update()

	pygame.quit()

arbol = Arbol("A")
agregarElemento(arbol, "B", "A")
agregarElemento(arbol, "C", "B")
agregarElemento(arbol, "D", "A")
recA(arbol,0)

def esMenorFunction(x,y):
	return x<y
def imprimir(elemento):
	#listaN.append(elemento)
	print (elemento)

arbolB=ArbolBinario(esMenorFunction)
agregarElementoB(arbolB,5)
agregarElementoB(arbolB,3)
agregarElementoB(arbolB,6)
agregarElementoB(arbolB,4)
agregarElementoB(arbolB,7)

def rotI(a):
	q=a.getD()
	aux=q.getI()
	q.setI(a)
	a.setD(aux)
	return q

#arbolB.setR(rotI(arbolB.getR()))
#ejecutarPreOrden(arbolB, imprimir)

gameLoop(arbol)
#verA(arbol,0)
