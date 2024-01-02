from src.aplicacion.querys.Basicos import getrutabase
import os

class Usar:
    def __init__(self,nombre,linea):
        self.nombre = nombre
        self.errores = ''
        self.nueva = ''
        self.linea = linea
    def ejecutar(self,tmp):
        print('cambiando base de datos')
        if not self.verificar(self.nombre):
            self.errores += f'ERRO EN USAR: la base de datos {self.nombre} no existe  linea: {self.linea}\n'
        else:
            self.nueva = self.nombre

    def verificar(self,db):
        ruta = getrutabase(db)
        return os.path.exists(ruta)