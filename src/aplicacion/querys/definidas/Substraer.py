class Substraer:
    def __init__(self,texto,inicio,fin,linea):
        self.texto=texto
        self.inicio=inicio
        self.fin=fin
        self.errores = ''
        self.resultado = ''
        self.linea = linea

    def ejecutar(self,db):
        self.texto = self.texto[1:-1]
        try:
            self.resultado = self.texto[self.inicio:self.fin]
            return self.resultado
        except Exception as e:
            self.errores= f'Indices fuera de rango en SUBSTRAER linea {self.linea}'
