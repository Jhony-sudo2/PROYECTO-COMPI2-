class Concatena:
    def __init__(self,valor1,valor2):
        self.valor1 = valor1
        self.valor2 = valor2
        self.errores = ''
        self.resultado = ''
    def ejecutar(self,db):
        self.resultado = str(self.valor1) + str(self.valor2)
        return self.resultado

