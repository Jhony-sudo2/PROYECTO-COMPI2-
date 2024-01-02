from src.aplicacion.querys.Basicos import getvalores


class Concatena:
    def __init__(self,valor1,valor2,tablasimbolos=None):
        self.valor1 = valor1
        self.valor2 = valor2
        self.errores = ''
        self.resultado = ''
        self.tablasimbolos = tablasimbolos
    def ejecutar(self,db):
        self.getValores()
        self.resultado = str(self.valor1) + str(self.valor2)
        return self.resultado

    def getValores(self):
        self.valor1 = getvalores(self.valor1, self.tablasimbolos)
        self.valor2 = getvalores(self.valor2, self.tablasimbolos)


