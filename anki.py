import os

def insercion(aLista,archivoR):
	for l in aLista:
		if(l[len(l)-1] is "\n"):
			archivoR.write(l)
		else:
			archivoR.write(l+"\n")
	archivoR.close()


def seleccion():
	archivo = open("mochos.txt", "r")
	aLista = archivo.readlines()
	archivo.close()
	archivoR = open("mochos.txt", "w")

	can=aLista.pop(0)
	print("Canción: "+can.split('-')[0]+" con progreso de "+can.split('-')[1])
	
	np=input('Nuevo progreso de? ')

	os.system('clear')
	if(int(can.split('-')[1])>int(np)):
		print('UPS!!!')
	else:
		print('MUY BIEN!!!')

	can=can.split('-')[0]+"-"+np

	pos=(len(aLista)+1)*int(np)//100
	aLista.insert(pos,can)

	insercion(aLista,archivoR)

	inicio()


def ingreso():
	archivo = open("mochos.txt", "r")
	aLista = archivo.readlines()
	archivo.close()
	archivoR = open("mochos.txt", "w")

	while(True):
		n=input('Nombre de mocho: ')
		if(n is not 's'):
			p=input('Porcentaje:')			
			archivoR.write(n+"-"+p+"\n")

		else:
			insercion(aLista,archivoR)

			archivoR.close()
			os.system('clear')
			inicio()
			break

def vista():
	lTup=[]
	archivo = open("mochos.txt", "r")
	aLista = archivo.readlines()
	archivo.close()

	for c in aLista:
		lTup.append((c.split('-')[0],c.split('-')[1]))

	#la longitud del dato mas largo
	mE=len(max(lTup, key=lambda x: len(x[0]))[0])

	for co in sorted(lTup, key=lambda x: int(x[1].replace("\n", ""))):
		print("|"+str(co[0]).ljust(mE)+"|"+str(co[1][0:len(co[1])-1]+'%').ljust(4)+"|")

	inicio()


def inicio():
	print('\n╔══════════════════════════════════╗')
	print('║MÉTODO ANKI DE APRENDIZAJE MUSICAL║')
	print('╚══════════════════════════════════╝')
	print('\n1-Ingreso de canciones')
	print('2-Ensayo del dia')
	print('3-Listado de progreso')
	opt=input()

	if(opt is '1'):
		os.system('clear')
		ingreso()
		
	elif(opt is '2'):
		os.system('clear')
		seleccion()
	else:
		os.system('clear')
		vista()

inicio()
