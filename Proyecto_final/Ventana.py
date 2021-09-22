import pygame
from Motor import Motor
from tkinter import *
from pygame.locals import *


class Ventana:
	
	def __init__(self):
		pygame.init()
		
		"Objetos"
		# Objeto que contiene la simulacion y grafica
		self.motor = Motor()
		# Reloj de pygame, usado para mantener el framerate
		self.clock = pygame.time.Clock()
		# Ventana del pygame
		self.ventana = pygame.display.set_mode((1250, 650))
		
		# Para saber que pygame se esta usando
		print(pygame.version.ver)
		
		"Metodos"
		# Pone titulo a la ventana
		pygame.display.set_caption("Proyecto grafos-Juan Pablo Pulgarin-Cristian David Cruz")
		# Hace el loop del programa(Si necesita agregar hilos o alguna otra cosa me dice)
		self.loop()
		
	def loop(self):
		"""Hace el loop del programa cada 1/60 segundos"""
		while True:
			self.eventos()				# Activa los eventos segun los cambios en el teclado/mouse/progama
			self.motor.metodos(self.ventana)		# Llama a los metodos del motor
			# self.dibuja_fps()			# Dibuja los FPS del programa(Para pruebas, luego borrar)
			pygame.display.update()		# Actualiza la graficacion del pygame
			
			#print("fps:"+str(round(self.clock.get_fps())))
			self.clock.tick(60)			# Fuerza al loop a que se haga cada 1/60 segundos
	
	def eventos(self):
		"""Activa los eventos segun los cambios en el teclado/mouse/progama"""
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
				
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q: self.motor.eventos_menu("q")
				if event.key == pygame.K_LEFT:self.motor.eventos_menu("izq")
				if event.key == pygame.K_RIGHT:self.motor.eventos_menu("der")
				if event.key == pygame.K_x: self.motor.eventos_menu("x")
				if event.key == pygame.K_z: self.motor.eventos_menu("z")
				
		#Llama a los eventos por teclado
		self.motor.evento_teclado()
	
	def dibuja_fps(self):
		"""Dibuja fps del programa"""
		self.ventana.blit(self.dibuja_font("FPS:" + str(round(self.clock.get_fps()))), (0, 0))
	
	def dibuja_font(self, text):
		"""Dibuja la fuente del programa"""
		return pygame.font.Font('freesansbold.ttf', 15).render(text, True, (0, 0, 0))


