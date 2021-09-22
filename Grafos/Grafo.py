from Vertice import *

class Grafo:
    def __init__(self):
        self.listaVertices = {}#diccionario que contiene como ind el dato del v y el dato como un obj tipo Vertice
        self.numVertices = 0

    def __iter__(self):#Crear invocacion iterable del obj
        #retorna un obj iterable con los vertices
        return iter(self.listaVertices.values())

    def __contains__(self,n):#para usa el in obj
        return n in self.listaVertices

    def agregarVertice(self,clave):
        self.numVertices = self.numVertices + 1
        nuevoVertice = Vertice(clave)
        self.listaVertices.setdefault(clave,nuevoVertice)
        return nuevoVertice

    def obtenerVertice(self,n):
        if(n in self.listaVertices):
            return self.listaVertices.get(n)
        else:
            return None

    def agregarAristaD(self,de,a,costo=0):
        if(de not in self.listaVertices):
            self.agregarVertice(de)
        if(a not in self.listaVertices):
            self.agregarVertice(a)
        self.listaVertices.get(a).predecesor=de
        self.listaVertices.get(de).agregarVecino(self.listaVertices.get(a), costo)
        
    def agregarArista(self,de,a,costo=0):
        if(de not in self.listaVertices):
            self.agregarVertice(de)
        if(a not in self.listaVertices):
            self.agregarVertice(a)
        self.listaVertices.get(a).predecesor=de
        self.listaVertices.get(de).agregarVecino(self.listaVertices.get(a), costo)
        self.listaVertices.get(de).predecesor=a
        self.listaVertices.get(a).agregarVecino(self.listaVertices.get(de), costo)

    def obtenerVertices(self):
        return self.listaVertices.keys()
        
    def recorrer(self,inicial,tip):
        visitados=[]
        lista=[]
        capturados=[]
        ponderacionT=0
        lista.append(self.obtenerVertice(inicial))
        visitados.append(self.obtenerVertice(inicial))
        if(inicial in self):
            while(lista):
                capturados.append(lista[tip].id)
                for p in lista[tip].conectadoA.values(): ponderacionT+=p
                for v in lista.pop(tip).obtenerConexiones():
                    if(v not in visitados):
                        visitados.append(v)
                        lista.append(v)
 
        return str(ponderacionT)+"-"+str(capturados)
    
    def matrisAd(self,m,nV):
        for dat in nV:
            self.agregarVertice(dat)
    
        for f in range(len(m)):
            for c in range(len(m[f])):
                if(m[f][c]!=0):
                    self.agregarArista(nV[f],nV[c],m[f][c])
                    
    def ver(self):
        for V in self:#itera sobre los vertices del obj G iterable
            print(V.obtenerId(),"-->",[str(V.conectadoA.get(x))+">"+str(x.id) for x in V.obtenerConexiones()])
 

    def Dijkstra(self,inicial,final):
            visitados=[]
            camino=[]
            adyacentes=[]#ad validos no visitados
            vActual=self.obtenerVertice(inicial);
            visitados.append(vActual)
            cMenor=0#costo menor de los ad
            menor=None
    
            while(len(visitados)<self.numVertices):
                for V in vActual.obtenerConexiones():
                    #print(vActual.id,"---",V.id)
                    if(V not in visitados):
                        if(V.costo==0 or (vActual.costo+vActual.conectadoA.get(V))<V.costo):
                            V.costo=(vActual.costo+vActual.conectadoA.get(V))
                            V.predecesor=vActual.id
                        adyacentes.append(V)
                        
                for v in adyacentes:
                    #print(vActual.id,v.id)
                    if(cMenor==0 or v.costo<cMenor):
                        cMenor=v.costo
                        menor=v
                        
                vActual=menor
                adyacentes.remove(menor)
                cMenor=0
                
                if(vActual not in visitados):
                    visitados.append(vActual)
                    print(vActual.id,(vActual.predecesor,vActual.costo))
           
            camino.append(self.obtenerVertice(final))
            actual=self.obtenerVertice(final).predecesor
            while(actual!=None):
                camino.append(self.obtenerVertice(actual))
                if(actual==inicial):break
                actual=self.obtenerVertice(actual).predecesor
                
            return camino.__reversed__()
