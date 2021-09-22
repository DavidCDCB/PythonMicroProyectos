# -*- coding: latin-1 -*-
#https://medium.com/@pacoavila_34646/unicode-en-python-1551c9b93c97

from PIL import ImageTk, Image
from graphviz import Digraph
import tkinter,sys
from tkinter.ttk import *
from tkinter import filedialog,messagebox
from tkinter import *
import tkinter as tk
import os

from Generador import Generador


'''
gramatica={"0": ["F","(E)"],
"1": ["E","R+T"],
"2": ["R","id OKF"],
"3": ["OK","lambda"],
"_id":2
}
'''

prueba='''E->E+T
E->T
T->T*F
T->F
F->(E)
F-> id
'''



prueba='''E->E+T
T->T*F|F
F->(E)| id +
'''

prueba='''A'->A
A->(B)
B->a
'''



prueba='''E->E+T
T->T*F|F
F->(E)| id| H B
H->m
B->r| lambda
'''

print("C:\\Users\\win8>nslookup ejercicioredes.com\nServidor:  ns.dns0.com\nAdress:  107.162.26.2\n\nNombre:  ejercicioredes.com\nAdress:  107.162.26.3")


class Ventana:
	def __init__(self):

		self.g = Digraph('G', filename='grafo', format='png')

		listaNodos={
			"Constituci�n Pol�tica de Colombia":[],
			"L�gica Matem�tica":["Matem�ticas Discretas"],
			"�lgebra Lineal":["Investigaci�n de Operaciones"],
			"C�lculo II":["Probabilidad"],
			"C�lculo III":["Matem�ticas Especiales"],
			"C�lculo I":["C�lculo II","C�lculo III","F�sica I"],
			"Matem�ticas Discretas":["Circuitos Digitales","Estructuras de Datos"],
			"Matem�ticas Especiales":["An�lisis y Dise�o de Algoritmos","Comunicaciones de Datos"],
			"Matem�ticas Fundamentales":["�lgebra Lineal","C�lculo I","Programaci�n II","Ingenier�a Econ�mica y Financiera"],
			"Probabilidad":["Matem�ticas Especiales","Investigaci�n de Operaciones"],
			"F�sica II":["Laboratorio Fisica II","Circuitos Digitales"],
			"Laboratorio Fisica I":[],
			"Laboratorio Fisica II":[],
			"F�sica I":["F�sica II","F�sica III","Laboratorio Fisica I"],
			"F�sica III":[],
			"Biologia Para Ingenieria":["Sistemas Inteligentes II"],
			"Programaci�n II":["Sistemas Operativos","Estructuras de Datos","Programacion III"],
			"Programaci�n Concurrente y Distribuida":["Sistemas Inteligentes I"],
			"Programacion I":["Programaci�n II"],
			"Programacion III":["Seguridad Inform�tica","Programaci�n Concurrente y Distribuida","Redes de Computadores I","Ingenier�a de Software I"],
			"An�lisis y Dise�o de Algoritmos":["Sistemas Inteligentes I"],
			"Aut�matas y Lenguajes Formales":["Estructura de Lenguajes"],
			"Estructura de Lenguajes":["An�lisis y Dise�o de Algoritmos"],
			"Sistemas Inteligentes I":["Sistemas Inteligentes II"],
			"Sistemas Inteligentes II":[],
			"Teor�a General de Sistemas":[],
			"Automatizaci�n y Control de Procesos":[],
			"Ingl�s Para Ingenier�a":["Investigaci�n Para Ingenier�a"],
			"Introducci�n a la Ingenier�a de Sistemas y Computaci�n":[],
			"Investigaci�n Para Ingenier�a":["Proyecto Integrador"],
			"Sistemas Operativos":["Programaci�n Concurrente y Distribuida"],
			"Comunicaciones de Datos":["Redes de Computadores III"],
			"Redes de Computadores II":["Redes de Computadores III","Seguridad Inform�tica"],
			"Redes de Computadores III":["Proyecto Integrador"],
			"Redes de Computadores I":["Programaci�n Concurrente y Distribuida","Redes de Computadores II"],
			"Ingenier�a de Software II":["Ingenier�a de Software III"],
			"Ingenier�a de Software III":["Proyecto Integrador"],
			"Ingenier�a de Software I":["Investigaci�n Para Ingenier�a","Ingenier�a de Software II","Administraci�n de Sistemas"],
			"Arquitectura de Computadores":["Microprocesadores"],
			"Circuitos Digitales":["Redes de Computadores I","Arquitectura de Computadores"],
			"Microprocesadores":["Automatizaci�n y Control de Procesos"],
			"Auditor�a Inform�tica":[],
			"Dise�o de Interfaces":["Redes de Computadores III","Programacion III"],
			"Seguridad Inform�tica":[],
			"Proyecto Integrador":["Cruda Realidad"],
			"Administraci�n de Sistemas":["Practica","Auditor�a Inform�tica","Gestion de Proyectos","Gesti�n Tecnol�gica"],
			"Bases de Datos I":["Ingenier�a de Software I","Bases de Datos II"],
			"Bases de Datos II":["Ingenier�a de Software III"],
			"Estructuras de Datos":["Aut�matas y Lenguajes Formales","Bases de Datos I"],
			"Gestion de Proyectos":["Proyecto Integrador"],
			"Gesti�n Tecnol�gica":[],
			"Ingenier�a del Conocimiento":[],
			"Habilidades Gerenciales":[],
			"Ingenier�a Econ�mica y Financiera":["Investigaci�n de Mercados"],
			"Investigaci�n de Mercados":["Habilidades Gerenciales"],
			"Investigaci�n de Operaciones":["Administraci�n de Sistemas"],
			"Investigaci�n de Mercados":["Habilidades Gerenciales"],
			"Practica":["Cruda Realidad"],
			"Cruda Realidad":[]
		}
		self.construye_grafo(listaNodos)

	def construye_grafo(self,listaNodos):
		self.g.attr(rankdir='LR', size='50')
		self.g.attr('node', shape='box3d')
		self.g.attr(bgcolor='black',fontcolor='white')
		
		# Se crean los nodos---------------------------------
		print("Nodos a crear\n\n")
		for k in listaNodos.keys():
			self.g.node(str(k), label=str(k), color='black',fontcolor='black',fillcolor='white',style='filled')


		# Se crean las adyacencias---------------------
		for key, item in listaNodos.items():
			for dat in item:
				self.g.edge(str(key), str(dat), label="" ,color='green')

		#Crea el png del grafo------------------------
		self.g.view()


	#Se edita luego, crea el diccionario para el procesamiento, cambie aqui las variables que necesite
	def obtieneDiccionario(self,t):
		gr={}
		entrada=t.get('0.1',END)
		for linea in entrada.split("\n"):
			if(len(linea.split("->"))>1):
				gr[str(entrada.split("\n").index(linea))]=[linea.split("->")[0],linea.split("->")[1]]
		
		return gr
		
	def extender(self,t):
		#entrada=t
		entrada=t.get('0.1',END)
		divididos=[]
		cad=""
		
		if(len(entrada.split("\n")[0].split("->")[1])>1):
			primero=entrada.split("\n")[0].split("->")[0]
			cad=cad+"S->"+primero+"\n"
		
		for linea in entrada.split("\n"):
			for prod in linea.split("->"):
				if(len(linea.split("->"))==2):
					if(linea.split("->").index(prod)==0 and "|" not in linea.split("->")[1]):
						cad=cad+linea.split("->")[0]+"->"+linea.split("->")[1]+"\n"
					else:
						if("|" in prod):
							for prod1 in prod.split("|"):
								cad=cad+linea.split("->")[0]+"->"+prod1+"\n"
							
		print(cad)
		return cad
		
		
	def obtieneDiccionarioP(self,entrada):
		gr={}
		for linea in entrada.split("\n"):
			if(len(linea.split("->"))>1):
				gr[str(entrada.split("\n").index(linea))]=[linea.split("->")[0],linea.split("->")[1]]
		
		return gr


v=Ventana()