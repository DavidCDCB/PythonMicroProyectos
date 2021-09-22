#! /usr/bin/python3
import random
import os
ind=[]

def crearM(f,c):
	m=[[None] * c for i in range(f)]
	return m

def genInd(ind):
	rep=False
	while(True):
		rep=False
		opt=random.randint(0,5)
		if(len(ind)==0):ind.append(opt)
		else:
			for i in range(len(ind)):
				if(ind[i]==opt):
					rep=True
					break

			if(rep==False):
				ind.append(opt)
		if(len(ind)==6):break
	return ind;

def bin(arr):
	narr=[0 for i in range(len(arr))]#Creacion de lista con datos predefinidos

	cont=0
	for i in range(len(arr)):
		if(cont<3): narr[arr[i]]=0
		else: narr[arr[i]]=1
		cont=cont+1
	return narr

def conse(arr):
	con=False
	for i in range(len(arr)):
		if(i+1 < len(arr) and i+2 < len(arr)):
			if((arr[i]==arr[i+1] and arr[i]==arr[i+2]) and arr[i]!=None):
				con=True
				break
	return con

def verC(arr):
	band=False
	cont=0
	for i in range(len(arr)):
		if(arr[i]==1):cont=cont+1
	if(cont!=len(arr)/2):band=True
	return band

def verM(m):
	cad=""
	lin=""
	for i in range(len(m)+1):
		if(i<len(m)):lin+="-+"
		else: lin+="-"
	for i in range(len(m)):
		for j in range(len(m[0])):
			cad=cad+str(m[i][j])+"|"
		print(lin)
		print(cad)
		cad=""
	print(lin)

def filRep(M):
	rep=False
	opt=[]
	for i in range(len(M)):
		if(M[i][0]!=None):
			opt=[]
			for j in range(len(M[0])):
				opt.append(M[i][j])
			if(compF(M,opt,i)==True):
				rep=True
				break

	return rep

def compF(M,opt,nf):
	nSim=0
	rep=False
	for i in range(len(M)):
		nSim=0
		for j in range(len(M[0])):
			if(M[i][j]==opt[j] and i!=nf):nSim=nSim+1
		if(nSim==6):
			rep=True
			break
	return rep

def colRep(M):
	rep=False
	opt=[]
	for i in range(len(M[0])):
		if(M[0][i]!=None):
			opt=[]
			for j in range(len(M)):
				opt.append(M[j][i])
			#verA(opt)
			if(compC(M,opt,i)==True):
				rep=True
				break

	return rep

def compC(M,opt,nf):
	nSim=0
	rep=False
	for i in range(len(M[0])):
		nSim=0
		for j in range(len(M)):
			if(M[j][i]==opt[j] and i!=nf):nSim=nSim+1
		if(nSim==6):
			rep=True
			break
	return rep



def verA(arr):
	cad=""
	for j in range(len(arr)):
		cad=cad+str(arr[j])+"-";
	print(cad)

def rec(M,cont):
	recur=True

	while(recur==True):
		conV=False
		if(cont==len(M)):
			return False
		else:
			while(True):
				arre=bin(genInd([]))
				if(conse(arre)==False):break

			for j in range(len(M[0])):
				M[cont][j]=arre[j]

			arr1=[]
			#rep=False
			for i in range(len(M[0])):
				arr1=[]
				for j in range(len(M)):
					arr1.append(M[j][i])
				if(conse(arr1)==True):
					#verM(M)
					conV=True

			if(conV==False):
				recur=rec(M,cont+1)
	return

M=crearM(6,6)

def sol(M):
	cont=0
	while(True):
		arr2=[]
		band=False

		rec(M,0)

		for i in range(len(M[0])):
			arr2=[]
			for j in range(len(M)):
				arr2.append(M[j][i])

			if(verC(arr2)==True):
				band=True

		#verM(M)
		cont=cont+1
		if(colRep(M)==False and filRep(M)==False and band==False):break
	#print("Intentos: ",cont)
	return M;


def opts(M1,lM):
	nSol=0
	rep=False
	if(len(lM)==0):
		lM.append(M)
	else:
		for i in range(len(lM)):
			#print(i)
			verM(lM[i])
			verM(M1)
			if(M1==lM[i]):
				rep=True
				print("---------------------")
				#verM(lM[i])
				#verM(M)
			else:
				rep=False
				break
	return rep


def compM(m1,m2):
	sim=0
	band=False

	for i in range(len(m1)):
		for j in range(len(m1[0])):
			if(m1[i][j]==m2[i][j]):sim=sim+1
	if(sim==36):
		band=True
	return band

indice=0
lM=[]
lMp=[]
nSol=0
nRep=0

while(True):
	
	#print(i)
	opt=sol(crearM(6,6))
	
	dif=False
	ndif=0

	if(len(lM)==0):
		nSol=nSol+1
		lM.append(opt)
	else:
		os.system('clear')
		if(not opt in lM):
			lM.append(opt)
			verM(opt)
			print(genInd([]))
			input()
			print(len(lM))
			nRep=0
		else: 
			nRep+=1
			print(nRep)
	
	if(nRep==len(lM)):break
print(nSol)
