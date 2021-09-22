import random
import time
import os

class Personaje():
	
	def __init__(self,pvO=None,nom=None,pv=None,ma=None,hab=[],pHab=[],est=None):
		self.pv=pv
		self.ma=ma
		self.hab=hab
		self.pHab=pHab
		self.est=est
		self.nom=nom
		self.pvO=pvO
		self.punt=0;
		
	def setPunt(self,punt):
		self.punt=punt
	def getPunt(self):
		return self.punt
		
	def setPvO(self,pvO):
		self.pvO=pvO
	def getPVO(self):
		return self.pvO
		
	def getPvO(self):
		return self.pvO
	
	def getNom(self):
		return self.nom
	def setNom(self,nom):
		self.nom=nom
	
	def getPv(self):
		return self.pv
	def setPv(self,pv):
		self.pv=pv
		
	def getHab(self):
		return self.hab
	def setHab(self,hab=[]):
		self.hab=hab
		
	def getPHab(self):
		return self.pHab
	def setPHab(self,pHab=[]):
		self.pHab=pHab
	
	def getMa(self):
		return self.ma
	def setMa(self,ma):
		self.ma=ma
		
	def getEst(self):
		return self.est
	def setEst(self,est=[]):
		self.est=est
		
class Enemigo():
	
	def __init__(self,nom=None,pv=None,punt=None,hab=[],pHab=[],est=None):
		self.pv=pv
		self.hab=hab
		self.pHab=pHab
		self.est=est
		self.nom=nom
		self.punt=punt
	
	def getPunt(self):
		return self.punt
	def setPunt(self,punt):
		self.nom=punt
	
	def getNom(self):
		return self.nom
	def setNom(self,nom):
		self.nom=nom
	
	def getPv(self):
		return self.pv
	def setPv(self,pv):
		self.pv=pv
		
	def getHab(self):
		return self.hab
	def setHab(self,hab=[]):
		self.hab=hab
		
	def getPHab(self):
		return self.pHab
	def setPHab(self,pHab=[]):
		self.pHab=pHab
		
	def getEst(self):
		return self.est
	def setEst(self,est=[]):
		self.est=est

def ver(lpj,ini,afe):
	for i in range(len(lpj)):
		if(lpj[i].getEst()=="Estable"):
			
			if(ini==True and afe==i):
				print(chr(27)+"[0;31m",i+1,lpj[i].getNom(),"PV: (",lpj[i].getPv(),"/",lpj[i].getPvO(),") ","PM: (",lpj[i].getMa(),")",lpj[i].getEst())
			else:
				print(chr(27)+"[1;32m",i+1,lpj[i].getNom(),"PV: (",lpj[i].getPv(),"/",lpj[i].getPvO(),") ","PM: (",lpj[i].getMa(),")",lpj[i].getEst())
		elif(lpj[i].getEst()=="Ciego"):
			print(chr(27)+"[0;36m",i+1,lpj[i].getNom(),"PV: (",lpj[i].getPv(),"/",lpj[i].getPvO(),") ","PM: (",lpj[i].getMa(),")",lpj[i].getEst())
		elif(lpj[i].getEst()=="Camuflado" or lpj[i].getEst()=="Protegido" or lpj[i].getEst()=="Defensa"):
			print(chr(27)+"[1;33m",i+1,lpj[i].getNom(),"PV: (",lpj[i].getPv(),"/",lpj[i].getPvO(),") ","PM: (",lpj[i].getMa(),")",lpj[i].getEst())
		else:
			print(chr(27)+"[0;31m",i+1,lpj[i].getNom(),"PV: (",lpj[i].getPv(),"/",lpj[i].getPvO(),") ","PM: (",lpj[i].getMa(),")",lpj[i].getEst())
	print(chr(27)+"[0m")

def CrearPj():
	lpj=[]
	lpj.append(Personaje(2500,"Gerrero",2500,0,["Ataque","Furia","Escudo","Defenderse"],[10,15],"Estable"))
	lpj.append(Personaje(1500,"Picaro",1500,0,["Ataque","Asesino","Camuflar","Defenderse"],[8,15,True],"Estable"))
	lpj.append(Personaje(800,"Brujo",800,100,["Ataque","Necro","Maldicion","Defenderse"],[3,12,6],"Estable"))
	lpj.append(Personaje(850,"Sacerdotisa",850,100,["Ataque","Cura Masiva","Curar","Defenderse"],[5,15,100],"Estable"))
	return lpj;
	
def CrearEne():
	lpe=[]
	cant=random.randint(1,5)
	
	for i in range(cant):
		tip=random.randint(1,5)
		
		if(tip==1):
			lpe.append(Enemigo("Duende",19,10,["Ataque","Falla"],[19,0],"Vivo"))
		elif(tip==2):
			lpe.append(Enemigo("Araña",52,31,["Ataque","Falla","Veneno"],[13,0,10],"Vivo"))
		elif(tip==3):
			lpe.append(Enemigo("Lilith",300,150,["Magia","Ataque","Cegera"],[46,10,0],"Vivo"))
		elif(tip==4):
			lpe.append(Enemigo("Vampireza",270,195,["Magia","Ataque","Cegera"],[38,21],"Vivo"))
		else:
			lpe.append(Enemigo("Quimera",350,300,["Magia","Ataque","Tormenta"],[42,30,15,0],"Vivo"))

	return lpe;

def vPV(cons,act,var):
	tot=0
	if(cons>act):
		tot=(cons-act)
		if(tot>var):
			tot=var
	return tot

def validarEntrada(limite,mensaje):
	while(True):
		entrada=int(input(mensaje))
		print(entrada,limite+1)
		if(entrada<limite+1):
			return entrada
		else:
			print("Entrada incorrecta!")
		
def barra(actual,total):
	pass
	

def Arena(tip,liA,liD,nA,nD,nH):
	add=0
		
	if(tip==1):
	
		if(liA[nA].getEst()!="Ciego"):
		
			print("Antes:",liD[nD].getPv())
			
			if(liA[nA].getHab()[nH]=="Ataque"):
				if(liD[nD].getEst()=="Maldito"):
					add=20;
				else:
					add=0;
			
				liD[nD].setPv(liD[nD].getPv()-(liA[nA].getPHab()[nH]+add))
				print("Puntos de daño: ",liA[nA].getPHab()[nH]+add)
				liA[0].setPunt(liA[0].getPunt()+(liA[nA].getPHab()[nH]+add))
				add=0;
				
			if(liA[nA].getHab()[nH]=="Asesino"):
				if(liD[nD].getEst()=="Maldito"):
					add=20;
				else:
					add=0;
				liD[nD].setPv(liD[nD].getPv()-(liA[nA].getPHab()[nH]+add))
				print("Puntos de daño: ",liA[nA].getPHab()[nH]+add)
				liA[0].setPunt(liA[0].getPunt()+(liA[nA].getPHab()[nH]+add))
				add=0;
				
			if(liA[nA].getHab()[nH]=="Furia"):
				liA[nA].setPv(liA[nA].getPv()-10)
				for i in range(len(liD)):
					liD[i].setPv(liD[i].getPv()-(liA[nA].getPHab()[nH]/len(liD)))
					print("Puntos de daño: ",liA[nA].getPHab()[nH]/len(liD))
					liA[0].setPunt(liA[0].getPunt()+(liA[nA].getPHab()[nH]*len(liD)))
			
			if(liA[nA].getHab()[nH]=="Camuflar"):
				liA[nA].setEst("Camuflado")
				

			
			if(liA[nA].getHab()[nH]=="Maldicion"):
				if(liA[nA].getMa()>=10):
					liD[nD].setEst("Maldito")
					liA[nA].setMa(liA[nA].getMa()-10)
				else:
					liD[nD].setPv(liD[nD].getPv()-(liA[nA].getPHab()[nH]+add))
					
			if(liA[nA].getHab()[nH]=="Escudo"):
				ver(liA,False,0)
				#cu=int(input("Proteger a: "))
				validarEntrada(len(liA),"Proteger a: ")
				
				liA[cu-1].setEst("Protegido")
				
			if(liA[nA].getHab()[nH]=="Necro"):
				if(liA[nA].getMa()>=15):
					liA[nA].setMa(liA[nA].getMa()-15)
					for i in range(len(liD)):
						liD[i].setPv(liD[i].getPv()-50)
				else:
					liD[nD].setPv(liD[nD].getPv()-(liA[nA].getPHab()[nH]+add))
					print("Puntos de daño: ",liA[nA].getPHab()[nH]+add)
					
			if(liA[nA].getHab()[nH]=="Cura Masiva"):
				if(liA[nA].getMa()>=20):
					liA[nA].setMa(liA[nA].getMa()-20)
					
					for i in range(len(liA)):
						print("Para",liA[i].getNom(),": ")
						print("Puntos de salud: ",vPV(liA[i].getPvO(),liA[i].getPv(),50),"+")
						liA[i].setPv(liA[i].getPv()+vPV(liA[i].getPvO(),liA[i].getPv(),50))

				else:
					liD[nD].setPv(liD[nD].getPv()-(liA[nA].getPHab()[nH]+add))
					
			if(liA[nA].getHab()[nH]=="Curar"):
				if(liA[nA].getMa()>=15):
					liA[nA].setMa(liA[nA].getMa()-15)
					ver(liA,False,0)
					#cu=int(input("Curar a: "))
					cu=validarEntrada(len(liA),"Curar a: ")
					print("Puntos de salud:",liA[cu-1].getPv()+vPV(liA[cu-1].getPvO(),liA[cu-1].getPv(),70),"+")
					liA[cu-1].setPv(liA[cu-1].getPv()+vPV(liA[cu-1].getPvO(),liA[cu-1].getPv(),70))
					if(liA[cu-1].getEst()=="Ciego"):
						liA[cu-1].setEst("Estable")
					
				else:
					liD[nD].setPv(liD[nD].getPv()-(liA[nA].getPHab()[nH]+add))
			print("Despues:",liD[nD].getPv())
		else:	
			print("Personaje Ciego!!!")
			
			
		if(liA[nA].getHab()[nH]=="Defenderse"):
			liA[nA].setEst("Defensa")
			
		if(liA[nA].getEst()=="Envenenado"):
			liA[nA].setPv(liA[nA].getPv()-10)
			print("Veneno: -10")

	if(tip==2):
			
		if(liA[nA].getHab()[nH]=="Ataque" or liA[nA].getHab()[nH]=="Magia"):
			if(liD[nD].getEst()!="Camuflado"):
				if(liD[nD].getEst()=="Protegido"):
					liD[nD].setPv(int(liD[nD].getPv()-(liA[nA].getPHab()[nH]/2)))
					liD[nD].setEst("Estable")
				elif(liD[nD].getEst()=="Defensa"):
					liD[nD].setPv(int(liD[nD].getPv()-(liA[nA].getPHab()[nH]/3)))
					liD[nD].setEst("Estable")
				else:
					liD[nD].setPv(liD[nD].getPv()-(liA[nA].getPHab()[nH]+add))
			else:
				liD[nD].setEst("Estable")

		if(liA[nA].getHab()[nH]=="Cegera"):
			liD[nD].setEst("Ciego")
			
		if(liA[nA].getHab()[nH]=="Veneno"):
			liD[nD].setEst("Envenenado")
			
		if(liA[nA].getHab()[nH]=="Tormenta"):
			for i in range(len(liD)):
				liD[i].setPv(liD[i].getPv()-20)
		
def gameLoop(titulo):
	
	for i in titulo:
		#time.sleep(0.5)
		print (chr(27)+i+chr(27)+"[0m")
	
	print (chr(27)+"[1;36m"+"PyRPG BY CDCB"+chr(27)+"[0m","\n")
	lpj=CrearPj()
	nPe=0
	pos=1
	et=1
	
	while(True):

		if(nPe==4):
			print("HAS PERDIDO!!!!!!")
			print("PUNTAJE FINAL:",lpj[0].getPunt())
			break
		else:
			lpe=CrearEne()
			optPj=-1
			optEne=-1
			nMu=0
			caE=len(lpe)
			afe=0
			ini=False
			
		for i in range(len(lpj)):
			lpj[i].setEst("Estable")

		while(nMu!=caE and nPe!=4):
			ver(lpj,ini,afe)
			
			optPj+=1
			if(optPj>=len(lpj)):
				optPj=0

			print("PUNTAJE:",lpj[0].getPunt())
			print("POCIONES:",pos)
			print("ETER:",et)
			print("--------------------",chr(27)+"[0m")
			
			for i in range(len(lpe)):
				if(lpe[i].getEst()=="Vivo"):
					print(chr(27)+"[1;31m",i+1,lpe[i].getNom()," ",lpe[i].getEst())
				else:
					print(chr(27)+"[0;31m",i+1,lpe[i].getNom()," ",lpe[i].getEst(),chr(27)+"[0m")
				
			#selE=int(input(lpj[optPj].getNom()+"----->Enemigo: ",))
			selE=validarEntrada(len(lpe),str(lpj[optPj].getNom()+"----->Enemigo: "))
			
			print("--------------------",chr(27)+"[0m")
			
			if(selE>=len(lpe)):
				selE=len(lpe)-1

			for i in range(len(lpj[optPj].getHab())):
				print(i+1,lpj[optPj].getHab()[i])
			
			if(pos>0 or et>0):
				print("0 Usar")
			
			#selA=int(input(" Habilidad: "))
			selA=validarEntrada(len(lpj[optPj].getHab())," Habilidad: ")
			
			os.system('clear')
			os.system('cls')
			
			if(selA==0):
				if(pos>0):
					print("1- Pociones: ",pos)
				if(et>0):
					print("2- Eter: ",et)
				if(pos>0 or et>0):
					#ob=int(input(" Objeto: "))
					ob=validarEntrada(2," Objeto: ")
					
					if(ob==1):
						ver(lpj,ini,afe)
						#pjP=int(input("  Curar a: "))
						pjP=validarEntrada(len(lpj),"  Curar a: ")
						lpj[pjP-1].setPv(lpj[pjP-1].getPv()+vPV(lpj[pjP-1].getPvO(),lpj[pjP-1].getPv(),100))
						pos-=1
						if(lpj[pjP-1].getEst()=="Ciego" or lpj[pjP-1].getEst()=="Envenenado"):
							lpj[pjP-1].setEst("Estable")
					if(ob==2):
						ver(lpj,ini,afe)
						#pjP=int(input("  Poner Mana a: "))
						pjP=validarEntrada(len(lpj),"  Poner Mana a: ")
						lpj[pjP-1].setMa(lpj[pjP-1].getMa()+60)
						et-=1
			else:
				Arena(1,lpj,lpe,optPj,(selE-1),(selA-1))
				time.sleep(2)

			if(lpe[selE-1].getPv()<0):
				lpj[0].setPunt(lpj[0].getPunt()+lpe[selE-1].getPunt())
				lpe[selE-1].setEst("Muerto")
				nMu+=1
				del lpe[selE-1]	
				print("Muertes: ",nMu)
			
			if(nMu==caE):
				print("\n",chr(27)+"[1;33m","<<<<Has ganado el combate>>>>")
				tes=random.randint(0,1)
				if(tes==0):
					pos+=1
					print("Has obtenido una Pocion!",chr(27)+"[0m")
				else:
					et+=1
					print("Has obtenido Un Eter!",chr(27)+"[0m","\n")
				break
				
			optEne+=1
			if(optEne>=len(lpe)):
				optEne=0
				
			habE=random.randint(0,len(lpe[optEne].getHab()))

			
			while(True):
				perAt=random.randint(0,3)
				if(lpj[perAt].getEst()!="Muerto"):
					break

			for i in range(5):
				cad=""
				os.system('clear')
				for j in range(i):
					cad+="-"
					
				print(chr(27)+"[33m","\n")
				print("++++++++++++++++++++++")
				print(lpe[optEne].getHab()[habE-1])
				print(lpe[optEne].getNom(),cad,">")
				time.sleep(0.5)
				
			os.system('clear')
			print(lpe[optEne].getNom(),"---->",lpj[perAt].getNom(),"-"+str(lpe[optEne].getPHab()[habE-1]))
			print("++++++++++++++++++++++",chr(27)+"[0m","\n")
			time.sleep(1)
			
			Arena(2,lpe,lpj,optEne,perAt,habE-1)
			afe=perAt
			ini=True
			
			if(lpj[perAt].getPv()<0):
				lpj[perAt].setEst("Muerto")
				print(chr(27)+"[0;31m"+"Ha muerto: ",lpj[perAt].getNom()+chr(27)+"[0m")
				del lpj[perAt]
				nPe+=1
				

titulo=[]

titulo.append("     ▄███████▄ ▄██   ▄      ▄████████    ▄███████▄    ▄██████▄  ")
titulo.append("    ███    ███ ███   ██▄   ███    ███   ███    ███   ███    ███ ")
titulo.append("    ███    ███ ███▄▄▄███   ███    ███   ███    ███   ███    █▀  ")
titulo.append("    ███    ███ ▀▀▀▀▀▀███  ▄███▄▄▄▄██▀   ███    ███  ▄███        ")
titulo.append("  ▀█████████▀  ▄██   ███ ▀▀███▀▀▀▀▀   ▀█████████▀  ▀▀███ ████▄  ")
titulo.append("    ███        ███   ███ ▀███████████   ███          ███    ███ ")
titulo.append("    ███        ███   ███   ███    ███   ███          ███    ███ ")
titulo.append("   ▄████▀       ▀█████▀    ███    ███  ▄████▀        ████████▀  ")
titulo.append("                           ███    ███                          ")
titulo.append("   ▄█████████████████████  ▀█▀    ▀█▀ █████████████████████████▄")


gameLoop(titulo)
