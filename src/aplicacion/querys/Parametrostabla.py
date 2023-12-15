class Parametrostabla:
    def __init__(self,nombre,tipo,condicion=None,foranea=None):
        self.nombre = nombre
        self.tipo = tipo
        self.condicion = condicion
        self.foranea = foranea


    def imprimir(self):
        print('-------parametro-----')
        print(self.nombre)
        print(self.tipo)
        if(self.condicion != None):
            print(self.condicion)
        if(self.foranea != None):
            print(self.foranea[0])
            print(self.foranea[1])
