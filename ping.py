import requests
import time
import os
from datetime import datetime

# 2672 bits
def check_internet(url='https://gist.githubusercontent.com/DavidCDCB/d034dcf2a5a3ac16482b7c73c32754d8/raw/'):
	global fails,data,estado,c_size
	try:
		data = requests.get(url,timeout=3)
		c_size = len(data.content)
		estado=True
	except Exception as e:
		fails=fails+1
		estado=False
		
def get_barra(num):
	cad = "|"
	if(num < 0):
		num = 5
	for b in range(num):
		cad+="██"
	for b in range(30-num):
		cad+="░░"
	return cad+"|"

data = None	
fails=0
low = 0
estado=True
count = 0
minimo = 5000
maximo = 0
suma = 0
porcentaje = 0
actual = 0
n_carga = 1
barra = ""
e_barra = ["(-)","(\\)","(|)","(/)"]
carga = ""
size = 0
c_size = 0 #Bytes
b_s = 0
time_t = 0

#os.system("brave-browser https://ny.testmy.net/b/dl-5MB")

while(True):
	ini = datetime.now()
	check_internet();
	dif = datetime.now()-ini
	carga = e_barra[n_carga-1]
	count += 1
	actual = (dif.seconds*1000)+(dif.microseconds//1000)
	suma += actual
	avg = suma//count
	barra = get_barra(((3000-actual)*30)//2962)
	minimo = min(minimo,actual)
	maximo = max(maximo,actual)
	porcentaje = round((low/count)*100)
	time_t += actual
	
	os.system("clear")
	
	if(time_t >= 1000):
		b_s = size/1000 #/125000
		time_t = 0
		size = 0
	else:
		size += c_size
	
	if(dif.seconds>0 and estado==True):
		low += 1
		print(data.text)
		print(f"\033[93m{carga} {actual:5} ms {barra}\033[0m")
		print(f"\nmin: {minimo} AVG: {avg} MAX: {maximo} \nLOW: {low} ({porcentaje}%) FAIL: {fails} \nKBps: {b_s}")
	elif(dif.seconds==0 and estado==True):
		print(data.text)
		print(f"\033[92m{carga} {actual:5} ms {barra}\033[0m")
		print(f"\nmin: {minimo} AVG: {avg} MAX: {maximo} \nLOW: {low} ({porcentaje}%) FAIL: {fails} \nKBps: {b_s}")
		
	elif(estado==False):
		count = 0
		low = 0
		minimo = 5000
		maximo = 0
		suma = 0
		print(f"\033[91m{carga} {actual:5} ms {get_barra(1)}:{fails}\033[0m")
		time.sleep(1)
		
	data = None
	n_carga += 1
	if(n_carga==5):
		n_carga=1
	
	
		
