import os
import time

corrimiento='''
	0 0 0 r 0
	0 1 0 r 1
	0 _ _ * !
	
	1 1 1 r 1
	1 0 1 r 0
	1 _ 1 r 2
	
	2 _ _ * !
	'''
	
limpieza='''
	0 * * r 0
	0 _ _ l 1
	
	1 0 * l 2
	1 1 * l 1
	
	2 0 * l 2
	2 1 0 r 3
	
	3 0 * r 3
	3 _ * l 4
	3 1 * l 4
	
	4 0 1 l 1
	
	2 _ * r 5
	
	5 0 _ r 5
	5 1 * * !
	'''
	
sumar3='''
	0 * * r 0
	0 _ _ l 1

	1 0 1 l 2
	1 1 0 l 3

	2 0 1 l 4
	2 1 0 l 5

	3 0 1 l 4
	3 1 * l 5

	4 * * l 6

	5 1 0 l 5
	5 0 1 l 6
	5 _ 1 l 7

	6 * * l 6
	6 _ _ * !
	
	7 _ _ * !
	'''
	
fuck='''
	0 _ * r 0
	0 | * l 1
	1 _ . r 2
	2 | * r 2
	2 _ . r 0
	0 X * r 3
	3 _ D * !
	'''

def MaquinaTuring(ltran,dInput):
	estadoActual=0
	posicion=1
	while estadoActual != "!":
		for t in ltran.split("\n\t"):
			if(t != "" and t.split(" ")[0] == str(estadoActual)):
				if((t.split(" ")[1] == dInput[posicion]) or t.split(" ")[1] == "*"):
						print("Estado Actual: q",estadoActual)
						
						print("".join(dInput))
						
						cad="^"
						for i in range(posicion):
							cad=" "+cad
						print(cad)
						
						if(t.split(" ")[2]!="*"):
							dInput[posicion]=t.split(" ")[2]
							
						print("Transicion:",t)
						print("".join(dInput))
						
						if(t.split(" ")[3]=="r"):
							posicion=posicion+1
							if(posicion>=len(dInput)):
								dInput.append("_")
							
						if(t.split(" ")[3]=="l"):
							posicion=posicion-1
							if(posicion<0):
								dInput.insert(0,"_")
								posicion=0
							
						if(t.split(" ")[4]!="!" and t.split(" ")[4]!="!\n"):
							estadoActual=int(t.split(" ")[4])
						else:
							estadoActual="!"
							
						cad="^"
						for i in range(posicion):
							cad=" "+cad
						print(cad)
						
						input()
						os.system('clear')
	return dInput
	
print("Resultado:","".join(MaquinaTuring(fuck,"_ _ | _ _ _ | _ _ X _".split(" "))))
print("Resultado:","".join(MaquinaTuring(limpieza,"_ 1 1 0 1 0 0 _".split(" "))))
print("Resultado:","".join(MaquinaTuring(sumar3,"_ 1 1 1 1 _".split(" "))))
print("Resultado:","".join(MaquinaTuring(corrimiento,"_ 1 1 0 1 _".split(" "))))
		
