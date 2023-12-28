class SetVariable:
    def __init__(self,nombre,valor,tablasimbolos=None):
        self.nombre = nombre
        self.valor = valor;
        self.tablasimbolos = tablasimbolos;\
        self.errores = ''


    def ejecutar(self,db):
        print(self.valor)
