class Tanque:
    def __init__(self, x, y, num, capacidad_max,barrios):
        self.num= num
        self.x = x
        self.y = y
        self.capacidad_max=capacidad_max
        self.capacidad_actual=0
        self.barrios=barrios

    def __str__(self):
        return "num="+str(self.num)+",x="+str(self.x)+",y="+str(self.y)+",capacidad"+str(self.capacidad_max)
    
    def agrega_barrio(self,barrio):
        self.barrios.append(barrio)
        print("Agrego a "+str(self.num))