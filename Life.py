#! /usr/bin/python3
#1-Si una muerta tiene a su alrededor exactamente 3 vivas nace.
#2-Si una viva tiene menos de 2 o mas de 3 vivas a su alrededor muere.
import time
import random
import os
def crearM(f,c):
	m=[[0] * c for i in range(f)]
	return m

def verM(m):
	cad=""
	lin=""
	for i in range((len(m)*2)+3):
		lin+="-"
	print(lin)
	for i in range(len(m)):
		for j in range(len(m[0])):
			if(m[i][j]==0):cad=cad+"  "
			if(m[i][j]==1):cad=cad+" "+'\033[103m'+" "+'\033[0m'    
			if(m[i][j]==3):cad=cad+" "+'\033[102m'+" "+'\033[0m'
			if(m[i][j]==2):cad=cad+" "+'\033[43m'+" "+'\033[0m'
			else: 
				if(m[i][j]!=2 and m[i][j]!=3 and m[i][j]!=1 and m[i][j]!=0):cad=cad+"|"+str(m[i][j])
		print("|"+cad+" |")
		cad=""
	print(lin)

def Limp(m):
	mov=False
	for i in range(len(m)):
		for j in range(len(m[0])):
			if(m[i][j]==1):
				m[i][j]=3
				mov=True
			
			if(m[i][j]==2):
				m[i][j]=0
				mov=True
	return mov

def Life(m):
	cont=0
	for i in range(len(m)):
		for j in range(len(m[0])):
				
			if((j+1)<len(m)):
				if(m[i][j+1]==3 or m[i][j+1]==2):cont=cont+1
			if((j-1)>=0):
				if(m[i][j-1]==3 or m[i][j-1]==2):cont=cont+1

			if((i+1)<len(m)):
				if(m[i+1][j]==3 or m[i+1][j]==2):cont=cont+1
			if((i-1)>=0):
				if(m[i-1][j]==3 or m[i-1][j]==2):cont=cont+1
				
			if((i+1)<len(m) and (j+1)<len(m)):
				if(m[i+1][j+1]==3 or m[i+1][j+1]==2):cont=cont+1
			if((i-1)>=0 and (j-1)>=0):
				if(m[i-1][j-1]==3 or m[i-1][j-1]==2):cont=cont+1

			if((i-1)>=0 and (j+1)<len(m)):
				if(m[i-1][j+1]==3 or m[i-1][j+1]==2):cont=cont+1
			if((i+1)<len(m) and (j-1)>=0):
				if(m[i+1][j-1]==3 or m[i+1][j-1]==2):cont=cont+1

			if(m[i][j]==3):
				if(cont<2 or cont>3):
					m[i][j]=2
				
			if(m[i][j]==0):
				if(cont==3):
					m[i][j]=1
					
			cont=0

def Loop(M,t):
	alt=1
	cont=0
	mov=True
	while(mov==True and cont<40):
		#os.system('cls')
		os.system('clear')
		if(alt==1):
			verM(M)
			Life(M)
			mov=Limp(M)
			alt=2
		elif(alt==2):
			verM(M)
			Limp(M)
			Life(M)
			alt=1
		time.sleep(t)
		print(cont)

def gen(m):
	obs=0
	obs1=0
	for i in range(1000):
		while(True):
			obs=random.randint(0,len(M)-1)
			obs1=random.randint(0,len(M)-1)
			if(M[obs][obs1] != 3):break
		if(M[obs][obs1]==0):M[obs][obs1]=3


def f1(M):
	for i in range(14,24):
		M[5][i]=3
		M[i][5]=3
	for i in range(14,24):
		M[31][i]=3
		M[i][31]=3

	M[15][17]=3
	M[15][19]=3
	M[15][18]=3
	M[16][18]=3
	#M[18][18]=3
	M[20][18]=3
	M[21][18]=3
	M[21][19]=3
	M[21][17]=3
	

def f2(M):
	M[19][13]=3
	M[19][11]=3
	M[18][12]=3
	M[20][12]=3
	M[21][12]=3
	M[17][12]=3
	
	M[19][23]=3
	M[19][25]=3
	M[18][24]=3
	M[17][24]=3
	M[20][24]=3
	M[21][24]=3
	
	M[18][18]=3
	M[19][18]=3
	M[20][19]=3
	M[20][17]=3
	M[18][17]=3
	M[18][19]=3

#M=crearM(37,37)
M=crearM(70,70)

#f1(M)
gen(M)	

verM(M)
input()
Loop(M,0.2)
