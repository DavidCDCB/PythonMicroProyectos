#! /usr/bin/python3
# _*_ coding: utf8 _*_

import os
import socket

PORT = 23000

def get_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		s.connect(('10.255.255.255', 1))
		IP = s.getsockname()[0]
	except Exception:
		IP = '127.0.0.1'
	finally:
		s.close()
	return IP

def main():
	print(get_ip())
	IP_SERVER = '127.0.0.1'

	mySocket = socket.socket()
	mySocket.bind((IP_SERVER,PORT))
	mySocket.listen(1)

	while True:
		print("\nEsperando cliente conectado...")
		user,addr = mySocket.accept()
		print("Conexion de: {}".format(addr[0]))
		user.sendall("ok".encode("ascii"))
		while True:
			data = user.recv(16)
			print('received {!r}'.format(data))
			if data:
				print('sending data back to the client')
				user.sendall(data.encode("ascii"))
				break
			else:
				print('no data from', addr)
				break

	user.close()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		exit()
