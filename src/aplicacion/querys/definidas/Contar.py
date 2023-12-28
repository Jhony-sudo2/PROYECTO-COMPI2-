from src.aplicacion.querys.Basicos import getrutatablas, getrutadatos

import pandas as pd
class Contar:
    def __init__(self,tabla,columna):
        self.columna = columna
        self.tabla = tabla
        self.errores = ''
        self.resultado = ''

    def ejecutar(self,db):
        print('contar')
        ruta = getrutatablas(db)
        ruta = getrutadatos(ruta,self.tabla)
        try:
            archivo = open(ruta,'r')
            pf = pd.read_xml(archivo)
            self.resultado += str(len(pf)) + '\n'
            return len(pf)
        except FileNotFoundError:
            self.errores += f'La tabla {self.tabla} no existe'