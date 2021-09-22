import pygame
from tkinter import *
from tkinter import ttk
from tkinter import font
from pygame.locals import *
import sys
import math
from PIL import Image
pygame.init()
pygame.font.init()
fuente = pygame.font.Font(None, 30)

class Angulo:
	def __init__(self):
		self.a=0
		self.b=0
	def setA(self,dat):
		self.a=dat
	def getA(self):
		return self.a
	def setB(self,dat):
		self.b=dat
	def getB(self):
		return self.b

an=Angulo()

def tk():
	global texto,inp,chequeo,rbt,t,lis
	win=Tk()
	win.title("Entrada de Datos")
	win.resizable("FALSE","FALSE")
	#Info colores http://wiki.tcl.tk/16166
	win.config(bg="white") # Le da color al fondo
	win.geometry("340x185")
	#"flat" (default), "raised", "sunken", "solid", "ridge", or "groove".
	vp=Frame(win,borderwidth=5, relief="ridge", width=300, height=300)
	vp.grid(column=0,row=0,padx=(0,0),pady=(0,0))
	vp.columnconfigure(1,weight=2)
	vp.rowconfigure(0,weight=1)
	vp.config(bg="#D5D5D5")

	valor=IntVar()

	rbt=IntVar()
	s = ttk.Style()
	s.configure('TRadiobutton', background='blue' )

	f=font.Font(family='Helvetica', size=12, weight='bold')
	f1=font.Font(family='Helvetica', size=12, weight='bold')

	Radiobutton(vp,text="Hielo",activebackground="#25B1FF", font=f, variable=rbt, value=1).grid(column=0,row=0,sticky=(W))
	Radiobutton(vp,text="Benceno",activebackground="#BDD400", font=f, variable=rbt, value=2).grid(column=0,row=1,sticky=(W))
	Radiobutton(vp,text="Esmeralda",activebackground="#3CCD00", font=f, variable=rbt, value=3).grid(column=0,row=2,sticky=(W))
	Label(vp,text="Grados Insidencia: ",font=f1,padx=10,pady=1,fg="black").grid(column=0,row=3,sticky=(W))
	inp=Entry(vp,width=10,textvariable=valor,font=f)
	inp.grid(column=0,row=4,sticky=(W))

	dx1=0
	dx2=0
	obj=Angulo()

	def inic():
		nb=0
		if(rbt.get()==1):
			nb=1.31
		if(rbt.get()==2):
			nb=1.50
		if(rbt.get()==3):
			nb=1.58

		ang=float(valor.get())

		c=(3*10**8)
		#nb=(rbt.get())
		senb=math.sin(((1.0*math.sin(ang*(math.pi/180)))/nb)*(math.pi/180))
		b=(1/(senb))
		v1=(c/nb)
		if((200*math.sin(b*(math.pi/180)))<0):
			db=(200*math.sin(b*(math.pi/180)))*-1
		else:
			db=(200*math.sin(b*(math.pi/180)))

		obj.setA(200*math.sin(ang*(math.pi/180)))
		obj.setB(db)
		print(obj.getB())
		vp.config(bg="#D5D5D5")
		Label(vp,text="Ang. Refraccion:",font=f1,padx=10,pady=1,fg="black",bg="white").grid(column=1,row=0,sticky=(W))
		Label(vp,text=b,padx=10,pady=1,font=f1,fg="black",bg="white").grid(column=1,row=1,sticky=(W))
		Label(vp,text="Velocidad en medio: ",font=f1,padx=10,pady=1,fg="black",bg="white").grid(column=1,row=2,sticky=(W))
		Label(vp,text=v1,padx=10,pady=1,font=f1,fg="black",bg="white").grid(column=1,row=3,sticky=(W))

		gameLoop(obj,rbt.get())
		pygame.quit()


	Button(vp,text="Simular",bg='#81A7BE',font=f,command=inic,activebackground="#F50743",borderwidth=3,compound="right").grid(column=1,row=4,sticky=(W))

	win.mainloop()


def gameLoop(obj,m):
	dx1=obj.getA()
	dx2=obj.getB()
	gameExit = False

	gameExit = False
	clock = pygame.time.Clock()
	superficie=pygame.display.set_mode((500,600))#Crea el fondo
	pygame.display.set_caption('Simulacion')

	cx=250
	cx1=250
	while not gameExit:
		clock.tick(60)

		superficie.fill((255, 255, 255))
		if(cx>=250-dx1):
			cx-=1

		if(cx1<=250+dx2):
			cx1+=1
			print(cx1,"-",cx1)

		if(m==1):
			pygame.draw.rect(superficie, (37,177,255), [0, 300, 500, 600])
		elif(m==2):
			pygame.draw.rect(superficie, (189,212,0), [0, 300, 500, 600])
		else:
			pygame.draw.rect(superficie, (60,205,0), [0, 300, 500, 600])

		pygame.draw.line(superficie, (0, 0, 0), (250, 0), (250, 600), 3)
		pygame.draw.line(superficie, (228, 2, 2),(250,300) , (cx, 0), 7)
		pygame.draw.line(superficie, (0, 42, 2), (250, 300), (cx1, 600), 7)
		tex=(dx1,"-",dx2)
		#superficie.blit(fuente.render(str(tex) , 0, (0, 0, 0)), (0,0))
		pygame.display.update()
		superficie.fill((0,0,0))
		for event in pygame.event.get():
			if(event.type==pygame.QUIT):
				gameExit=True
	pygame.quit()

def ini(ang):

	dy=200*math.cos(ang*(math.pi/180))
	dx=200*math.sin(ang*(math.pi/180))
	print(dy,"-",dx)
	gameLoop(dx,(dy))
	pygame.quit()
	quit()

print(math.sin(90*(math.pi/180)))
print(1/math.sin(90*(math.pi/180)))
#gameLoop(20,20)
tk()

#ini(ang)
