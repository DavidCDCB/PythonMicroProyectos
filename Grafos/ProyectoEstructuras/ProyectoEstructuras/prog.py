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
			"Constitución Política de Colombia":[],
			"Lógica Matemática":["Matemáticas Discretas"],
			"Álgebra Lineal":["Investigación de Operaciones"],
			"Cálculo II":["Probabilidad"],
			"Cálculo III":["Matemáticas Especiales"],
			"Cálculo I":["Cálculo II","Cálculo III","Física I"],
			"Matemáticas Discretas":["Circuitos Digitales","Estructuras de Datos"],
			"Matemáticas Especiales":["Análisis y Diseño de Algoritmos","Comunicaciones de Datos"],
			"Matemáticas Fundamentales":["Álgebra Lineal","Cálculo I","Programación II","Ingeniería Económica y Financiera"],
			"Probabilidad":["Matemáticas Especiales","Investigación de Operaciones"],
			"Física II":["Laboratorio Fisica II","Circuitos Digitales"],
			"Laboratorio Fisica I":[],
			"Laboratorio Fisica II":[],
			"Física I":["Física II","Física III","Laboratorio Fisica I"],
			"Física III":[],
			"Biologia Para Ingenieria":["Sistemas Inteligentes II"],
			"Programación II":["Sistemas Operativos","Estructuras de Datos","Programacion III"],
			"Programación Concurrente y Distribuida":["Sistemas Inteligentes I"],
			"Programacion I":["Programación II"],
			"Programacion III":["Seguridad Informática","Programación Concurrente y Distribuida","Redes de Computadores I","Ingeniería de Software I"],
			"Análisis y Diseño de Algoritmos":["Sistemas Inteligentes I"],
			"Autómatas y Lenguajes Formales":["Estructura de Lenguajes"],
			"Estructura de Lenguajes":["Análisis y Diseño de Algoritmos"],
			"Sistemas Inteligentes I":["Sistemas Inteligentes II"],
			"Sistemas Inteligentes II":[],
			"Teoría General de Sistemas":[],
			"Automatización y Control de Procesos":[],
			"Inglés Para Ingeniería":["Investigación Para Ingeniería"],
			"Introducción a la Ingeniería de Sistemas y Computación":[],
			"Investigación Para Ingeniería":["Proyecto Integrador"],
			"Sistemas Operativos":["Programación Concurrente y Distribuida"],
			"Comunicaciones de Datos":["Redes de Computadores III"],
			"Redes de Computadores II":["Redes de Computadores III","Seguridad Informática"],
			"Redes de Computadores III":["Proyecto Integrador"],
			"Redes de Computadores I":["Programación Concurrente y Distribuida","Redes de Computadores II"],
			"Ingeniería de Software II":["Ingeniería de Software III"],
			"Ingeniería de Software III":["Proyecto Integrador"],
			"Ingeniería de Software I":["Investigación Para Ingeniería","Ingeniería de Software II","Administración de Sistemas"],
			"Arquitectura de Computadores":["Microprocesadores"],
			"Circuitos Digitales":["Redes de Computadores I","Arquitectura de Computadores"],
			"Microprocesadores":["Automatización y Control de Procesos"],
			"Auditoría Informática":[],
			"Diseño de Interfaces":["Redes de Computadores III","Programacion III"],
			"Seguridad Informática":[],
			"Proyecto Integrador":["Cruda Realidad"],
			"Administración de Sistemas":["Practica","Auditoría Informática","Gestion de Proyectos","Gestión Tecnológica"],
			"Bases de Datos I":["Ingeniería de Software I","Bases de Datos II"],
			"Bases de Datos II":["Ingeniería de Software III"],
			"Estructuras de Datos":["Autómatas y Lenguajes Formales","Bases de Datos I"],
			"Gestion de Proyectos":["Proyecto Integrador"],
			"Gestión Tecnológica":[],
			"Ingeniería del Conocimiento":[],
			"Habilidades Gerenciales":[],
			"Ingeniería Económica y Financiera":["Investigación de Mercados"],
			"Investigación de Mercados":["Habilidades Gerenciales"],
			"Investigación de Operaciones":["Administración de Sistemas"],
			"Investigación de Mercados":["Habilidades Gerenciales"],
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