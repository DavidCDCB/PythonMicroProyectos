#! /usr/bin/python
#https://stackoverflow.com/questions/42928765/convertnot-authorized-aaaa-error-constitute-c-readimage-453
#https://stackoverflow.com/questions/13303449/urllib2-httperror-http-error-403-forbidden
import re
import os
import sys
import urllib.request

lbar=[]
def download_images_from_url(url,cap,nPag,tomo,total,files):
    bar="#"
    carpeta=cap
    
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,} 
    request=urllib.request.Request(url,None,headers) #The assembled request
    response = urllib.request.urlopen(request)
    data = response.read() # The data u need
    
    imgUrls = re.findall('img .*?src="(.*?)"', str(data))
    
    
    for imgUrl in imgUrls:
        if(re.search('.jpg',imgUrl)):
            os.system('clear')
            nPag+=1
            print(str(total)+" Descargando Pag "+str(nPag)+" Cap "+str(tomo))
            for b in lbar:
                print(b)
            print(str(bar+">"))
            os.system('wget -q -nv -A .jpg '+imgUrl+' -O '+carpeta+'/'+str(tomo)+'-'+str(nPag)+'.jpg')
            files.append(str(tomo)+'-'+str(nPag)+'.jpg')
            
            bar+="#"
    lbar.append(bar)
    return files
    
if __name__ == '__main__':
    if(sys.platform.startswith('linux')):#win32 
        links=[]
        nPag=0
        nlink="" 
        cap="Manga"
        pdf="convert "
        files=[]
        tomo=sys.argv[2]
        
        archivo = open(sys.argv[1], "r") 
        lista=archivo.readlines()
        
        for i in range(0,len(lista)): 
            links.append(lista[i].split("\n")[0])

        archivo.close()
        #print(lista[0].split("\n")[0])
        os.system('mkdir ' + cap)
        os.system('mkdir pdf')

        for link in links:
            print(link)
            nlink=""
            for i in range(0,len(link.split("/"))-1):
                nlink+=link.split("/")[i]+"/"
                
            files=download_images_from_url(nlink+"cascade",cap,nPag,tomo,len(links),[])

            if(len(sys.argv)==4):
                if(sys.argv[3]=="-pdf"):
                    pdf="convert "
                    for dat in files:
                        pdf+="Manga/"+dat+" "
                    pdf=pdf+"./pdf/Tomo-"+str(tomo)+".pdf"
                    print("Generando pdf...")
                    os.system(pdf)
            print("OK!")
            tomo=int(tomo)+1
        os.system("mcomix -f -m -d -w ./Manga")
    exit(0)





