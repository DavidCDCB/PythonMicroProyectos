from os import system as exc
import sys

# http://www.sokobano.de/wiki/index.php?title=Level_format
# https://www.sourcecode.se/sokoban/levels

matriz_mapa = []
matriz_objetos = []
matriz_actual = []
pos_c = []
pos_c_block = []
pos_h = []
pos_p = [0,0]
g_puntos = 0
completado = False
inicio = True
num_file = 1
direccion = 'd'
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
	#limpiar()

	for i in range(len(m)):
		for j in range(len(m[i])):
			if(m[i][j] == "#"):# Pared
				color = BCOLORS['WARNING']
			if(m[i][j] == "*"):# Hueco
				color = BCOLORS['OKGREEN']
			if(m[i][j] == "@"):# Caja
				color = BCOLORS['OKCYAN']
			if(m[i][j] == "&"):# Personaje
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
	fr = open(f"src/levels/microban1.txt", "r", encoding="utf-8")
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


def verificar_paquete():
	try:
		import pygame as pg
	except ImportError as e:
		print("Intalando Paquete...")
		if(sys.platform.startswith('linux')):
			exc("sudo pip3 install pygame")
		else:
			exc("pip install pygame")
		import pygame as pg
	return pg

def limpiar():
	if(sys.platform.startswith('linux')):
		exc("clear")
	else:
		exc("cls")

def encontrar_objetos(mO):
	for i in range(len(mO)):
		for j in range(len(mO[i])):
			if(mO[i][j] == "&"):
				pos_p[0] = i
				pos_p[1] = j
			if(mO[i][j] == '@'):
				if([i,j] not in pos_c):
					pos_c.append([i,j])
			if(mO[i][j] == '*'):
				if([i,j] not in pos_h):
					pos_h.append([i,j])

def verificar_puntos():
	global pos_c, matriz_mapa, g_puntos, completado
	puntos = 0
	
	encontrar_objetos(matriz_objetos)
	for c in pos_c:
		if(c in pos_h):
			puntos += 1

	g_puntos = puntos
	if(g_puntos == len(pos_c) and len(pos_c) != 0):
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
	global pos_c, pos_p, direccion
	direccion = dir
	pos_c = []
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
	pos_c_block = []
	pos_h = []
	pos_p = [0,0]
	g_puntos = 0
	inicio = True
	completado = False

def evaluar_bloqueos():
	global pos_c_block
	pos_c_block = []
	for c in pos_c:
		n_bloqueo = 0
		l_adyacentes = []

		if(c not in pos_h):
			if((matriz_mapa[c[0]][c[1]+1] == "#" or matriz_objetos[c[0]][c[1]+1] == "@") and len(l_adyacentes) < 2):
				l_adyacentes.append(1)
			if((matriz_mapa[c[0]][c[1]-1] == "#" or matriz_objetos[c[0]][c[1]-1] == "@") and len(l_adyacentes) < 2):
				l_adyacentes.append(2)
			if((matriz_mapa[c[0]+1][c[1]] == "#" or matriz_objetos[c[0]+1][c[1]] == "@") and len(l_adyacentes) < 2):
				l_adyacentes.append(3)
			if((matriz_mapa[c[0]-1][c[1]] == "#" or matriz_objetos[c[0]-1][c[1]] == "@") and len(l_adyacentes) < 2):
				l_adyacentes.append(4)

		if(l_adyacentes == [1,3] or l_adyacentes == [1,4] or l_adyacentes == [2,4] or l_adyacentes == [2,3]):
			pos_c_block.append(c)

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
		if(str(p) == "u"):
			limpiar()
			evaluar("u")
		if(str(p) == "d"):
			limpiar()
			evaluar("d")
		if(str(p) == "r"):
			limpiar()
			evaluar("r")
		if(str(p) == "l"):
			limpiar()
			evaluar("l")
		if(str(p) == "'r'"):
			limpiar()
			print("Reiniciar, enter para continuar...")
			reiniciar()
		
def render_img(pg,canvas,img,x,y):
	image = pg.image.load(img)
	rect = image.get_rect()
	rect.top = y
	rect.left = x
	canvas.blit(image,rect)

def render_matriz(pg,canvas,m):
	size_obj = 50
	for i in range(len(m)):
		for j in range(len(m[i])):
			if(m[i][j] == "#"):
				render_img(pg,canvas,"./src/img/wall.bmp", size_obj*j,(size_obj*i)+40)
			if(m[i][j] == "*"):
				render_img(pg,canvas,"./src/img/target.bmp", size_obj*j,(size_obj*i)+40)
			if(m[i][j] == "@"):
				render_img(pg,canvas,"./src/img/box.bmp", size_obj*j,(size_obj*i)+40)
			if(m[i][j] == " "):
				render_img(pg,canvas,"./src/img/space.bmp", size_obj*j,(size_obj*i)+40)	

			if([i,j] in pos_h and m[i][j] == "@"):
				render_img(pg,canvas,"./src/img/box_on_target.bmp", size_obj*j,(size_obj*i)+40)

			if([i,j] in pos_c_block and m[i][j] == "@"):
				render_img(pg,canvas,"./src/img/block.bmp", size_obj*j,(size_obj*i)+40)

			if(m[i][j] == "&"):
				if(direccion == "d"):
					render_img(pg,canvas,"./src/img/pd.bmp", size_obj*j,(size_obj*i)+40)
				elif(direccion == "u"):
					render_img(pg,canvas,"./src/img/pu.bmp", size_obj*j,(size_obj*i)+40)
				elif(direccion == "r"):
					render_img(pg,canvas,"./src/img/pr.bmp", size_obj*j,(size_obj*i)+40)
				elif(direccion == "l"):
					render_img(pg,canvas,"./src/img/pl.bmp", size_obj*j,(size_obj*i)+40)

def gameLoop(pygame):
	global completado, num_file, inicio

	gameExit = False
	clock = pygame.time.Clock()
	superficie = pygame.display.set_mode((1000,700))#Crea el fondo
	pygame.display.set_caption('SokoPy')
	superficie.fill((0,0,0))#color del fondo RGB
	fuente = pygame.font.Font(None, 30)

	while not gameExit:
		clock.tick(60)
		superficie.fill((0,0,0))
		texto1 = fuente.render(f"Nivel {num_file+1}", 0, (255, 255, 255))
		texto2 = fuente.render(f"Use the arrow keys and 'r' to restart the level.", 0, (255, 255, 255))
		superficie.blit(texto1, (0,0))
		superficie.blit(texto2, (0,20))

		if(inicio):
			limpiar()
			readFile(num_file)
			inicio = False
			asignar_objetos()
			encontrar_objetos(matriz_mapa)
			render_matriz(pygame,superficie,matriz_objetos)

		if(completado):
			reiniciar()
			num_file += 1
			fr = open(f"src/save.txt", "w", encoding="utf-8")
			fr.write(str(num_file))
			fr.close()

		render_matriz(pygame,superficie,matriz_actual)
		verificar_puntos()
		#print(g_puntos,pos_h,pos_c)

		for event in pygame.event.get():
			if(event.type==pygame.QUIT):
				gameExit=True
			
			if(event.type==pygame.KEYUP):
				evaluar_bloqueos()
				if(event.key == pygame.K_UP):
					evaluar("u")
				if(event.key == pygame.K_DOWN):
					evaluar("d")
				if(event.key == pygame.K_RIGHT):
					evaluar("r")
				if(event.key == pygame.K_LEFT):
					evaluar("l")

				if(event.key==pygame.K_r):
					reiniciar()

				

		pygame.display.update()


pg = verificar_paquete()
pg.init()

fr = open(f"src/save.txt", "r", encoding="utf-8")
num_file = int(fr.readline())
fr.close()
gameLoop(pg)

