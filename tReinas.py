import random
import os
from datetime import datetime
import threading

d1 = []
d2 = []
lm = []

solu = False
fail = []

nR = 20


def crearM(f, c):
    m = [[" "] * c for i in range(f)]
    return m


def verM(m, archivo):
    cad = ""
    lin = ""
    caracter = ""
    if(len(m) > 0):
        for i in range(len(m[0])*2):
            lin += "-"
        print(lin)
        archivo.write(lin+"\n")
        for i in range(len(m)):
            for j in range(len(m[0])):
                if(m[i][j] != " "):
                    cad = cad+"*"+"|"
                else:
                    cad = cad+str(m[i][j])+"|"
            print("|"+cad)
            archivo.write("|"+cad+"\n")
            cad = ""
        archivo.write(lin+"\n")


def rep(m, lm):

    ban = False
    for i in range(len(lm)):
        if(m == lm[i]):
            ban = True
            break
    return ban


def Solucion(ver, archivo1, archivo):
    nMax = 10
    m = []
    m
    global fail
    global solu
    while(True):
        '''
        if(solu):
                for i in list(set(fail)):#Filtrado rapido
                        archivo1.write(i+"\n")
                print("--------------")
                break
        '''
        d1 = []
        d2 = []

        pCol = range(0, nR)
        pFil = [0]*nR

        for i in range(len(pCol)):
            num = random.randint(0, nR-1)
            while(pFil[num] != 0):
                num = random.randint(0, nR-1)
            pFil[num] = pCol[i]

        if(len(pFil) == 0):
            fail.append(str(pFil))

        if(not str(pFil) in fail):
            for i in range(len(pFil)):
                if((not (i-pFil[i]) in d1) and (not (i+pFil[i]) in d2)):
                    d1.append(i-pFil[i])
                    d2.append(i+pFil[i])
                else:
                    if(not str(pFil) in fail):
                        fail.append(str(pFil))
                    break

            verM(m, archivo)
            if((len(d1) > nMax) or (len(d2) > nMax)):

                print(d1)
                print(d2)
                print("Buscando...")

                # nMax=max(len(d1),len(d2))

            if(len(set(d1)) == nR and len(set(d2)) == nR):
                m = crearM(nR, nR)
                for i in range(len(pFil)):
                    m[i][pFil[i]] = pFil[i]
                print(len(fail))

                # for i in list(set(fail)):#Filtrado rapido
                #	archivo1.write(i+"\n")

                solu = True
                break
    return m


def Soluciones(archivo, archivo1, fail):
    nRep = 0
    while(True):
        m = Solucion(False, archivo1, fail)
        if(len(lm) == 0):
            lm.append(m)
        else:
            if(not rep(m, lm)):
                lm.append(m)
                nRep = 0
            else:
                nRep += 1

        if(nRep == len(lm)*2):
            break
        verM(m, archivo)
        print("Intentos"+str(nRep))
        print("Total:"+str(len(lm)))
    return lm


def inicio():
    global fail

    archivo1l = open("Fails.txt", "r")
    for linea in archivo1l.readlines():
        fail.append(linea.split("\n")[0])
        # print(linea)
    archivo1l.close()

    print(len(fail))

    archivo = open("Reinas.txt", "a")
    archivo1 = open("Fails.txt", "w")
    ini = datetime.now()

    # lm=Soluciones(archivo,archivo1,fail)
    # lm.append(Solucion(False,archivo1))

    verM(Solucion(False, archivo1, archivo), archivo)
    print(datetime.now()-ini)
    archivo.write(str(datetime.now()-ini))

    archivo.close()
    archivo1.close()


for num_hilo in range(1):
    hilo = threading.Thread(name=num_hilo, target=inicio)
    hilo.start()
