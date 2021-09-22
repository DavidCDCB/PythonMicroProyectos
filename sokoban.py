from os import system as exc
import sys

matriz_mapa = []
matriz_objetos = []
matriz_actual = []
pos_c = []
pos_h = []
pos_p = [0,0]
g_puntos = 0
completado = False
inicio = True
num_file = 1

m_level = []

def printMatriz(m):
	BCOLORS = {
	    "HEADER": '\033[95m',
	    "OKBLUE": '\033[94m',
	    "OKCYAN": '\033[96m',
	    "OKGREEN": '\033[92m',
	    "WARNING": '\033[93m',
	}

	color = ''
	cad = ''
	for i in range(len(m)):
		for j in range(len(m[i])):
			if(m[i][j] == "#"):
				color = BCOLORS['WARNING']
			if(m[i][j] == "*"):
				color = BCOLORS['OKGREEN']
			if(m[i][j] == "@"):
				color = BCOLORS['OKCYAN']
			if(m[i][j] == "&"):
				color = BCOLORS['HEADER']
			if([i,j] in pos_h and m[i][j] == "@"):
				color = BCOLORS['OKGREEN']

			cad += color+m[i][j]+'\033[0m'
		print(cad)
		cad = ''

def convertir_fila(f,limp):
	for i in range(len(f)):
		if(f[i] != "\n"):
			if(limp == False):
				if(f[i] == "+" or f[i] == "@"):
					f[i] = '&'
				if(f[i] == "$" or f[i] == "*"):
					f[i] = '@'
				if(f[i] == "."):
					f[i] = '*'

			else:
				if(f[i] == "+" or f[i] == "*"):
					f[i] = '*'
				if(f[i] == "@"):
					f[i] = ' '
				if(f[i] == "$"):
					f[i] = ' '
				if(f[i] == "."):
					f[i] = '*'
		else:
			f[i] = ""
	return f


def readFile(nF):
	global m_level
	fr = open(f"Classic.txt", "r", encoding="utf-8")
	lines = fr.readlines()
	fr.close()
	lines = list(filter(lambda x: x != "\n", lines))

	aux = ""
	for l in lines:
		if(";" in l):
			m_level.append(aux)
			aux = ""
		else:
			aux += l

	for l in m_level[nF].split("\n"):
		if(l != "\n"):
			matriz_mapa.append(convertir_fila(list(l),True))
			matriz_objetos.append(convertir_fila(list(l),False))

	printMatriz(matriz_objetos)

def verificar_paquete():
	try:
		from pynput import keyboard as k
	except ImportError as e:
		print("Intalando Paquete...")
		if(sys.platform.startswith('linux')):
			exc("sudo pip3 install pynput")
		else:
			exc("pip install pynput")
		from pynput import keyboard as k
	return k

def figura(num):
	if(num == 0):
		return ' '
	if(num == 1):
		return '#'
	if(num == 2):
		return '.'
	if(num == 3):
		return '@'
	if(num == 4):
		return "&"

def limpiar():
	if(sys.platform.startswith('linux')):
		exc("clear")
	else:
		exc("cls")

def encontrar_objetos(mE,mO):
	for i in range(len(mO)):
		for j in range(len(mO[i])):
			if(mO[i][j] == "&"):
				pos_p[0] = i
				pos_p[1] = j
			if(mO[i][j] == '@'):
				pos_c.append([i,j])
			if(mO[i][j] == '*'):
				pos_h.append([i,j])

def verificar_puntos():
	global pos_c, matriz_mapa, g_puntos, completado
	puntos = 0
	
	for c in pos_c:
		if(matriz_mapa[c[0]][c[1]] == '*'):
			puntos += 1

	g_puntos = puntos
	if(puntos == len(pos_c)):
		print("\nGANASTE!")
		completado = True


def asignar_objetos():
	global matriz_actual, matriz_mapa, matriz_objetos

	matriz_actual = matriz_mapa.copy()
	for i in range(len(matriz_mapa)):
		matriz_actual[i] = matriz_mapa[i].copy()

	for i in range(len(matriz_objetos)):
		for j in range(len(matriz_objetos[i])):
			if(matriz_objetos[i][j] == "&" or matriz_objetos[i][j] == '@'):
				matriz_actual[i][j] = matriz_objetos[i][j]


def ubicar_P(pP,npP,nObj):
	global matriz_actual, matriz_mapa, matriz_objetos

	matriz_objetos[pP[0]][pP[1]] = matriz_mapa[pP[0]][pP[1]]
	matriz_objetos[npP[0]][npP[1]] = nObj
	

def validar_C(pC,npC,dir):
	global matriz_actual, matriz_mapa, matriz_objetos
	
	if(matriz_mapa[npC[0]][npC[1]] == '#' or matriz_objetos[npC[0]][npC[1]] == '@'):
		return pC

	return npC

def evaluar_C(pC,dir):
	npC = pC.copy()

	if(dir == "u"):
		npC[0] -= 1 
	if(dir == "d"):
		npC[0] += 1 
	if(dir == "l"):
		npC[1] -= 1 
	if(dir == "r"):
		npC[1] += 1

	if(validar_C(pC,npC,dir) != pC):
		npC = validar_C(pC,npC,dir)
		matriz_objetos[pC[0]][pC[1]] = matriz_mapa[pC[0]][pC[1]]
		matriz_objetos[npC[0]][npC[1]] = '@'
		return True
	else:
		return False

def validar_P(pP,npP,dir):
	global matriz_actual, matriz_mapa, matriz_objetos

	if(matriz_objetos[npP[0]][npP[1]] == '@'):
		if(evaluar_C(npP,dir)):
			return npP
		else:
			return pP

	if(matriz_mapa[npP[0]][npP[1]] == '#'):
		return pP

	if(matriz_mapa[npP[0]][npP[1]] == ' ' or matriz_mapa[npP[0]][npP[1]] == '*'):
		return npP


def evaluar(dir):
	global pos_c, pos_p
	pos_c = []
	encontrar_objetos(matriz_mapa,matriz_objetos)
	verificar_puntos()
	temp_pos_p = pos_p.copy()

	if(dir == "u"):
		temp_pos_p[0] -= 1 
	if(dir == "d"):
		temp_pos_p[0] += 1 
	if(dir == "l"):
		temp_pos_p[1] -= 1 
	if(dir == "r"):
		temp_pos_p[1] += 1 

	
	ubicar_P(pos_p,validar_P(pos_p,temp_pos_p,dir),"&")
	asignar_objetos()
	printMatriz(matriz_actual)
	

def reiniciar():
	global num_file,matriz_mapa,matriz_objetos,matriz_actual,pos_c,pos_h,pos_p,g_puntos,num_file,inicio,completado

	matriz_mapa = []
	matriz_objetos = []
	matriz_actual = []
	pos_c = []
	pos_h = []
	pos_p = [0,0]
	g_puntos = 0
	inicio = True
	completado = False

def pulsaciones(p):
	global completado, num_file, inicio

	if(inicio == True):
		limpiar()
		readFile(num_file)
		inicio = False

	if(completado):
		reiniciar()
		num_file += 1
		print(f"\n\nNivel {num_file} Enter para iniciar")
	else:
		if(str(p) == "Key.up"):
			limpiar()
			evaluar("u")
		if(str(p) == "Key.down"):
			limpiar()
			evaluar("d")
		if(str(p) == "Key.right"):
			limpiar()
			evaluar("r")
		if(str(p) == "Key.left"):
			limpiar()
			evaluar("l")
		if(str(p) == "'r'"):
			limpiar()
			print("Reiniciar, enter para continuar...")
			reiniciar()
		


print("Nivel 1 Enter para iniciar")
with verificar_paquete().Listener(on_press=pulsaciones) as listen:
	listen.join()
		