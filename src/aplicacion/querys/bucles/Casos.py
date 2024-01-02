from src.aplicacion.querys.bucles.Caso import Caso


class Casos:
    def __init__(self,listacasos,tablasimbolos=None,extra=None):
        self.listacasos:list[Caso]=listacasos
        self.tablasimbolos= tablasimbolos
        self.errores = ''



    def ejecutar(self,db):
        for tmp in self.listacasos:
            self.ejecutarcaso(tmp.condiciones,tmp.acciones)

    def ejecutarcaso(self,condiciones,acciones):
        print('ejecutando caso individual')

