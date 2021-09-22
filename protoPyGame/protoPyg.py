#https://www.pythonmania.net/es/2010/03/23/tutorial-pygame-introduccion/
import pygame
import random
import threading
import time
from tkinter import *

pygame.init()

class Cuadrado:
	
	def __init__(self, x, y, lado, color, fondo):
		self.x = x
		self.y = y
		self.color = color
		self.fondo = fondo
		self.lado = lado
		self.rect = pygame.Rect(self.x,self.y,self.lado,self.lado)    
	
	def getY(self):
		return self.y
		
	def setY(self,y):
		self.y=y
	def setX(x):
		self.x=x
	def getRect(self):
		return self.rect
	def getX(self):
		return self.x
		
	def pinta(self):
		pygame.draw.rect(self.fondo,self.color,[self.x,self.y,50,50])
		
		
class Personaje:
	
	def __init__(self,x,y,s,r):
		#pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(r)
		self.rect = self.image.get_rect()
		self.rect.top = y
		self.rect.left = x
		self.speed = 0.5 
		self.s=s   
	
	def getY(self):
		return self.rect.top
	def setY(self,y):
		self.rect.top=y
	def setX(self,x):
		self.rect.left=x
	def getX(self):
		return self.rect.left
	def getRect(self):
		return self.rect
	def setRect(self,r):
		self.rect=r
	def getImg(self):
		return self.image
	def setImg(self,i):
		self.image=i
	
		
	def pinta(self):
		self.s.blit(self.image, self.rect)


def rePaint():
	pygame.display.update()#Actualiza fincion especifica

def colicion(obj1,obj2):
	return obj1.colliderect(obj2)

def gameLoop():
	#background_image = load_image('images/fondo_pong.png')

	x=300
	xc=0
	y=300
	yc=0
	gameExit = False
	al = random.randint(10,30)
	clock = pygame.time.Clock()
	superficie=pygame.display.set_mode((800,600))#Crea el fondo
	random.randint(10,30)
	pygame.display.set_caption('ProtoGamePy')
	superficie.fill((0,0,0))#color del fondo RGB
	sonido = pygame.mixer.Sound("pun1.wav")
	fuente = pygame.font.Font(None, 30)
	texto1 = fuente.render("Pruebas PyGame", 0, (255, 255, 255))
	lista=[]
	lista.append(Cuadrado(50,50,100,(255,0,255),superficie))

	while not gameExit:
		
		clock.tick(60)
		x+=xc
		y+=yc
		superficie.fill((0,0,0))
		
		#pygame.draw.circle(superficie,(0,0,255),[x,y],50,0)
		
		per=Personaje(0,0,superficie,"per.png")
		
		per.setY(y)
		per.setX(x)
		
		superficie.blit(per.getImg(),per.getRect())
		superficie.blit(texto1, (0,0))
		#re=pygame.Rect(x,y,50,50)#Se ubica un cuadrado en el circulo

		if(x>=800):
			yc=-10
			xc=-10
		elif(x<=0):
			xc=10
			yc=10
		elif(y<=0):
			xc=-10
			yc=+10
		elif(y>=600):
			xc=10
			yc=-10
		
		for i in range(len(lista)):
			lista[i].pinta()
			
		for i in range(len(lista)):
			lista[i].setY(lista[i].getY()+1)
			for a in range(len(lista)):
				if(colicion(per.getRect(),lista[a].getRect())):
					sonido.play()
					#lista[a].color=(255,0,0)
					lista[a].setY(lista[a].getY()-10)
		
		for event in pygame.event.get():
			if(event.type==pygame.QUIT):
				gameExit=True
			#print(pygame.mouse.get_pos())

			#Dibuja cuadrado en la superficie con color X,Y,W,H
			if(event.type==pygame.MOUSEBUTTONDOWN):
				if(pygame.mouse.get_pressed()[0]):
					lista.append(Personaje(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],superficie,"s.png"))
					#lista.append(Cuadrado(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],100,(255,0,255),superficie))

			#Dibuja circulo en la superficie con color X,Y,R,F		
			if(event.type==pygame.KEYDOWN):
				if(event.key==pygame.K_SPACE):
					pygame.draw.circle(superficie,(255,0,0),[x,y],100,50)
					
				if(event.key==pygame.K_RIGHT):
					xc=10
					yc=10
					
				elif(event.key==pygame.K_LEFT):
					xc=-10
					yc=-10
			
			if(event.type==pygame.KEYUP):
				if(event.key==pygame.K_SPACE):
					pygame.draw.circle(superficie,(255,0,0),[x,y],100,50)
					
				if(event.key==pygame.K_RIGHT):
					xc=0
					yc=0
					
				elif(event.key==pygame.K_LEFT):
					xc=0
					yc=0
			
			#if(event.type==pygame.MOUSEMOTION):
				#x=pygame.mouse.get_pos()[0]
				#y=pygame.mouse.get_pos()[1]
			
			
		rePaint()
		
		
		
		
def hilo():
	for i in range(10):
		time.sleep(3)
		print(i)
	
def shilo():
	for i in range(10):
		print(i-1)
		
hilo2 = threading.Thread(target=shilo)
hilo1 = threading.Thread(target=hilo)
hilo1.start()
hilo2.start()

gameLoop()


pygame.quit()
quit()


