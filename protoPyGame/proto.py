from os import system as exc
import sys
import random

fail = True
start = False
points = 0

class Personaje:
	def __init__(self,pg,s,x,y,r):
		self.image = pg.image.load(r)
		self.image = pg.transform.scale(self.image, (30, 30))
		self.rect = self.image.get_rect()
		self.rect.size = (30,20)
		self.rect.top = y
		self.rect.left = x
		self.speed = 2 
		self.surface=s

		self.estado = ""
		self.dis_move = 0   
	
	def get_Y(self):
		return self.rect.top
	def set_Y(self,y):
		self.rect.top=y
	def set_X(self,x):
		self.rect.left=x
	def get_X(self):
		return self.rect.left
	def get_rect(self):
		return self.rect
	def set_rect(self,r):
		self.rect=r
	def get_img(self):
		return self.image
	def set_img(self,i):
		self.image=i
		
	def get_speed(self):
		return self.speed
		
	def render(self):
		self.surface.blit(self.image, self.rect)

	def check_jump(self):
		speed = 3
		if(self.estado == "subida"):
			if(self.dis_move <= 90):
				self.set_Y(self.get_Y()-speed)
				self.dis_move += speed
			else:
				self.estado = "caida"

		if(self.estado == "caida"):
			if(self.dis_move >= 0):
				self.set_Y(self.get_Y()+speed)
				self.dis_move -= speed
			else:
				self.estado = ""


class Enemy:
	def __init__(self,pg,s,x,y,r,size):
		self.image = pg.image.load(r)
		self.image = pg.transform.scale(self.image, size)
		self.rect = self.image.get_rect()
		self.rect.top = y
		self.rect.left = x
		self.surface = s
		self.rect.size = size

	def get_rect(self):
		return self.rect
	def set_X(self,x):
		self.rect.left=x
	def get_X(self):
		return self.rect.left
	def render(self):
		self.surface.blit(self.image, self.rect)

def colicion(obj1,obj2):
	return obj1.get_rect().colliderect(obj2.get_rect())

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

def render_img(pg,canvas,img,x,y):
	image = pg.image.load(img)
	image = pg.transform.scale(image, (700, 300))
	rect = image.get_rect()
	rect.top = y
	rect.left = x
	canvas.blit(image,rect)
	return image
	
	
	
def colicion(obj1,obj2):
	return obj1.get_rect().colliderect(obj2.get_rect())

def gameLoop(pygame):
	global fail, start, points
	pygame.init()
	
	gameExit = False
	clock = pygame.time.Clock()
	surface = pygame.display.set_mode((700,300))#Crea el fondo
	pygame.display.set_caption('PySnake')
	surface.fill((0,0,0))#color del fondo RGB
	fuente = pygame.font.Font(None, 50)
	fuente1 = pygame.font.Font(None, 30)
	text = "Press Space..."

	obj = Personaje(pygame,surface,10,300-30,"./src/img/seg.png")
	list_enemy = []

	distances = [150,200,300]
	height = [50,60,20] 
	posicion = 300
	for e in range(10):
		altura = random.choice(height)
		list_enemy.append(Enemy(pygame,surface,posicion,300-altura,"./src/img/seg.bmp",(20,altura)))
		posicion += random.choice(distances)

	while not gameExit:
		clock.tick(60)
		surface.fill((0,0,0))
		render_img(pygame,surface,"./src/img/bg.jpg",0,0)
		#surface.blit(fuente1.render(f"Points: {points}", 0, (255, 255, 255)), (0,0))
		#surface.blit(fuente.render(text, 0, (255, 255, 255)), (0,20))

		for event in pygame.event.get():
			if(event.type==pygame.QUIT):
				gameExit=True
							
			if(event.type==pygame.KEYDOWN):			
				if(event.key == pygame.K_SPACE):
					if(obj.estado == ""):
						obj.estado = "subida"
					
		obj.check_jump()
		obj.render()
		
		for e in list_enemy:
			e.set_X(e.get_X()-1)
			e.render()

			if(colicion(e,obj)):
				print(list_enemy.index(e))

			if(e.get_X() < 0):
				list_enemy.remove(e)
		
		pygame.display.update()
pg = verificar_paquete()
gameLoop(pg)

