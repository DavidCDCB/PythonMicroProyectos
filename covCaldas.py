import requests
import json
import os
from datetime import datetime
from datetime import date
#from matplotlib import pyplot
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

source = 'https://www.datos.gov.co/resource/gt2j-8ykr.json?$limit=100000&departamento_nom=CALDAS'
new_source = 'https://www.datos.gov.co/resource/gt2j-8ykr.json?$limit=100000&recuperado=Activo&departamento_nom=CALDAS&$where=fecha_recuperado IS NULL AND fecha_muerte IS NULL'
sourceDb ='https://datacovidcaldas.firebaseio.com/muestras.json'


def getInfo2(url):
	r = requests.get(url)
	return r.json()

def gHistorial(fechas,muestras,size_text):
	nMuestras=[]
	size=size_text
	
	for m in muestras:
		if(m!="\n" and m!=""):
			nMuestras.append(int(m))
			
	with plt.style.context('dark_background'):
			
		plt.plot(fechas,nMuestras,color='red',marker='o',markersize=8,linewidth=3.5)

		plt.xticks(fontsize=size,rotation=45)
		plt.yticks(fontsize=size)
		plt.xlabel('Fechas',fontsize=size)
		plt.ylabel('Activos',fontsize=size)
		plt.title("Cantidad de casos activos en Caldas",fontsize=size)
		plt.grid(True)
		
		fig = matplotlib.pyplot.gcf()
		fig.set_size_inches(len(muestras)*2,15)
		fig.savefig('activosCaldas.png', dpi=100)
	
	return plt

def create_xlabel(fechas):
	result = []
	frec = 10
	
	for i in range(len(fechas)):
		if(i % frec == 0):
			result.append(fechas[i])
		else:
			result.append("")
	return result

def create_xposition(fechas):
	result = []
	frec = 1
	pos = 0
	
	for i in range(len(fechas)):
		pos += frec
		result.append(pos)

	return result

def gHistorial2(fechas,muestras,size_text):
	nMuestras=[]
	size=size_text
	
	for m in muestras:
		if(m!="\n" and m!=""):
			nMuestras.append(int(m))
			
	with plt.style.context('dark_background'):
		fig, ax = plt.subplots()
		ax.set_xticks(create_xposition(fechas))
		ax.set_xticklabels(create_xlabel(fechas))
		
		for label in ax.get_xticklabels():
			label.set_rotation(45)
			label.set_fontsize(size-7)
			
		for label in ax.get_yticklabels():
			label.set_fontsize(size)
		
		ax.set_ylabel('Activos',fontsize=size)
		ax.set_xlabel(f'{fechas[0]} {fechas[-1]}',fontsize=size-5)
		ax.set_title("Historico de casos activos en Caldas",fontsize=size)
		plt.bar([i for i in range(len(fechas))], nMuestras, width = 1.0, color='orange')
		fig.set_size_inches(15,10)
		fig.savefig('activosCaldas1.png', dpi=100)	
	return plt


		
def historial(nActivos):
	#open("muestras.txt","w").close()
	#open("fechas.txt","w").close()
	obj_muestra = {}
	list_obj_muestra = []
	
	visibles=15

	print(f"Activos: {str(nActivos)}")

	muestra=str(nActivos)
	fecha=date.today().strftime("%d-%b-%Y")

	muestras=requests.get(sourceDb).json()
	cantidades=[m['cantidad'] for m in muestras.values()]
	fechas=[m['fecha'] for m in muestras.values()]
	
	
	if((muestra not in cantidades) and (fecha not in fechas)):

		if(requests.post(sourceDb,json = {'fecha':fecha,'cantidad':muestra}).status_code == 200):
			cantidades.append(muestra)
			fechas.append(fecha)
			print(cantidades)
		
	#gHistorial(fechas,cantidades,20)
	gHistorial2(fechas,cantidades,20)
	#gHistorial(fechas[len(fechas)-visibles:],cantidades[len(cantidades)-visibles:],10).show()
	
		
	#fw.close()
	#fr.close()
		
def getActivos(data):
	cantidad=0
	cerca=0
	for row in data:
		if("fecha_muerte" not in row.keys() and "fecha_recuperado" not in row.keys() ):
		
			cantidad+=1
			if(row["ciudad_municipio_nom"].lower() == "supia"):
				cerca+=1
				#viewData(row)
				print(f"{row['fecha_inicio_sintomas'].split(' ')[0]:11}|{row['fecha_diagnostico'].split(' ')[0]:11}|{row['edad']}|{row['sexo']}|{row['ubicacion']}")
			
	print(f"Cercanos: {cerca}")
	return cantidad
	

try:
	data=getInfo2(source)
	new_data = getInfo2(new_source)
	nActivos = len(new_data)
	historial(nActivos)
	getActivos(new_data)
except Exception as e:
	print(e)
	print("Falla")
	input()
	
	
	
'''
import requests
import json
import os
from datetime import datetime
from datetime import date
#from matplotlib import pyplot
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

source='https://www.datos.gov.co/resource/gt2j-8ykr.json?$limit=100000&departamento_nom=CALDAS'
new_source = 'https://www.datos.gov.co/resource/gt2j-8ykr.json?$limit=100000&recuperado=Activo&departamento_nom=CALDAS&$where=fecha_recuperado IS NULL AND fecha_muerte IS NULL'
sourceDb='https://datacovidcaldas.firebaseio.com/muestras.json'

campos={
	"fecha":'fecha_diagnostico',
	"estado":'estado',
	"ciudad":'ciudad_municipio_nom',
	"atencion":'ubicacion',
	"genero":'sexo',
	"sintomas":'fecha_inicio_sintomas'
}

ini=datetime.now()
dicS={}
dicL={}
dicE={}
dicEs={}
dicFe={}
dicEd={"0-9":0,"10-19":0,"20-29":0,"30-39":0,"40-49":0,"50-59":0,"60-89":0,"90-100":0}

lk={
	'fecha_diagnostico',
	'estado',
	'ciudad_de_ubicaci_n',
	'atenci_n',
	'tipo',
	'sexo',
	'fis'
}


def file(string):
	fw=open("reporte.txt","a",encoding="utf-8")
	fw.write(string+"\n")
	fw.close()

def ft(string,esp):
	espacios=esp-len(string)
	for i in range(espacios):
		string=string+" "
	return string+"║ "

def getInfo(url):  
	req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
	data = urlopen(req).read()
	decoded = json.loads(data)
	return decoded	
	
def corregirLlaves(row):
	for k in lk:
		print(row)
		if(k not in list(row.keys())):
			
			row[k]="?"
			return False
		
	return True
			
def ordenado(dic):

	for row in dic:
		pass

def procesoDatos(data):
	count=1
	erroneos=0
	correcto=None
	
	file(" # ║   Reporte  ║   Sintomas    ║     Lugar      ║    Estado   ║Edad║Genero║ Contagio");
	for row in data:
		
		correcto=corregirLlaves(row);
		
		if(correcto and row["fecha_diagnostico"]!="?"):
			#if(":" in row["fecha_diagnostico"] ):
			#	dia=int(row["fecha_diagnostico"].split("-")[2].split("T")[0])
			#	mes=int(row["fecha_diagnostico"].split("-")[1])
			
			#if((int(ini.day)==dia or int(ini.day)-1==dia) and ini.month == int(mes)):
				#file('	{0}{1}{2:5s}{3}{4}{5}{6}'.format(ft(str(count),3),ft(row["fecha_diagnostico"].split("T")[0],11),ft(row["fis"].split("T")[0],14),ft(row['ciudad_de_ubicaci_n'],15),ft(row['atenci_n'],12),ft(row['edad'],3),ft(row['sexo'],2),row['tipo']))
			count+=1

			if(row['ciudad_de_ubicaci_n']=='Supía'):
				file(ft(str(count),3)+ft(row["fecha_diagnostico"].split("T")[0],11)+ft(row["fis"].split("T")[0],14)+ft(row['ciudad_de_ubicaci_n'],15)+ft(row['atenci_n'],12)+ft(row['edad'],3)+ft(row['sexo'],5)+row['tipo'])
				if(correcto==False):
					print(row)
				
			if(row['atenci_n']!='Recuperado' and row['atenci_n']!='Fallecido'):
				setDic(row['estado'],dicEs)
				setDic(row['ciudad_de_ubicaci_n'],dicL)
				setEdDic(row['edad'],dicEd)
				
			setDic(row['sexo'],dicS)
			setDic(row['atenci_n'],dicE)
			setDic(row["fecha_diagnostico"].split("T")[0],dicFe)
		else:
			erroneos+=1
			
	print("Erroneos: ",erroneos)
	
def getEstados(data):
	for row in data:
		if('atenci_n' in row.keys()):
			setDic(row['atenci_n'],dicE)
	
def recuperacion(nRecuperados):
	r = open('sanados.txt', 'r')
	g = r.readline()
	
	if(int(g)<int(nRecuperados)):
		r = open('sanados.txt', 'w')
		r.write(str(nRecuperados))
		r.close()
		return str(nRecuperados)+"_"+str(nRecuperados-int(g))
	
	r.close()
	return str(nRecuperados)
	
def setDic(key,dic):
	if(key in list(dic.keys())):
		dic[key]=int(dic[key])+1
	else:
		dic[key]=1
					
def setEdDic(key,dic):
	for (c,v) in dic.items():
		if(int(key)<=int(c.split("-")[1]) and int(key)>=int(c.split("-")[0])):
			dic[c]=int(dic[c])+1
	
def barra(n,total,c1,c2):
	cad=""
	size=(n*100)/total
	for i in range(round(size)):
		cad=cad+c1
	for i in range(100-round(size)):
		cad=cad+c2
	return cad+" "+str(round(size))+"%"
		
def verG(dic,total):
	for (c,v) in dic.items():
		file("	"+str(c)+":"+str(v)+" ")
		file("	"+barra(int(v),total,"▓","░"))
		
def nActivos(dicE):
	count=0
	for k in dicE.keys():
		if(k!="Fallecido" and k!="Recuperado"):
			count=count+int(dicE[k])
	return count;

def viewData(d):
	for c,v in d.items():
		print(f"{c:23s}: {v}")
	print("\n")



def getInfo2(url):
	r = requests.get(url)
	return r.json()

def gHistorial(fechas,muestras,size_text):
	nMuestras=[]
	size=size_text
	
	for m in muestras:
		if(m!="\n" and m!=""):
			nMuestras.append(int(m))
			
	with plt.style.context('dark_background'):
			
		plt.plot(fechas,nMuestras,color='red',marker='o',markersize=8,linewidth=3.5)

		plt.xticks(fontsize=size,rotation=45)
		plt.yticks(fontsize=size)
		plt.xlabel('Fechas',fontsize=size)
		plt.ylabel('Activos',fontsize=size)
		plt.title("Cantidad de casos activos en Caldas",fontsize=size)
		plt.grid(True)
		
		fig = matplotlib.pyplot.gcf()
		fig.set_size_inches(len(muestras)*2,15)
		fig.savefig('activosCaldas.png', dpi=100)
	
	return plt

def create_xlabel(fechas):
	result = []
	frec = 10
	
	for i in range(len(fechas)):
		if(i % frec == 0):
			result.append(fechas[i])
		else:
			result.append("")
	return result

def create_xposition(fechas):
	result = []
	frec = 1
	pos = 0
	
	for i in range(len(fechas)):
		pos += frec
		result.append(pos)

	return result

def gHistorial2(fechas,muestras,size_text):
	nMuestras=[]
	size=size_text
	
	for m in muestras:
		if(m!="\n" and m!=""):
			nMuestras.append(int(m))
			
	with plt.style.context('dark_background'):
		fig, ax = plt.subplots()
		ax.set_xticks(create_xposition(fechas))
		ax.set_xticklabels(create_xlabel(fechas))
		
		for label in ax.get_xticklabels():
			label.set_rotation(45)
			label.set_fontsize(size-7)
			
		for label in ax.get_yticklabels():
			label.set_fontsize(size)
		
		ax.set_ylabel('Activos',fontsize=size)
		ax.set_xlabel(f'{fechas[0]} {fechas[-1]}',fontsize=size-5)
		ax.set_title("Historico de casos activos en Caldas",fontsize=size)
		plt.bar([i for i in range(len(fechas))], nMuestras, width = 1.0, color='orange')
		fig.set_size_inches(15,10)
		fig.savefig('activosCaldas1.png', dpi=100)	
	return plt


		
def historial(nActivos):
	#open("muestras.txt","w").close()
	#open("fechas.txt","w").close()
	obj_muestra = {}
	list_obj_muestra = []
	
	
	visibles=15

	print(f"Activos: {str(nActivos)}")

	muestra=str(nActivos)
	fecha=date.today().strftime("%d-%b-%Y")

	#fr=open("muestras.txt","r",encoding="utf-8")
	#fw=open("muestras.txt","a",encoding="utf-8")
	
	#muestras=fr.readlines()
	muestras=requests.get(sourceDb).json()
	
	#visibles=len(muestras)#-----------------------------
	
	#cantidades=[m.split(",")[0] for m in muestras]
	#fechas=[m.split(",")[1] for m in muestras]
	
	cantidades=[m['cantidad'] for m in muestras.values()]
	fechas=[m['fecha'] for m in muestras.values()]
	
	#for i in range(len(cantidades)):
	#	list_obj_muestra.append({'fecha':fechas[i],'cantidad':cantidades[i]})
		
	
	if((muestra not in cantidades) and (fecha not in fechas)):
		#fw.write(muestra+","+fecha+"\n")
		#list_obj_muestra.append({'fecha':fecha,'cantidad':muestra})
		#print(requests.put(sourceDb,json = list_obj_muestra).status_code) 
		if(requests.post(sourceDb,json = {'fecha':fecha,'cantidad':muestra}).status_code == 200):
			cantidades.append(muestra)
			fechas.append(fecha)
			print(cantidades)
		
	#gHistorial(fechas,cantidades,20)
	gHistorial2(fechas,cantidades,20)
	#gHistorial(fechas[len(fechas)-visibles:],cantidades[len(cantidades)-visibles:],10).show()
	
		
	#fw.close()
	#fr.close()
		
def getActivos(data):
	cantidad=0
	cerca=0
	for row in data:
		if("fecha_muerte" not in row.keys() and "fecha_recuperado" not in row.keys() ):
		
			cantidad+=1
			if(row["ciudad_municipio_nom"].lower() == "supia"):
				cerca+=1
				#viewData(row)
				print(f"{row['fecha_inicio_sintomas'].split(' ')[0]:11}|{row['fecha_diagnostico'].split(' ')[0]:11}|{row['edad']}|{row['sexo']}|{row['ubicacion']}")
			
	print(f"Cercanos: {cerca}")
	return cantidad
	

open("reporte.txt","w").close()


for i in range(255):
	print(str(i)+" "+str(chr(i)))
	file(str(i)+" "+str(chr(i)))
	
file("Reportes de Covid-19 en CALDAS\n")
file("->Casos Nuevos:\n...")	



try:
	data=getInfo2(source)
	nActivos=getActivos(data)
	print(nActivos)
	new_data = getInfo2(new_source)
	nActivos = len(new_data)
	#getEstados(data)
	#nActivos=nActivos(dicE)
	historial(nActivos)
	#print(f"Total de registros: {str(len(data))}")
except Exception as e:
	print(e)
	print("Falla")
	input()




dicE={}
procesoDatos(data)

file("\nTotal:"+str(total))
file("Activos:"+str(nActivos))
file("Recuperados:"+recuperacion(dicE["Recuperado"])+"\n")
	

#input("\nENTER para ver detalles...")

file("	"+barra(nActivos,total,"▓","░").split(" ")[0])
file("\n->Estado de reportes:\n")
verG(dicE,total)
file("\n->Estado de Activos:\n")
verG(dicEs,nActivos)
file("\n->Lugar de Activos:\n")
verG(dicL,nActivos)
file("\n->Edades de Activos:\n")
verG(dicEd,nActivos)
file("\n->Genero:\n")
verG(dicS,total)

file("\n->Conteo por dias:\n")
verG(dicFe,max(list(dicFe.values())))



#os.system("nano reporte.txt")

os.system("start /MAX notepad.exe reporte.txt")

input("\nENTER para ver detalles...")

pyplot.pie(dicE.values(),colors=('green','red','yellow','orange'),labels=(dicE.keys()),autopct='%1.1f%%',shadow=True,startangle=90)
pyplot.axis('equal')
pyplot.title('Estado')
pyplot.show()

pyplot.pie(dicEs.values(),colors=('green','red','yellow','orange'),labels=(dicEs.keys()),autopct='%1.1f%%',shadow=True,startangle=90)
pyplot.axis('equal')
pyplot.title('Estado de '+str(nActivos)+' Activos')
pyplot.show()

pyplot.pie(dicS.values(),colors=('blue','red','black','yellow'),labels=(dicS.keys()),autopct='%1.1f%%',shadow=True,startangle=90)
pyplot.axis('equal')
pyplot.title('Genero')
pyplot.show()

input()


#https://www.datos.gov.co/resource/gt2j-8ykr.json?$limit=100000&$select=atenci_n,COUNT(atenci_n)&$group=atenci_n&departamento=Caldas
 

'''

