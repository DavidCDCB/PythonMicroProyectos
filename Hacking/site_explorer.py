#! /usr/bin/python3
# _*_ coding: utf8 _*_

#https://mechanize.readthedocs.io/en/latest/index.html

from collections import deque
from bs4 import BeautifulSoup
from Wappalyzer import Wappalyzer, WebPage
import mechanize as mz
import hashlib
import requests
import argparse
import os
import sys
import re

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'


def main():
	open("rutas.txt", "w", encoding="utf-8").close()
	open("recursos.txt", "w", encoding="utf-8").close()
	params = get_parametros()
	#headers = get_headers(params.target)
	#get_tecnologies(params.target)
	#get_data("https://www.kindgirls.com")
	get_data(params.target)
	

def get_hash(text):
	hash_object = hashlib.md5(text.encode())
	return hash_object.hexdigest()
	# return str(len(text))


def file(string,file_name):
	fw = open(file_name, "a", encoding="utf-8")
	fw.write(string+"\n")
	fw.close()


def get_tecnologies(url):
	wappalyzer = Wappalyzer.latest()
	webpage = WebPage.new_from_url(url)
	print("Tecnologias usadas en: {}".format(url))
	tecnoligies = wappalyzer.analyze_with_versions_and_categories(webpage)
	for t in tecnoligies:
		print(t)
	input("\nEnter para analizar...")


def get_links(text):
	ln=[]
	for tag in re.findall('<a.*?href="(.*?)"',text):
		if(tag != "/" and tag != ""):
			ln.append(tag)
	return ln

def get_sources(text,original_site):
	links=[]
	original_site=original_site.split("/")[2]
	for s in re.findall('<.*?src="(.*?)"',text):
		if(" " not in s):
			if("." in s.split("/")[len(s.split("/"))-1]):
				if("://" not in s and "//" not in s):
					if(s[0]!="/"):
						links.append("https://"+original_site+"/"+s)
					else:
						links.append("https://"+original_site+s)
				else:
					
					if("//" in s):
						links.append("https://"+s.split("//")[1])
					else:
						links.append("https://"+s)
	return links


def new_get_href(site,original_site):
	bus = mz.Browser()
	bus.set_handle_robots(False)
	bus.set_handle_equiv(False)
	bus.addheaders = [('User-Agent',USER_AGENT)]
	links=[]
	
	original_site=original_site.split("/")[2]
	dominio=original_site.split(".")[len(original_site.split("."))-2]

	if(dominio in site):
		#text=bus.open(site).read()
		text=requests.get(url=site).text
		#lLinks=bus.links()
		lLinks=get_links(text)

		for i in lLinks:
			if(len(links) == 0 or i not in links):
				if("://" not in i and i != ""):
					if(i[0]!="/"):
						links.append("https://"+original_site+"/"+i)
					else:
						links.append("https://"+original_site+i)
				else:
					if(original_site in i):
						links.append(i)
		return {
			"text":text,
			"links":links
		}

	else:
		return {
			"text":[],
			"links":[]
		}


def download_images(imgs, site):
	if(len(imgs) > 0):
		path = site.split("//")[1].replace("/", "_")
		if(os.path.isdir(path+"/") == False):
			os.mkdir(path+"/")

		print("\nDESCARGANDO: \n")
		for imgUrl in imgs:
			name_img = imgUrl.split("/")[len(imgUrl.split("/"))-1]
			os.system('wget -nv '+imgUrl+' -O '+path+'/'+name_img)
			# wget.download("http://"+imgUrl, out=path+'/')


def get_data(site):
	original_site = site
	cola = deque()
	visitados = [] # lista de visitados
	data_visitada = [] # tamaño de la data de cada ruta
	sitios_visitados = [] # rutas validas
	imgs = [] # links a imagenes
	sources = [] # recursos 
	
	while(cola != False):

		try:
			contenido=new_get_href(site,original_site)
			#data = requests.get(url=site).text
			data = str(contenido['text'])
			if(get_hash(data) not in data_visitada or len(data_visitada) == 0):
				data_visitada.append(get_hash(data))
				sitios_visitados.append(site)
				file(site,"rutas.txt")
			else:
				print(get_hash(data))
				data = ""
		except Exception as e:
			data = ""
			print("<<NO CONECTADO>>", e)

		if(data != ""):

			# Captura de recursos en general
			for i in get_sources(data,original_site):
				if(i not in sources or len(sources) == 0):
					sources.append(i)
					file(i,"recursos.txt")
					
			''' Captura de imagenes JPG
			for i in get_tags_img(data):
			    if(i not in imgs or len(imgs) == 0):
			        imgs.append(i)
			        file(i) '''

			#download_images(sources,site)

			#links = get_tags_href1(data, site, original_site)
			links = contenido["links"]
			for l in links:
				if((l not in cola or len(cola) == 0) and l not in visitados):
					cola.append(l)

			print("BUSCANDO...")
		
		#os.system("clear")
		print("\n"+site+"\n")
		print("\nPOSIBLES RUTAS: "+str(len(cola)))
		print("LINKS PROCESADOS: "+str(len(visitados)))
		print("SITIOS VALIDOS: "+str(len(sitios_visitados)))
		print("RECURSOS ENCONTRADOS: "+str(len(sources)))
		
		
		if(len(cola) > 0):
			site = cola.popleft()
			visitados.append(site)
		else:
			break

	print("\nDIRECTORIOS ENCONTRADOS:")
	for s in sitios_visitados:
		print(s)

	print("\nRECURSOS ENCONTRADOS:")
	for i in sources:
		print(i)

def eliminar(l):
	cad = ""
	for group in l.split("/"):
		if(".html" not in group and ".aspx" not in group and ".php" not in group):
			for letter in group:
				cad += letter
			cad += "/"
	# print(cad[:-1])
	return cad[:-1]


def get_tags_img(str):
	links = []
	l = ""
	for line in str.split("\n"):
		if("img" in line and 'src="' in line):
			for line1 in line.split("img"):
				for line2 in line1.split("src"):
					if(".jpg" in line2 or ".jpeg" in line2):
						if(len(line2.split('"')) > 2):
							if("//" in line2.split('"')[1]):
								l = line2.split('"')[1].split("//")[1]
								if(l[len(l)-1] == "g"):
									links.append(l)
								else:
									if(".jpg" in line2):
										l = l.split(".jpg")[0]
										links.append(l+".jpg")
	return links


def get_tags_src(str,link,original_site):
	links = []
	s = ""
	original_site=original_site.split("/")[2]
	for line in str.split("\n"):
		if('src="' in line):
			for line1 in line.split("src"):
				if(len(line1.split('"'))>=2):
					s=line1.split('"')[1]
					if(" " not in s):
						if("." in s.split("/")[len(s.split("/"))-1]):

							if("://" not in s and "//" not in s):

								if(s[0]!="/"):
									links.append("https://"+original_site+"/"+s)
								else:
									links.append("https://"+original_site+s)
							else:
								if("//" in s):
									links.append("https://"+s.split("//")[1])
								else:
									links.append("https://"+s)
	return links


def get_tags_href1(str, link, original_site):
	links = []
	l = ""
	for line in str.split("\n"):
		if("<a" in line and 'href' in line):
			for line1 in line.split("<a"):
				for line2 in line1.split("href"):
					if('"' in line2):
						l = line2.split('"')[1]
						if(" " not in l and l != "/"):
							if("://" not in l):  # Si es una ruta relativa
								if("." in l):
									link = eliminar(link)
									if(l[0] != "/" and link[len(link)-1] != "/"):
										l = "/"+l
									if(l[0] == "/" and link[len(link)-1] == "/"):
										l = l[1:]
									links.append(link+l)
								else:
									links.append(link+l)
							elif(original_site in l):  # Si la ruta es del mismo sitio
								links.append(l)

	if(link.split("//")[1] in links):
		links.remove(link.split("//")[1])
	return links


def get_headers(site):
	try:
		url = requests.get(url=site)
		encabezados = dict(url.headers)
		return encabezados
	except:
		print("Sin conexion")


def show_headers(headers):
	for k, v in headers.items():
		print("{} - {}".format(k, v))


def get_parametros():
	parser = argparse.ArgumentParser(description="Argumentos")
	parser.add_argument('-t', '--target', help="Explicacion del argumeto")
	return parser.parse_args()


if __name__ == "__main__":
	main()
