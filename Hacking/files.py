#! /usr/bin/python3
# _*_ coding: utf8 _*_
# https://pypi.org/project/who-is-on-my-wifi/

import os
import argparse
from os import popen
from netdiscover import * #using sudo apt install netdiscover
from mac_vendor_lookup import MacLookup

def main():
	#params = get_parametros()
	disc = Discover()
	lHost = []
	getway=get_way()
	print(getway)
	for i in range(5):
		for host in disc.scan(ip_range=getway):
			mac = str(host['mac']).split("'")[1]
			ip = str(host['ip']).split("'")[1]
			lHost.append(ft(mac,18)+ft(ip,15)+ft(mac,20))
		print("Encontrados: "+str(len(list(set(lHost)))))

	save = open("hosts.txt", "r", encoding="utf-8").readlines()
	print("\nDispositivos NUEVOS conectados:")
	for host in list(set(lHost)):
		if(host+"\n" not in save):
			print(host)
			file(host,"hosts.txt")
				
	print("\nDispositivos actualmente conectados:")
	for host in list(set(lHost)):
		if(host+"\n" in save):
			print(host)

def file_explorer():
	os.chdir("/home/david-pc/")
	actual = os.getcwd()
	for d in os.listdir(actual):
		if(os.path.isdir(d)):
			print(d)

def get_parametros():
	parser = argparse.ArgumentParser(description="Argumentos")
	parser.add_argument('-t', '--target', help="Ip router")
	return parser.parse_args()

def file(string,file_name):
	fw = open(file_name, "a", encoding="utf-8")
	fw.write(string+"\n")
	fw.close()

def ft(string,esp):
	espacios=esp-len(string)
	for i in range(espacios):
		string=string+" "
	return string+"║"

def get_way():
	r_ip = ""
	line = os.popen("ifconfig | grep '192.'").read()
	ip = line[line.index("inet"):line.index(("netmask"))].strip("inet ").strip(" ")

	for octeto in ip.split("."):
		if(ip.split(".").index(octeto)<3):
			r_ip += octeto+"."
		else:
			r_ip += "0/24"
	return r_ip


if __name__ == "__main__":
	main()
