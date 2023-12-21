from src.aplicacion.querys.Basicos import *
import pandas as pd
class Select:
    def __init__(self,tabla):
        self.tabla = tabla
        self.errores = ''
        self.resultado = ''
        self.ruta = ''


    def ejecutar(self,db):
        self.ruta = getrutatablas(db)
        if existetabla(self.ruta + self.tabla):
            self.obtenerdatos()
        else:
            self.errores = f'la tabla {self.tabla} no existe\n'


    def obtenerdatos(self):
        rutatmp = getrutadatos(self.ruta, self.tabla)
        archivo = open(rutatmp, "r")
        df = pd.read_xml(archivo)
        self.resultado = df


    def getsalida(self):
        return self.resultado
