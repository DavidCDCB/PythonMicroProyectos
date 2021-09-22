import random
import time
import os
import pygame

pygame.init()

life = 18
max_life = 18
atack = 1
shield = 0
score = 0

num_cels = 3

cube = [[None]*num_cels for i in range(num_cels)]
pos = [(len(cube)//2),(len(cube)//2)]


def print_cube():
	global life,max_life,atack,shield,score
	line = "\033[1;34;40m║\033[0m"

	BC = {
	    "HEADER": '\033[0;30;41m',
	    "OKBLUE": '\033[0;30;44m',
	    "OKCYAN": '\033[0;30;46m',
	    "OKGREEN": '\033[0;30;42m',
	    "WARNING": '\033[0;30;43m',
	}

	print(f"SCORE: {score}")
	for i in range(len(cube)):
		cad = line
		for j in range(len(cube[i])):
			item = cube[i][j]
			
			if(item['type'] == "E"):
				cad += f"{BC['HEADER']}{item['value']:2} \033[0m{line}"
			elif(item['type'] == "A"):
				cad += f"{BC['OKCYAN']}{item['value']:2} \033[0m{line}"
			elif(item['type'] == "S"):
				cad += f"{BC['WARNING']}{item['value']:2} \033[0m{line}"
			elif(item['type'] == "L"):
				cad += f"{BC['OKGREEN']}{item['value']:2} \033[0m{line}"
			else:
				cad += f" \033[6m{cube[i][j]['type']}\033[0m {line}"
		print("\033[1;34;40m╬═══╬═══╬═══╬\033[0m")
		print(cad)
	print("\033[1;34;40m╬═══╬═══╬═══╬\033[0m")
	print(f"{BC['OKGREEN']}HP: {life}/{max_life}  {BC['OKCYAN']}ATK: {atack}  {BC['WARNING']}DEF: {shield}\033[0m ")


def select_element(l_por):
	enemies = [
		{"type":"E","value":3},{"type":"E","value":6},{"type":"E","value":2},{"type":"E","value":9},
		{"type":"E","value":2},{"type":"E","value":4},{"type":"E","value":7},{"type":"E","value":5}
	]
	lifes =	[{"type":"L","value":3},{"type":"L","value":5}]
	shields = [{"type":"S","value":4},{"type":"S","value":8},{"type":"S","value":5}]
	wapons = [{"type":"A","value":7},{"type":"A","value":5},{"type":"A","value":3}]
	
	select = random.choices([enemies,wapons,lifes,shields], weights = l_por)[0]
	
	select = random.choice(select)
	return {'type':select['type'],'value':select['value']}


def complete_cube():
	for i in range(len(cube)):
		for j in range(len(cube[i])):
			if(cube[i][j] == None):
				cube[i][j] = select_element([40,35,15,15])


def check_pos(p,np):
	if(np[0]<=len(cube)-1 and np[1]<=len(cube)-1 and np[0]>=0 and np[1]>=0):
		return np
	else:
		return p

def interaction(pos_P,pos_E):
	global cube,life,max_life,atack,shield,score

	element = cube[pos_E[0]][pos_E[1]]
	move = False

	if(element["type"] == "E"):
	
		life_e = cube[pos_E[0]][pos_E[1]]['value']

		if(atack > 0):
			score += atack
			if(atack <= life_e):
				life_e -= atack
				atack = 0
			else:
				t_life = life_e
				life_e -= atack
				atack -= t_life

			cube[pos_E[0]][pos_E[1]]['value'] = life_e

			if(life_e>0):
				return False
			else:
				return True

		if(shield == 0):
			life -= element['value']
			return True

		if(shield > 0):
			if(element['value'] - shield > 0):
				life -= element['value'] - shield
			shield -= element['value']
			if(shield<0):shield = 0
			return True
			

	if(element["type"] == "A"):
		atack = element['value']
		move = True

	if(element["type"] == "S"):
		shield = element['value']
		move = True

	if(element["type"] == "L"):
		life += element['value']
		if(life>max_life):life=max_life
		move = True

	return move


def set_pos(move):
	global cube, pos

	n_pos = pos.copy()
	if(move == "w"):
		n_pos[0] -= 1
	if(move == "s"):
		n_pos[0] += 1
	if(move == "a"):
		n_pos[1] -= 1
	if(move == "d"):
		n_pos[1] += 1

	if(str(pos) != str(check_pos(pos,n_pos))):
		if(interaction(pos,n_pos) == True):
			cube[pos[0]][pos[1]] = None
			pos = check_pos(pos,n_pos)
			cube[pos[0]][pos[1]] = {"type":"P"}

def print_format_table():
    #prints table of formatted text format options
    for style in range(8):
        for fg in range(30,38):
            s1 = ''
            for bg in range(40,48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print('\n')


def render_img(pg,canvas,img,x,y):
	image = pg.image.load(img)
	image = pg.transform.scale(image, (30, 30))
	rect = image.get_rect()
	rect.top = y
	rect.left = x
	canvas.blit(image,rect)

def render(pg,surface,matrix):
	red = (178, 24, 24)
	yellow = (252, 205, 69)
	green = (24, 178, 24)
	blue = (24, 178, 178)
	desface = 35

	font = pg.font.Font(None, 50)
	font_attr = pg.font.Font(None, 30)

	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			if("value" in matrix[i][j].keys()):
				texto1 = font.render(f"{matrix[i][j]['value']}", 0, (0, 0, 0))
			else:
				texto1 = font.render(f"{matrix[i][j]['type']}", 0, (255, 255, 255))

			if(matrix[i][j]['type'] == "E"):
				pg.draw.rect(surface, red, (j*100, i*100, 100, 100))
			if(matrix[i][j]['type'] == "S"):
				pg.draw.rect(surface, yellow, (j*100, i*100, 100, 100))
			if(matrix[i][j]['type'] == "A"):
				pg.draw.rect(surface, blue, (j*100, i*100, 100, 100))
			if(matrix[i][j]['type'] == "L"):
				pg.draw.rect(surface, green, (j*100, i*100, 100, 100))

			if(matrix[i][j]['type'] != "P"):
				surface.blit(texto1, ((j*100)+desface,(i*100)+desface))
				pg.draw.rect(surface, (0, 0, 0), (j*100, i*100, 100, 100),3)
			else:
				r_score = font.render(f"{score}", 1, (255, 255, 255))
				surface.blit(r_score, ((j*100)+desface,(i*100)+desface))
				r_life = font_attr.render(f"{life}", 1, green)
				r_armor = font_attr.render(f"{atack}", 1, blue)
				r_def = font_attr.render(f"{shield}", 1, yellow)
				
				surface.blit(r_life, ((j*100),(i*100)))
				surface.blit(r_armor, ((j*100)+40,(i*100)))
				surface.blit(r_def, ((j*100)+80,(i*100)))
				

#print_format_table()

complete_cube()
cube[pos[0]][pos[0]] = {"type":"P"}
print_cube()

clock = pygame.time.Clock()
superficie = pygame.display.set_mode((num_cels*100,num_cels*100))#Crea el fondo
pygame.display.set_caption('DungeonCube')
superficie.fill((0,0,0))#color del fondo RGB
fuente = pygame.font.Font(None, 50)
game_exit = False


while(life>0 and game_exit == False):
	clock.tick(60)
	superficie.fill((0,0,0))

	for event in pygame.event.get():
		if(event.type==pygame.QUIT):
			game_exit = True

		if(event.type==pygame.KEYDOWN):	
			if(event.key==pygame.K_UP):			
				move = "w"
			elif(event.key==pygame.K_DOWN):			
				move = "s"
			elif(event.key==pygame.K_RIGHT):			
				move = "d"
			elif(event.key==pygame.K_LEFT):			
				move = "a"
			else:
				move = ""
				
			if(move != ""):
				set_pos(move)
				complete_cube()
				os.system("clear")
				#print_cube()

	render(pygame,superficie,cube)
	pygame.display.update()
	
print("GAME OVER")



