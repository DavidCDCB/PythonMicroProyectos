from os import system as exc
import sys
import random

fail = True
start = False
points = 0

class Segment:
	def __init__(self,pg,s,x,y,r,d):
		self.image = pg.image.load(r)
		self.image = pg.transform.scale(self.image, (30, 30))
		self.rect = self.image.get_rect()
		self.rect.top = y
		self.rect.left = x
		self.rect.size = (20,20)
		self.speed = 2 
		self.surface=s   
		self.direction = d
	
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
		
	def set_direction(self,d):
		self.direction=d
	def get_direction(self):
		return self.direction

	def render(self):
		self.surface.blit(self.image, self.rect)
		
class Item:
	def __init__(self,pg,s,x,y,r):
		self.image = pg.image.load(r)
		self.image = pg.transform.scale(self.image, (50, 50))
		self.rect = self.image.get_rect()
		self.rect.top = y
		self.rect.left = x
		self.n_pos = [random.randint(0+30,500-30),random.randint(0+30,500-30)]
		self.surface=s   
		self.speed = 1

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
		
	def set_n_pos(self,n_pos):
		self.n_pos = n_pos
		
	def render(self):
		self.surface.blit(self.image, self.rect)
		
	def set_pos(self,n_pos):
		if(self.get_X() < self.n_pos[0]):
			self.set_X(self.get_X()+self.speed)
		if(self.get_X() > self.n_pos[0]):
			self.set_X(self.get_X()-self.speed)
		if(self.get_Y() < self.n_pos[1]):
			self.set_Y(self.get_Y()+self.speed)
		if(self.get_Y() > self.n_pos[1]):
			self.set_Y(self.get_Y()-self.speed)
		if(self.get_X() == self.n_pos[0] and self.get_Y() == self.n_pos[1]):
			self.set_n_pos(n_pos)

class Enemy:
	def __init__(self,pg,s,x,y,r):
		self.image = pg.image.load(r)
		self.image = pg.transform.scale(self.image, (50, 50))
		self.rect = self.image.get_rect()
		self.rect.top = y
		self.rect.left = x
		self.surface = s

	def get_rect(self):
		return self.rect

	def render(self):
		self.surface.blit(self.image, self.rect)
			
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
	image = pg.transform.scale(image, (500, 500))
	rect = image.get_rect()
	rect.top = y
	rect.left = x
	canvas.blit(image,rect)
	return image
	
	
def set_pos(obj):
	newPosX = obj.get_X()
	newPosY = obj.get_Y()
	d = obj.direction
	
	if(d == "r" and obj.get_X() < 500-30):
		newPosX = obj.get_X()+obj.get_speed()
	if(d == "l" and obj.get_X()>0):
		newPosX = obj.get_X()-obj.get_speed()
	if(d == "d" and obj.get_Y() < 500-30):
		newPosY = obj.get_Y()+obj.get_speed()
	if(d == "u" and obj.get_Y()>0):
		newPosY = obj.get_Y()-obj.get_speed()
		
	obj.set_X(newPosX)
	obj.set_Y(newPosY)
	
def check_fail(segments,s,h_obj):
	global fail
	if(h_obj.get_X() >= 500-30 or h_obj.get_X() <= 0):
		fail = True
	if(h_obj.get_Y() >= 500-30 or h_obj.get_Y() <= 0):
		fail = True
		
	if(segments.index(s)>1):
		if(colicion(s,h_obj)):
			fail = True

def add_segment(pygame,surface,i_obj,h_obj,segments):
	global points
	space = 50

	if(colicion(i_obj,h_obj)):
		end = segments[-1]
		points += 1
	
		i_obj.set_X(random.randint(0+space,500-space))
		i_obj.set_Y(random.randint(0+space,500-space))
		i_obj.set_n_pos([end.get_X(),end.get_Y()])
		
		if(end.get_direction() == "r"):
			segments.append(Segment(pygame,surface,end.get_X()-30,end.get_Y(),"./src/img/seg.png","r"))
		if(end.get_direction() == "l"):
			segments.append(Segment(pygame,surface,end.get_X()+30,end.get_Y(),"./src/img/seg.png","l"))
		if(end.get_direction() == "u"):
			segments.append(Segment(pygame,surface,end.get_X(),end.get_Y()+30,"./src/img/seg.png","u"))
		if(end.get_direction() == "d"):
			segments.append(Segment(pygame,surface,end.get_X(),end.get_Y()-30,"./src/img/seg.png","d"))

	
def colicion(obj1,obj2):
	return obj1.get_rect().colliderect(obj2.get_rect())

def gameLoop(pygame):
	global fail, start, points
	pygame.init()
	
	gameExit = False
	clock = pygame.time.Clock()
	surface = pygame.display.set_mode((500,500))#Crea el fondo
	pygame.display.set_caption('PySnake')
	surface.fill((0,0,0))#color del fondo RGB
	fuente = pygame.font.Font(None, 50)
	fuente1 = pygame.font.Font(None, 30)

	cut_points = []
	segments = []
	pos_enemy = []

	text = "Press Space..."

	
	while not gameExit:
		clock.tick(60)
		surface.fill((0,0,0))
		render_img(pygame,surface,"./src/img/bg.jpg",0,0)
		surface.blit(fuente1.render(f"Points: {points}", 0, (255, 255, 255)), (0,0))
		surface.blit(fuente.render(text, 0, (255, 255, 255)), (0,20))
		
		if(start == True):
			cut_points = []
			segments = []
			pos_enemy = []
			points = 0
			h_obj = Segment(pygame,surface,300,30,"./src/img/head.png","r")
			i_obj = Item(pygame,surface,0,0,"./src/img/target.png")
			i_obj.set_X(random.randint(0+50,500-50))
			i_obj.set_Y(random.randint(0+50,500-50))
			segments.append(Segment(pygame,surface,270,30,"./src/img/seg.png","r"))
			segments.append(Segment(pygame,surface,240,30,"./src/img/seg.png","r"))
			start = False
			fail = False
			text = ""
			
			for e in range(5):
				enemy = Enemy(pygame,surface,random.randint(0+50,500-50),random.randint(0+50,500-50),"./src/img/enemy.png")
				pos_enemy.append(enemy)
			
			
		for event in pygame.event.get():
			if(event.type==pygame.QUIT):
				gameExit=True
							
			if(event.type==pygame.KEYUP):			
				if(event.key == pygame.K_UP):
					h_obj.set_direction("u")
					cut_points.append([(h_obj.get_X(),h_obj.get_Y()),"u"])
				if(event.key == pygame.K_DOWN):
					h_obj.set_direction("d")
					cut_points.append([(h_obj.get_X(),h_obj.get_Y()),"d"])
				if(event.key == pygame.K_RIGHT):
					h_obj.set_direction("r")
					cut_points.append([(h_obj.get_X(),h_obj.get_Y()),"r"])
				if(event.key == pygame.K_LEFT):
					h_obj.set_direction("l")
					cut_points.append([(h_obj.get_X(),h_obj.get_Y()),"l"])
					
				if(event.key == pygame.K_SPACE):
					start = True
					
			'''
			if event.type == pygame.MOUSEBUTTONDOWN:
				if(pygame.mouse.get_pressed()[0]):
					posX, posY = event.pos
					if h_obj.get_rect().collidepoint(posX, posY):
						print('clicked on image')
			'''	
		if(fail == False):
			set_pos(h_obj)
			h_obj.render()
			i_obj.set_pos([segments[-1].get_X(),segments[-1].get_Y()])
			
			if(colicion(segments[-1],i_obj)):
				if(len(segments) > 1):
					segments.pop()
					i_obj.set_pos([random.randint(0+50,500-50),random.randint(0+50,500-50)])
					points -= 1
					
			i_obj.render()
					
			for e in pos_enemy:
				e.render()
				if(colicion(h_obj,e)):
					fail = True
			
			for s in segments:
				if(len(cut_points) > 0):
					for c in cut_points:
						#print(cut_points[0],s.get_X(),s.get_Y())
						if(s.get_X() == c[0][0] and s.get_Y() == c[0][1]):
							s.set_direction(c[1][0])
							if(segments.index(s) == len(segments)-1):
								cut_points.remove(c)
				set_pos(s)
				s.render()
				check_fail(segments,s,h_obj)
				
			add_segment(pygame,surface,i_obj,h_obj,segments)
		else:
			for s in segments:
				s.set_direction(random.choice(["d","u","l","r"]))
				set_pos(s)
				s.render()
				text = "GAME OVER"
		
		pygame.display.update()
pg = verificar_paquete()
gameLoop(pg)

