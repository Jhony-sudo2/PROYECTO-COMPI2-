from src.aplicacion.querys.Basicos import getvalores


class SetVariable:
    def __init__(self,nombre,valor,linea,variable=None,tablasimbolos=None):
        self.nombre = nombre
        self.valor = valor
        self.tablasimbolos = tablasimbolos
        self.errores = ''
        self.linea = linea
        self.variable =variable


    def ejecutar(self,db):
        if self.buscarvariable():
            if isinstance(self.valor, str):
                self.getValor()
                self.variable.valor = self.valor
            elif isinstance(self.valor, object):
                self.valor.tablasimbolos = self.tablasimbolos
                self.valor = self.valor.ejecutar(db)

            print(f'asignando valor {self.valor}  a la variable {self.nombre}')
        else:
            self.errores += f'ERROR: la variable {self.nombre} no existe linea: {self.linea}'
            print(f'la variable {self.nombre} no existe linea: {self.linea}')
    def buscarvariable(self):
        for valor in self.tablasimbolos:
            if valor.nombre == self.nombre:
                self.variable = valor
                return True
        return False
    def getValor(self):
        self.valor = getvalores(self.valor,self.tablasimbolos)