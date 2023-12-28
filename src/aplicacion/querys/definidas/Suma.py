from src.aplicacion.querys.Basicos import getrutatablas, getrutadatos
import pandas as pd

class Suma:
    def __init__(self,tabla,columna):
        self.tabla = tabla
        self.columna = columna
        self.errores = ''
        self.resultado = ''

    def ejecutar(self,db):
        print('ejecutando suma de datos')
        ruta = getrutatablas(db)
        ruta = getrutadatos(ruta, self.tabla)
        try:
            archivo = open(ruta,'r')
            df = pd.read_xml(archivo)
            tmp = df[self.columna]
            try:
                suma = tmp.sum()
                print(suma)
                self.resultado += str(suma) + ' \n'
            except ValueError:
                # Si hay errores, al menos un valor no es un entero
                self.errores += f"La columna '{self.columna}' no contiene solo valores enteros."
        except Exception as e:
            self.errores += ' Error en Suma de datos'
        pass