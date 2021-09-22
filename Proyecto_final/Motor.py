from Grafo import Grafo
from Barrio import Barrio
from Tanque import Tanque
from tkinter import *
import pygame,random
from pygame.locals import *
import math
import json


class Motor:

    def __init__(self):
        # Variables
        self.contador = 0   # Contador global

        # Datos
        self.barrios=[]     # Lista de barrios
        self.g = Grafo()    # Grafo con los tanques
        self.matriz = []     # Matriz del mapa(Edita luego)
        self.matriz_temp = []  # Matriz temporal para calcular caminos
        
        # Graficacion
        self.img_mapa = []  # Lista de imagenes para graficar(modificar luego)
        self.cursor = Cursor()      # Cursor del programa
        self.menu = Menu()      # Menu del programa
        self.fuenteA = pygame.font.SysFont("Calibri", 30)
        
        # Datos auxiliares
        self.tanque_aux=None        #Tanque auxiliar, usado en creacion de arista
        self.camino_aux=[]          #Lista auxiliar usada en creacion de arista
        self.prim=[]                #Lista de rutas optimas para el arbol
        self.bool_rutas=False       #Establece si se deben mostrar o no las rutas
        
        #Contadores para id
        self.cont_id_barrio = 0
        self.cont_id_tanque = 0
        self.cont_id_tuberia = 0

        # Metodos
        self.carga_imagenes()  # Carga las imagenes a la lista de imagenes
        self.carga_matriz()  # Carga la matriz con numeros a graficar
        self.carga_grafo()  # Carga el grafo
        
        
    def carga_matriz(self):
        """Carga la matriz con los datos a dibujar"""
        for i in range(0, 40, 1):
            self.matriz.append([0]*40)



    def carga_grafo(self):
        with open('file.json') as file:
            data = json.load(file)
            
            for v in data['Tanques']:
                self.crea_tanque(int(v['x'])*2,int(v['y'])*2,int(v['Capacidad']),int(v['Nombre']))
                
            for a in data['Aristas']:
                t1=self.g.devuelve_vertice_num(int(a['Inicio']))
                t2=self.g.devuelve_vertice_num(int(a['Fin']))
                peso=int(a['Peso'])
                self.crea_tuberia(t1,t2,peso)
    
            for b in data['Barrios']:
                x=b['x']*2
                y=b['y']*2
                num=b['id']
                self.crea_barrio(x,y,num)
                
        



    def carga_imagenes(self):
        """Carga el diccionario de imagenes"""
        self.img_mapa={
        "pasto_0":pygame.image.load('Recursos/Mapa/pasto_0.png'),
        "pasto_1": pygame.image.load('Recursos/Mapa/pasto_1.png'),
        "ciudad_0":pygame.image.load('Recursos/Mapa/ciudad_0.png'),
        "ciudad_1":pygame.image.load('Recursos/Mapa/ciudad_1.png'),
        "ciudad_2": pygame.image.load('Recursos/Mapa/ciudad_2.png'),
        "ciudad_3": pygame.image.load('Recursos/Mapa/ciudad_3.png'),
        "tA_0":pygame.image.load('Recursos/Mapa/tuberiaA_0.png'),
        "tA_1":pygame.image.load('Recursos/Mapa/tuberiaA_1.png'),
        "tA_2":pygame.image.load('Recursos/Mapa/tuberiaA_2.png'),
        "tA_3":pygame.image.load('Recursos/Mapa/tuberiaA_3.png'),
        "tB_0":pygame.transform.rotate(pygame.image.load('Recursos/Mapa/tuberiaA_0.png'),90),
        "tB_1":pygame.transform.rotate(pygame.image.load('Recursos/Mapa/tuberiaA_1.png'),90),
        "tB_2":pygame.transform.rotate(pygame.image.load('Recursos/Mapa/tuberiaA_2.png'),90),
        "tB_3":pygame.transform.rotate(pygame.image.load('Recursos/Mapa/tuberiaA_3.png'),90),
        "tD_0":pygame.image.load('Recursos/Mapa/tuberiaD_0.png'),
        "tD_1":pygame.transform.rotate(pygame.image.load('Recursos/Mapa/tuberiaD_0.png'),90),
        "tG": pygame.image.load('Recursos/Mapa/tuberiaG.png'),
        "tDG":pygame.transform.rotate(pygame.image.load('Recursos/Mapa/tuberiaDG.png'),90),
        "tanque_0":pygame.image.load('Recursos/Mapa/tanque_0.png'),
        "tanque_1": pygame.image.load('Recursos/Mapa/tanque_1.png'),
        "tanque_2": pygame.image.load('Recursos/Mapa/tanque_2.png'),

        }
        

        


    def metodos(self, ventana):
        """Llama a todos los metodos necesarios de la clase en cada loop"""
        self.dibujar(ventana)
        self.cursor.metodos()
        self.desborde()
        self.contador += 1

    def desborde(self):
        for vertice in self.g.listaVertices.keys():
            if vertice.num is not 0:
                vertice.capacidad_actual = 0
            else:
                vertice.capacidad_actual=vertice.capacidad_max
        
        
        for v,a in self.g.listaVertices.items():
            for arista in a:
                if arista.bool_ruta and arista.destino.num is not 0:
                    arista.destino.capacidad_actual+=arista.peso



    """---------Metodos para graficar-----------------"""

    def dibujar(self, ventana):
        """Dibuja los elementos del motor en orden"""
        pygame.Surface.fill(ventana, (155, 155, 155))
        ancho = 32
        largo = 32
    
        def dibuja_tanques():
            """Dibuja los tanques del grafo"""
            for tanque in self.g.listaVertices.keys():
                x, y = (tanque.x * 32-10, tanque.y * 32-10)
                # texto = dibuja_texto(str(tanque.capacidad_max))
            
                if tanque.capacidad_actual is 0:
                    ventana.blit(self.img_mapa["tanque_2"], (x, y))
                elif tanque.capacidad_actual <= tanque.capacidad_max:
                    ventana.blit(self.img_mapa["tanque_0"], (x, y))
                else:
                    ventana.blit(self.img_mapa["tanque_1"], (x, y))
            
                # ventana.blit(texto, (x+8,y+10))
    
        def dibuja_barrios():
            """Dibuja los barrios"""
            for barrio in self.barrios:
                for i in range(0, len(barrio.pos)):
                    p = barrio.pos[i]
                    if barrio.sprite[i] is 0:
                        ventana.blit(self.img_mapa["ciudad_0"], (p[0] * 32, p[1] * 32))
                    elif barrio.sprite[i] is 1:
                        ventana.blit(self.img_mapa["ciudad_1"], (p[0] * 32, p[1] * 32))
                    elif barrio.sprite[i] is 2:
                        ventana.blit(self.img_mapa["ciudad_2"], (p[0] * 32, p[1] * 32))
                    elif barrio.sprite[i] is 3:
                        ventana.blit(self.img_mapa["ciudad_3"], (p[0] * 32, p[1] * 32))
    
        def dibuja_tuberias():
            """Dibuja las tuberias"""
            mod_cont = self.contador % 20
            # Dibuja tuberias obstruidas
            
            for arista in self.g.aristas_eliminadas:
                inicio = (arista[0].x, arista[0].y)
                fin = (arista[1].x, arista[1].y)
                camino = arista[2]
    
                lis = self.rutas_sprite(camino, fin, inicio)
                for i in range(0, len(camino), 1):
                    punto = camino[i]
                    punto = (punto[0] * 32, punto[1] * 32)
        
                    if lis[i] is 0: ventana.blit(self.img_mapa["tD_0"], punto)
                    if lis[i] is 1: ventana.blit(pygame.transform.flip(self.img_mapa["tD_0"], True, False), punto)
                    if lis[i] is 2: ventana.blit(self.img_mapa["tD_1"], punto)
                    if lis[i] is 3: ventana.blit(pygame.transform.flip(self.img_mapa["tD_1"], False, True), punto)
                    if lis[i] is 4: ventana.blit(self.img_mapa["tDG"], punto)
                    if lis[i] is 5: ventana.blit(pygame.transform.rotate(self.img_mapa["tDG"], 90), punto)
                    if lis[i] is 6: ventana.blit(pygame.transform.rotate(self.img_mapa["tDG"], 180), punto)
                    if lis[i] is 7: ventana.blit(pygame.transform.rotate(self.img_mapa["tDG"], 270), punto)
            
            #Dibuja tuberias sin obstruir
            for tanque in self.g.listaVertices.keys():
                for arista in self.g.listaVertices[tanque]:
                    if arista.bool_ruta is True:
                    
                        lis = self.rutas_sprite(arista.camino, (tanque.x, tanque.y),
                                                (arista.destino.x, arista.destino.y))
                        for i in range(0, len(arista.camino), 1):
                            punto = arista.camino[i]
                            punto = (punto[0] * 32, punto[1] * 32)
                        
                            if mod_cont < 5:
                                if lis[i] is 0: ventana.blit(self.img_mapa["tA_0"], punto)
                                if lis[i] is 1: ventana.blit(pygame.transform.flip(self.img_mapa["tA_0"], True, False),
                                                             punto)
                                if lis[i] is 2: ventana.blit(self.img_mapa["tB_0"], punto)
                                if lis[i] is 3: ventana.blit(pygame.transform.flip(self.img_mapa["tB_0"], False, True),
                                                             punto)
                            elif mod_cont < 10:
                                if lis[i] is 0: ventana.blit(self.img_mapa["tA_1"], punto)
                                if lis[i] is 1: ventana.blit(pygame.transform.flip(self.img_mapa["tA_1"], True, False),
                                                             punto)
                                if lis[i] is 2: ventana.blit(self.img_mapa["tB_1"], punto)
                                if lis[i] is 3: ventana.blit(pygame.transform.flip(self.img_mapa["tB_1"], False, True),
                                                             punto)
                            elif mod_cont < 15:
                                if lis[i] is 0: ventana.blit(self.img_mapa["tA_2"], punto)
                                if lis[i] is 1: ventana.blit(pygame.transform.flip(self.img_mapa["tA_2"], True, False),
                                                             punto)
                                if lis[i] is 2: ventana.blit(self.img_mapa["tB_2"], punto)
                                if lis[i] is 3: ventana.blit(pygame.transform.flip(self.img_mapa["tB_2"], False, True),
                                                             punto)
                            elif mod_cont < 20:
                                if lis[i] is 0: ventana.blit(self.img_mapa["tA_3"], punto)
                                if lis[i] is 1: ventana.blit(pygame.transform.flip(self.img_mapa["tA_3"], True, False),
                                                             punto)
                                if lis[i] is 2: ventana.blit(self.img_mapa["tB_3"], punto)
                                if lis[i] is 3: ventana.blit(pygame.transform.flip(self.img_mapa["tB_3"], False, True),
                                                             punto)
                        
                            if lis[i] > 3:
                                if lis[i] is 4: ventana.blit(self.img_mapa["tG"], punto)
                                if lis[i] is 5: ventana.blit(pygame.transform.rotate(self.img_mapa["tG"], 90), punto)
                                if lis[i] is 6: ventana.blit(pygame.transform.rotate(self.img_mapa["tG"], 180), punto)
                                if lis[i] is 7: ventana.blit(pygame.transform.rotate(self.img_mapa["tG"], 270), punto)
        

        def dibuja_tuberias_barrios():
            """Dibuja las tuberias de los barrios a los tanques"""
            for tanque in self.g.listaVertices:
                x_t = tanque.x * 32
                y_t = tanque.y * 32
            
                cap = tanque.capacidad_actual
            
                for barrio in tanque.barrios:
                    x_b = barrio.pos[0][0] * 32
                    y_b = barrio.pos[0][1] * 32
                
                    if cap is 0:
                        pygame.draw.line(ventana, (0, 0, 0), (x_b + 16, y_b + 16), (x_t + 16, y_t + 16), 10)
                    else:
                        pygame.draw.line(ventana, (0, 0, 255), (x_b + 16, y_b + 16), (x_t + 16, y_t + 16), 10)
    
        def dibuja_info():
            """Dibuja la informacion"""
            pygame.draw.rect(ventana, (0,100,200), (1100, 570, 130,70))
            self.fuenteA = pygame.font.SysFont("Calibri", 25, True)
        
            obj = self.objeto_en_punto((self.cursor.posx // 32, self.cursor.posy // 32))
            texto_obj = obj.__class__.__name__
            #print(texto_obj)
        
            if texto_obj is "Tanque":
                texto = self.fuenteA.render("Tanque(" + str(obj.num)+")", True, (0, 0, 0))
                texto2 = self.fuenteA.render(str(obj.capacidad_actual) + "/" + str(obj.capacidad_max), True, (0, 0, 0))
            elif texto_obj is "Barrio":
                texto = self.fuenteA.render("Barrio", True, (0, 0, 0))
                texto2 = self.fuenteA.render("num:"+str(obj.num), True, (0, 0, 0))
            elif obj is None:
                texto = self.fuenteA.render("¿¿¿???", True, (0, 0, 0))
                texto2 = self.fuenteA.render("¿/?", True, (0, 0, 0))
            else:
                num_t1 = obj[0].num
                num_t2 = obj[1].num
                peso = obj[2]
            
                texto = self.fuenteA.render("Tuberia", True, (0, 0, 0))
                texto2 = self.fuenteA.render(str(num_t1) + "->" + str(num_t2) + "   " + str(peso), True, (0, 0, 0))
        
            ventana.blit(texto, (1100 + 10, 570+5))
            ventana.blit(texto2, (1100+10, 570+40))
            
        def dibuja_mapa():
            for i in range(0, 30, 1):
                for j in range(0, 40, 1):
                    ventana.blit(self.img_mapa["pasto_0"], (j * 32, i * 32))
    
        def dibuja_lineas():
            for x in range(0, 40, 1):
                pygame.draw.line(ventana, (125, 125, 125), (x * 32, 0), (x * 32, 1300),1)
            for y in range(0, 40, 1):
                pygame.draw.line(ventana, (125, 125, 125), (0, y * 32), (1300, y * 32),1)
    
        def dibuja_tuberia_aux():
            if self.menu.bool_guarda_arista is True:
                for punto in self.camino_aux:
                    pygame.draw.circle(ventana, (255, 2, 2), (16 + punto[0] * 32, 16 + punto[1] * 32), 6)
    
        def dibuja_camino():
            if self.bool_rutas is False:
                return
            
            for arista in self.prim:
                v1 = arista[0]
                v2 = arista[1]
            
                camino = self.g.camino_arista(v1, v2)
                if camino is not None:
                    for punto in camino:
                        x = punto[0]
                        y = punto[1]
                        pygame.draw.circle(ventana, (0,70,0), (16 + punto[0] * 32, 16 + punto[1] * 32), 6)
    
        dibuja_mapa()
        dibuja_lineas()
        dibuja_tuberias()
        dibuja_tuberias_barrios()
        dibuja_tanques()
        dibuja_barrios()
        dibuja_tuberia_aux()
        
        dibuja_info()
        dibuja_camino()

        # Dibuja el cursor del mapa
        self.cursor.dibuja_cursor(ventana)

        # Dibuja el menu del mapa
        self.menu.dibuja(ventana)
            
    """-----------------Metodos de evento------------"""
    
    def evento_teclado(self):
        """Eventos de teclado, se repiten con cada presion de tecla"""
        keys_pressed = pygame.key.get_pressed()
        
        def evento_cursor():
            """Mueve el cursor segun las flechas"""
            varx = 0
            vary = 0
    
            if keys_pressed[K_LEFT] and self.cursor.x - 1 >= 0: varx = -1
            elif keys_pressed[K_RIGHT] and self.cursor.x + 1 <39: varx = 1;
            
            if keys_pressed[K_UP] and self.cursor.y - 1 >= 0: vary = -1
            elif keys_pressed[K_DOWN] and self.cursor.y + 1 <20: vary = 1
            
            if varx != 0 or vary != 0:
                self.cursor.mover(varx, vary)
                if self.menu.bool_guarda_arista is True:
                    pass
                """
                    p1=(self.tanque_aux.x,self.tanque_aux.y)
                    p2=(self.cursor.posx // 32,self.cursor.posy // 32)
                    lista=self.camino_t1_a_t2(p2,p1)
                    print(str(lista))
                """


        if self.menu.bool_mostrar_menu is False:
            evento_cursor()



    def eventos_menu(self, evento):
        """Llama a los metodos segun el evento y el estado del menu"""

        x = self.cursor.posx // 32
        y = self.cursor.posy // 32
        
        #Eventos de mostrar y ocultar
        def mostrar_menu():
            self.menu.bool_mostrar_menu = True
    
        def sale_menu():
            self.menu.bool_mostrar_menu = False
            
        def selecciona_evento():
            if self.menu.estado is 5:
                evento_muestra_caminos()
                return
            if self.menu.estado is 6:
                self.evento_prueba_2()
                return
            
            
            self.menu.bool_entra_seleccion = True
            self.menu.bool_mostrar_menu = False
            
        def sale_evento():
            self.menu.bool_entra_seleccion = False
            self.menu.bool_mostrar_menu = True

    
        def evento_estado_izq():
            """Reduce el estado del menu en 1"""
            if self.menu.estado - 1 >= 0:
                self.menu.estado = self.menu.estado - 1
    
        def evento_estado_der():
            """Aumenta el estado del menu en 1"""
            if self.menu.estado + 1 <= self.menu.limite_estado:
                self.menu.estado = self.menu.estado + 1
        
        """Eventos de estado"""
        # 1-Crea tanque 2-Crea barrio 3-Crea arista 4-Cambia direccion 5-Obstruye 6-Muestra...algo
        def evento_estado():
            """Hace un evento segun un estado"""
            if self.menu.estado is 0:self.crea_barrio(x, y)
            if self.menu.estado is 1:self.crea_tanque(x, y)
            if self.menu.estado is 2:evento_guarda_arista()
            if self.menu.estado is 3:self.crea_obstruccion(x,y)
            if self.menu.estado is 4:self.cambia_direccion(x,y)

            
            
        def evento_muestra_caminos():
            if self.bool_rutas is True:
                self.bool_rutas=False
            else:
                self.bool_rutas=True
            
        def evento_guarda_arista():
            """Si se mantiene una arista y se conecta a otra arista, crea una arista"""
            if self.nombre_clase_objeto(self.objeto_en_punto((x, y))) is "Tanque":
                self.tanque_aux= self.objeto_en_punto((x, y))
                self.matriz_anchura((self.cursor.posx // 32, self.cursor.posy // 32))
                self.menu.bool_entra_seleccion = False
                self.menu.bool_guarda_arista= True
                
        def sale_evento_guarda_arista():
            self.menu.bool_guarda_arista= False
            self.menu.bool_entra_seleccion = True
            self.tanque_aux = None

            
        def evento_crea_tuberia():
            """Crea la tuberia"""
            if self.nombre_clase_objeto(self.objeto_en_punto((x, y))) is "Tanque":
                self.crea_tuberia(self.tanque_aux,self.objeto_en_punto((x, y)))
                sale_evento_guarda_arista()

        bool_sin_menu= self.menu.bool_mostrar_menu is False and self.menu.bool_entra_seleccion is False and self.menu.bool_guarda_arista is False
        bool_muestra_menu= self.menu.bool_mostrar_menu is True and self.menu.bool_entra_seleccion is False and self.menu.bool_guarda_arista is False
        bool_seleccion_evento= self.menu.bool_mostrar_menu is False and self.menu.bool_entra_seleccion is True and self.menu.bool_guarda_arista is False
        bool_evento_crea_arista= self.menu.bool_mostrar_menu is False and self.menu.bool_entra_seleccion is False and self.menu.bool_guarda_arista is True
        
        #eventos sin menu:
        if bool_sin_menu is True:
            if evento is "q": mostrar_menu()
        
        #Eventos con menu
        if bool_muestra_menu is True:
            if evento is "q": sale_menu()
            if evento is "izq": evento_estado_izq()
            if evento is "der": evento_estado_der()
            if evento is "x": selecciona_evento()
            if evento is "z": sale_menu()
        
        
        #Eventos al seleccionar un estado
        if bool_seleccion_evento is True:
            if evento is "x": evento_estado()
            if evento is "z": sale_evento()
            
        #Evento cuando se va a crear una arista
        if bool_evento_crea_arista is True:
            if evento is "x": evento_crea_tuberia()
            if evento is "z": sale_evento_guarda_arista()
            
    """-----------------Metodos de creacion--------------"""
    def evento_prueba(self):
        
        for tanque1 in self.g.listaVertices.keys():
            if tanque1.capacidad_actual is 0:
                tanque2=self.tanque_mas_cercano((tanque1.x,tanque1.y))
                self.crea_tuberia(tanque1,tanque2,5)

    def evento_prueba_2(self):
        
        tanques=[]
        tanquesC = []
        for tanque1 in self.g.listaVertices.keys():
            if tanque1.capacidad_actual is 0:
                x = tanque1.x
                y = tanque1.y
                difx=0
                dify=0
                
                if 0 <= x-2 < len(self.matriz_temp[0]) and 0 <=y+2 < len(self.matriz_temp):
                    difx,dify=(-2,2)
                elif 0 <= x+2 < len(self.matriz_temp[0]) and 0 <=y+2 < len(self.matriz_temp):
                    difx,dify=(2,2)
                elif 0 <= x-2 < len(self.matriz_temp[0]) and 0 <=y-2 < len(self.matriz_temp):
                    difx,dify=(-2,-2)
                elif 0 <= x+2 < len(self.matriz_temp[0]) and 0 <=y-2 < len(self.matriz_temp):
                    difx,dify=(+2,-2)
                    
                if difx is not 0 and dify is not 0:
                    xN=x+difx
                    yN=y+dify
                    
                    tanqueN=Tanque(xN,yN,99,99,[])
                    tanques.append(tanqueN)
                    tanquesC.append(tanque1)

        for i in range(0,len(tanques),1):
            t1=tanques[i]
            t2=tanquesC[i]

            self.crea_tanque_prueba(t1)
            self.crea_tuberia(t1,t2,2)

            
                    
                    
                    
                    
            
            
            


    def crea_barrio(self,x,y,num=0):
        #Revisa si no hay un objeto
        if self.existe_en_puntos([(x,y),(x+1,y),(x,y+1),(x+1,y+1)]) is False:
            bar=Barrio(x,y,num,[random.randint(0,3),random.randint(0,3),random.randint(0,3),random.randint(0,3)])
            self.barrios.append(bar)
            self.cont_id_barrio += 1
            tanq_cer = self.tanque_mas_cercano((x, y))
            
            
            if tanq_cer is not None:
                tanq_cer.agrega_barrio(bar)

        else:
            pass
            #Algo pasa
  
  
    def crea_tanque(self,x,y,cap=50,num=0):
        if self.existe_en_puntos([x,y]) is False:
            self.g.agregar_vertice(Tanque(x,y,num,cap,[]))
            self.matriz[y][x]=-1
            self.cont_id_tanque += 1
            
    def crea_tanque_prueba(self,tanque):
        if self.existe_en_puntos((tanque.x,tanque.y)) is False:
            self.g.agregar_vertice(tanque)
            self.matriz[tanque.y][tanque.x]=-1
            self.cont_id_tanque += 1
    

    def crea_tuberia(self, t1, t2,peso=30):
        p_1 = (t1.x, t1.y)
        p_2 = (t2.x, t2.y)
        self.matriz_anchura(p_2)
        lista = self.camino_t1_a_t2(p_1, p_2)
    
        for punto in lista:
            x = punto[0]
            y = punto[1]
            self.matriz[y][x] = -2
        self.g.agregar_arista(t1, t2, peso, lista)


        self.prim = self.g.prim(self.g.devuelve_vertice_num(0))
        
    def crea_obstruccion(self,x,y):
        objeto=self.objeto_en_punto((x,y))

        if type(objeto) is tuple:
            t1=objeto[0]
            t2=objeto[1]
            camino=objeto[2]
            self.g.elimina_arista(t1,t2)
            inicio = list(self.g.listaVertices.keys())[0]
            self.prim = self.g.prim(self.g.devuelve_vertice_num(0))
        
    def cambia_direccion(self,x,y):
        objeto=self.objeto_en_punto((x,y))
        if type(objeto) is tuple:
            t1=objeto[0]
            t2=objeto[1]
            camino=objeto[2]
            self.g.cambia_ruta_arista(t1,t2)
            inicio = list(self.g.listaVertices.keys())[0]
 

    """-------------Metodos para encontrar rutas y objetos------------------"""

    def matriz_anchura(self, inicio, cont=1):
        """Crea una matriz con todos los posibles caminos desde un punto dado"""
        self.matriz_temp = [row[:] for row in self.matriz]
        var_x, var_y = ([0, 0, +1, -1], [+1, -1, 0, 0])
        ancho, alto = (len(self.matriz_temp[0]), len(self.matriz_temp))
        x_ini, y_ini = inicio
    
        lista = [(x_ini, y_ini)]
        self.matriz_temp[y_ini][x_ini] = -1
    
        while len(lista) is not 0:
            lista_aux = lista.copy()
            lista = []
        
            for punto in lista_aux:
                x, y = punto
                for i in range(0, 4, 1):
                    xN, yN = (x + var_x[i], y + var_y[i])
                    if 0 <= xN < ancho and 0 <= yN < alto:
                        if self.matriz_temp[yN][xN] is 0 or self.matriz_temp[yN][xN] is -2 or self.matriz_temp[yN][xN] > cont:
                            self.matriz_temp[yN][xN] = cont
                            lista.append((xN, yN))
            cont = cont + 1
        """
        for i in range(0, len(self.matriz_temp), 1):
            for j in range(0, len(self.matriz_temp[i]), 1):
                if self.matriz_temp[i][j] is -1:
                    print("x", end="  ")
                elif self.matriz_temp[i][j] <= 9:
                    print(str(self.matriz_temp[i][j]), end="  ")
                else:
                    print(str(self.matriz_temp[i][j]), end=" ")
            print("")

        """

    def existe(self, punto_obj):
        """Devuelve un booleano si existe o no un objeto en ese punto"""
        for barrio in self.barrios:
            for punto in barrio.pos:
                if punto_obj == punto:
                    return True

        for tanque in self.g.listaVertices.keys():
            if punto_obj == (tanque.x, tanque.y):
                return True
        return False

    def existe_en_puntos(self,lista_puntos):
        for punto in lista_puntos:
            if self.existe(punto) is True:
                return True
        return False

    def objeto_en_punto(self, punto_obj):
        """Devuelve un objeto en un punto dado, retorna None si no se encuentra nada"""
        
        for barrio in self.barrios:
            for punto in barrio.pos:
                if punto_obj == punto:
                    return barrio
        for tanque in self.g.listaVertices.keys():
            if punto_obj == (tanque.x, tanque.y):
                return tanque
            
            for arista in self.g.listaVertices[tanque]:
                if arista.bool_ruta is True:
                    for punto in arista.camino:
                        if punto_obj == punto:
                            return (tanque,arista.destino,arista.peso,arista.camino)
        return None
    

        
    
    def nombre_clase_objeto(self,objeto):
        return objeto.__class__.__name__
    
    def objeto_mas_cercano(self,p_inicio):
        punto=self.punto_mas_cercano(p_inicio)
        if punto is not None:
            return self.objeto_en_punto(punto)
        
        return None
    
    def distancia(self,p_a, p_b):
        return int(math.sqrt(math.pow((p_b[0] - p_a[0]), 2) + math.pow((p_b[1] - p_a[1]), 2)))

    def tanque_mas_cercano(self, inicio):
        punto_menor, dist_aux = (None, None)
        
        for tanque in self.g.listaVertices.keys():
            if (dist_aux is None or self.distancia(inicio, (tanque.x, tanque.y)) < dist_aux):
                if (tanque.x, tanque.y) != inicio:
                    dist_aux = self.distancia(inicio, (tanque.x, tanque.y))
                    punto_menor = (tanque.x, tanque.y)

        return self.objeto_en_punto(punto_menor)
    

    def punto_mas_cercano(self, inicio):
        """Devuelve el punto del objeto mas cercano a otro punto"""
    
        def distancia(p_a, p_b):
            return int(math.sqrt(math.pow((p_b[0] - p_a[0]), 2) + math.pow((p_b[1] - p_a[1]), 2)))
    
        punto_menor, punto_aux = (None, None)
    
        for barrio in self.barrios:
            for punto in barrio.pos:
                if punto_aux is None or distancia(inicio, punto) < punto_aux:
                    punto_aux = distancia(inicio, punto)
                    punto_menor = (punto[1], punto[0])
    
        for tanque in self.g.listaVertices.keys():
            if (punto_aux is None or distancia(inicio, (tanque.x, tanque.y)) < punto_aux):
                punto_aux = distancia(inicio, (tanque.x, tanque.y))
                punto_menor = (tanque.y, tanque.x)
    
        return punto_aux


        
        
    def camino_t1_a_t2(self,p_1,p_2):
        if p_1 == p_2:
            return []
        
        x1=p_1[0]
        y1=p_1[1]
        x2=p_2[0]
        y2=p_2[1]
        
        lista=[]
        lista=self.ruta_dos_arista(x1+1,y1,x2,y2,lista,[],self.matriz_temp[y1][x1+1])
        lista=self.ruta_dos_arista(x1-1,y1,x2,y2,lista,[],self.matriz_temp[y1][x1-1])
        lista=self.ruta_dos_arista(x1,y1+1,x2,y2,lista,[],self.matriz_temp[y1+1][x1])
        lista=self.ruta_dos_arista(x1,y1-1,x2,y2,lista,[],self.matriz_temp[y1-1][x1])
        

        return lista


    def ruta_dos_arista(self,x1,y1,x2,y2,lista,lista_aux,cont):
        if not(0 <= x1 < len(self.matriz_temp[0]) and 0 <= y1 < len(self.matriz_temp)):
            return lista

        if x1 is x2 and y1 is y2:
            if len(lista) is 0 or len(lista_aux)<len(lista) or self.contador_cruzes(lista_aux)<self.contador_cruzes(lista):
                lista = lista_aux.copy()
                return lista

        if cont is not self.matriz_temp[y1][x1]:
            return lista

        lista_aux.append((x1,y1))
        lista=self.ruta_dos_arista(x1+1,y1,x2,y2,lista,lista_aux,cont-1)
        lista=self.ruta_dos_arista(x1-1, y1, x2, y2, lista, lista_aux, cont - 1)
        lista=self.ruta_dos_arista(x1, y1+1, x2, y2, lista, lista_aux, cont - 1)
        lista=self.ruta_dos_arista(x1, y1-1, x2, y2, lista, lista_aux, cont - 1)
        lista_aux.pop()
        
        return lista
            
        
    def contador_cruzes(self,lista):
        cont=0
        for punto in lista:
            if self.matriz[punto[1]][punto[0]] is -2:
                cont += 1
        return cont
    
    def rutas_sprite(self,lista,inicio,fin):
        def num_ruta_sprite(dif):
            if dif == (-1, 0, 1, 0): return 1
            if dif == (1, 0, -1, 0): return 0
            if dif == (0, 1, 0, -1): return 3
            if dif == (0, -1, 0, 1): return 2
            if dif == (-1, 0, 0, 1) or dif == (0,1,-1,0): return 4
            if dif == (0, 1, 1, 0) or dif == (1,0,0,1): return 5
            if dif == (1, 0, 0, -1) or dif == (0,-1,1,0): return 6
            if dif == (0, -1, -1, 0) or dif == (-1,0,0,-1): return 7
            return -1
        
        lista_spri=[]
        
        if len(lista) is 0:
            return []
        
        if len(lista) is 1:
            dx=lista[0][0]-inicio[0]
            dy=lista[0][1]-inicio[1]

            if (dx, dy) == (-1, 0): lista_spri.append(0)
            elif (dx, dy) == (+1, 0): lista_spri.append(1)
            elif (dx, dy) == (0, -1): lista_spri.append(2)
            elif (dx, dy) == (-1, +1): lista_spri.append(3)
            return
        
        
        if len(lista) is 2:
            dx1 = lista[0][0] - inicio[0]
            dy1 = lista[0][1] - inicio[1]
            dx2 = lista[0][0] - lista[1][0]
            dy2 = lista[0][1] - lista[1][1]
            
            lista_spri.append(num_ruta_sprite((dx1, dy1, dx2, dy2)))
            
            #Este se cambia luego
            dx1 = lista[1][0] - lista[0][0]
            dy1 = lista[1][1] - lista[0][1]
            dx2 = lista[1][0] - fin[0]
            dy2 = lista[1][1] - fin[1]
            lista_spri.append(num_ruta_sprite((dx1, dy1, dx2, dy2)))
            return
            
        
        
        elif len(lista) > 2:
            dx1 = lista[0][0] - inicio[0]
            dy1 = lista[0][1] - inicio[1]
            dx2 = lista[0][0] - lista[1][0]
            dy2 = lista[0][1] - lista[1][1]
            lista_spri.append(num_ruta_sprite((dx1, dy1, dx2, dy2)))
            
            
  
            
            for i in range(1,(len(lista)-1),1):
               
                dx1=lista[i][0]-lista[i-1][0]
                dy1=lista[i][1]-lista[i-1][1]
                dx2=lista[i][0]-lista[i+1][0]
                dy2=lista[i][1]-lista[i+1][1]
                lista_spri.append(num_ruta_sprite((dx1,dy1,dx2,dy2)))
                
            #Este se cambia luego
            dx1 = lista[-1][0] - lista[-2][0]
            dy1 = lista[-1][1] - lista[-2][1]
            dx2 = lista[-1][0] - fin[0]
            dy2 = lista[-1][1] - fin[1]


            lista_spri.append(num_ruta_sprite((dx1, dy1, dx2, dy2)))
            
        return lista_spri

"""No pasai de aqui aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"""


class Cursor:
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.posx = 0
        self.posy = 0
        self.movx = 0
        self.movy = 0
        self.contadorAnim = 0
        self.estado = 0
        self.estadoB = False
        
        self.cursores = [pygame.image.load('Recursos/Mapa/0.png'),
                         pygame.image.load('Recursos/Mapa/1.png'),
                         ]
    
    def metodos(self):
        """Metodos del cursor"""
        self.contadores()
        self.movimiento()
    
    def contadores(self):
        """Modifica los contadores"""
    
        if self.estadoB is False:
            self.contadorAnim = self.contadorAnim + 1;
            if self.contadorAnim > 60:
                self.contadorAnim = 0
            self.contadorMov = 0;
        
        elif self.estadoB is True:
            self.contadorMov = self.contadorMov + 1
            if self.contadorMov > 1:
                self.contadorMov = 0
            self.contadorAnim = 0
    
    def mover(self, difx, dify):
        """Hace que el cursor se mueva a una direccion especifica"""
    
        if self.estadoB is False:
            self.x = self.x + difx
            self.y = self.y + dify
            self.movx = difx
            self.movy = dify
            self.estadoB = True

    def movimiento(self):
        """Mueve el cursor segun el contador"""
    
        if self.estadoB is True:
            self.posx = self.posx + 8 * self.movx
            self.posy = self.posy + 8 * self.movy
        
        difX = self.x * 32 * self.movx - self.posx * self.movx
        difY = self.y * 32 * self.movy - self.posy * self.movy
        
        if difX <= 0 and difY <= 0:
            self.estadoB = False;

    def dibuja_cursor(self, ventana):
        """Dibuja el cursor del programa"""
        sprite_num = 0
        
        if self.estadoB is True:
            sprite_num = self.estado * 2
        
        else:
            if self.contadorAnim < 30:
                sprite_num = self.estado * 2
            
            else:
                sprite_num = (self.estado * 2) + 1
        
        ventana.blit(self.cursores[sprite_num], (-4 + self.posx , -4 + self.posy ))


class Menu:
    def __init__(self):
        self.estado=0
        self.limite_estado=6
        self.pos_x=0
        self.pos_y=0
        
        self.bool_mostrar_menu=False
        self.bool_entra_seleccion=False
        self.bool_guarda_arista = False
        
        self.arista_aux= None
        
        self.iconos = [pygame.image.load('Recursos/Mapa/M0.png'),
                         pygame.image.load('Recursos/Mapa/M1.png'),
                         pygame.image.load('Recursos/Mapa/M2.png'),
                         pygame.image.load('Recursos/Mapa/M3.png'),
                         pygame.image.load('Recursos/Mapa/M4.png'),
                         pygame.image.load('Recursos/Mapa/M5.png'),
                         ]

    
    def dibuja(self, ventana):
        
        def dibuja_menu():
            """Dibuja el menu si mostrar esta en True"""
            alto=60
            pygame.draw.rect(ventana, (0, 155, 0), (0, 0, 400, alto))
    
            for i in range(0, self.limite_estado, 1):
                if i is not self.estado:
                    pygame.draw.rect(ventana, (255, 255, 255), (20 + (20 + 7 * alto // 10) * i, alto // 7, 7 * alto // 10, 7 * alto // 10))
                else:
                    pygame.draw.rect(ventana, (125, 125, 125),(20 + (20 + 7 * alto // 10) * i, alto // 7, 7 * alto // 10, 7 * alto // 10))

                ventana.blit(self.iconos[i],(20 + (20 + 7 * alto // 10) * i, alto // 7))
                
        def dibuja_texto(texto):
            """Dibuja un texto dado"""
            return pygame.font.Font('freesansbold.ttf', 15).render(texto, True, (0, 0, 0))

        def dibuja_seleccion():
            """Dibuja la opcion que se seleccion, editar luego"""
            if self.estado is -1 : ventana.blit(dibuja_texto("Esto no deberia salir"), (0, 0))
            if self.estado is 0 : ventana.blit(dibuja_texto("Crea barrio"), (0, 0))
            if self.estado is 1 : ventana.blit(dibuja_texto("Crea tanque"), (0, 0))
            if self.estado is 2 : ventana.blit(dibuja_texto("Crear Tuberia"), (0, 0))
            if self.estado is 3 : ventana.blit(dibuja_texto("Desbordamiento tuberia"), (0, 0))
            if self.estado is 4 : ventana.blit(dibuja_texto("Cambiar ruta"), (0, 0))
            if self.estado is 5: ventana.blit(dibuja_texto("Muestra caminos"), (0, 0))
    
        #Si el menu se muestra
        if self.bool_mostrar_menu is True:
            dibuja_menu()
        #Si se selecciono una opcion
        elif self.bool_entra_seleccion is True:
            dibuja_seleccion()
        #Si no se esta en el menu
        elif self.bool_mostrar_menu is False and self.bool_entra_seleccion is False:
            ventana.blit(dibuja_texto("Q para el menu,X selecciona, Z retrocede"), (0, 0))
     
     
