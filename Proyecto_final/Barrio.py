class Barrio:
    def __init__(self, x, y, num=0,sprite=[0,0,0,0]):
        self.pos = [(x, y), (x+1, y), (x, y+1), (x+1, y+1)]
        self.sprite=sprite
        self.num=num
    
    def __str__(self):
        return "barrio num="+str(self.num)