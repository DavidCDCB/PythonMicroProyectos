
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


class Ventana:
	def __init__(self):

		self.g = Digraph('G', filename='grafo', format='png')

		#pruebas
		#gr=self.obtieneDiccionarioP(self.extender(prueba))
		#obj = Generador(gr,'lr1')
		#obj.tabla()
		#os.system("start notepad.exe solucion.txt")
		
		#Metodos de los botones----------
		def A():
			gr=self.obtieneDiccionarioP(self.extender(t))
			obj = Generador(gr,'lr0')
			self.g = Digraph('G', filename='grafo', format='png')
			self.construye_grafo(obj)
			obj.tabla()
			#os.system("start notepad.exe solucion.txt")
			
		def B():
			gr=self.obtieneDiccionarioP(self.extender(t))
			obj = Generador(gr,'lr1')
			self.g = Digraph('G', filename='grafo', format='png')
			self.construye_grafo(obj)
		
		
		self.alto=400
		self.ancho=500
		self.ventana = tk.Tk()
		self.ventana.geometry(str(self.ancho) + "x" + str(self.alto))
		self.ventana.title("Proyecto Final Lenguajes")
		
		#Construccion del frame A---------------
		self.frameA = tk.Frame(self.ventana, bg="black", width=self.ancho, height=self.alto)
		self.frameA.grid(row=0, column=0, sticky="NW")
		self.frameA.grid_propagate(0)
		self.frameA.update()
			
		#Botones---------------------
		self.buttonA = tk.Button(self.frameA, text="LRO", command=A).grid(row=1, column=0,sticky="W")
		self.buttonB = tk.Button(self.frameA, text="LR1", command=B).grid(row=1, column=0,sticky="W", padx=100)

		t=tk.Text(self.frameA,height=self.alto,width=50,font=('Consolas', 22,'bold'))
		t.insert(tk.END, prueba)

		s =tk.Scrollbar(self.frameA,orient=tk.VERTICAL, command=t.yview)
		s.grid(column=0,row=4,sticky="EN")
		t['yscrollcommand'] = s.set

		Sizegrip(self.frameA).grid(column=0, row=4, sticky=(S,E))

		t.config(yscrollcommand=s.set)
		t.grid(column=0,row=2)
		
		self.ventana.mainloop()
		

	def construye_grafo(self,obj):

		self.g.attr(rankdir='LR', size='16')
		self.g.attr('node', shape='box3d')
		self.g.attr(bgcolor='white',fontcolor='white')
		

		# Se crean los nodos---------------------------------
		print("Nodos a crear\n\n")
		for d in obj.listaNodos:
			datos_nodo = ""
			id_nodo = ""

			R=obj.buscarR(d["0"][0],d["0"][1])
			for key, item in d.items():
				
			
				if key != "_id":
					if(len(item)==2):
						datos_nodo = datos_nodo + item[0] + "=>" + item[1] + "\n"
					else:
						datos_nodo = datos_nodo + item[0] + "=>" + item[1] +" "+ item[2]+"\n"
				else:
					id_nodo = item

			datos_nodo = "I" + str(obj.listaNodos.index(d)) +R+ "\n" + datos_nodo

			if("R" in datos_nodo):
				self.g.node(str(id_nodo), label=datos_nodo, color='black',fontcolor='black',fillcolor='cyan',style='filled')
			else:
				self.g.node(str(id_nodo), label=datos_nodo, color='black',fontcolor='black',fillcolor='peru',style='filled')

		# Se crean las adyacencias---------------------
		for key, item in obj.limpiada.items():
			for lista in item:
				self.g.edge(str(key), str(lista[1]), label=lista[0] ,color='blue')

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

'''
E->E+T
E->T
T->T*F
T->F
F->(E)
F-> id

gr={
	"0":["E","E+T"],
	"1":["E","T"],
	"2":["T","T*F"], 
	"3":["T","F"],
	"4":["F","(E)"],
	"5":["F"," id"]
}
'''

v=Ventana()