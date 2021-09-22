#! /usr/bin/python3
import time
import random
import os
def crearM(f,c):
	m=[[0] * c for i in range(f)]
	return m
	
def verM(m):
	cad=""
	lin=""
	for i in range((len(m)*2)+1):
		lin+="-"
	print(lin)
	for i in range(len(m)):
		#print(m[i])
		for j in range(len(m[0])):
			if(m[i][j]==0):cad=cad+" "+" "
			if(m[i][j]==2):cad=cad+" "+chr(27)+"[0;31m"+"*"+chr(27)+"[0m"
			if(m[i][j]==3):cad=cad+" "+chr(27)+"[1;31m"+str(m[i][j])+chr(27)+"[0m"
			if(m[i][j]==5):cad=cad+" "+chr(27)+"[1;36m"+str(m[i][j])+chr(27)+"[0m"
			if(m[i][j]==1):cad=cad+" "+chr(27)+"[1;33m"+"*"+chr(27)+"[0m"
			else: 
				if(m[i][j]!=5 and m[i][j]!=3 and m[i][j]!=2 and m[i][j]!=0):cad=cad+"|"+str(m[i][j])
		#print(lin)
		print("|"+cad+"|")
		cad=""
	print(lin)

def Pos(m,r,coor):
	est1=False#estado de posicion correcta
	solu=False
	nOpt=0
	cic=0
	opt=[]
	lis=[]
	while(solu==False):
		
		if(m[coor[0]][coor[1]]==5):solu=True
		
		if(((coor[1]+1)<len(m) and m[coor[0]][coor[1]+1]==0) or ((coor[1]+1)<len(m) and m[coor[0]][coor[1]+1]==5)):
			lis.append([coor[0],coor[1]+1])
			
		if(((coor[0]+1)<len(m) and m[coor[0]+1][coor[1]]==0) or ((coor[0]+1)<len(m) and m[coor[0]+1][coor[1]]==5)):
			lis.append([coor[0]+1,coor[1]])
			
		if(((coor[1]-1)>=0 and m[coor[0]][coor[1]-1]==0) or ((coor[1]-1)>=0 and m[coor[0]][coor[1]-1]==5)):
			lis.append([coor[0],coor[1]-1])
			
		if(((coor[0]-1)>=0 and m[coor[0]-1][coor[1]]==0) or ((coor[0]-1)>=0 and m[coor[0]-1][coor[1]]==5)):
			lis.append([coor[0]-1,coor[1]])

		if(len(lis)>0):
			est1=True
			nOpt=random.randint(0,len(lis)-1)
			#print(lis,lis[nOpt][0],"-",lis[nOpt][1])
			if(m[lis[nOpt][0]][lis[nOpt][1]]==5):
				solu=True
				#print("**************************")
				break
			m[lis[nOpt][0]][lis[nOpt][1]]=1
			os.system('cls')
			os.system('clear')
			verM(m)
			time.sleep(0.1)
			solu=Pos(m,r,[lis[nOpt][0],lis[nOpt][1]])
			
		if(coor[0]==1 and coor[1]==1):
				
			for i in range(len(m)):
				for j in range(len(m[0])):
					if(m[i][j]==2):m[i][j]=0
		
		if(solu==False):
			m[coor[0]][coor[1]]=2
			os.system('cls')
			os.system('clear')
			verM(m)
			time.sleep(0.1)
		if(cic==1):break
		cic=cic+1
	return solu;

nR=20

M=crearM(nR,nR)
M[nR-3][nR-3]=5
M[1][1]=1
for x in range(1):
	#M[random.randint(0,len(M)-1)][random.randint(0,len(M)-1)]=5
	for i in range(nR):
		while(True):
			obs=random.randint(0,len(M)-1)
			obs1=random.randint(0,len(M)-1)
			if(M[obs][obs1] != 1 and M[obs][obs1] != 5):break
			
		if(M[obs][obs1] != 1 and M[obs][obs1] != 5):M[obs][obs1]=3
		else: i=i-1

	Pos(M,1,[1,1])
	verM(M)
	for i in range(len(M)):
		for j in range(len(M[0])):
			M[i][j]=0
