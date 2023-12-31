import os

from src.aplicacion.querys.Operacion import Operacion


class CreateDB(Operacion):
    pass
    def __init__(self, nombreTable,linea):
        self.nombreTable= nombreTable
        self.errores = ''
        self.linea = linea


    def ejecutar(self, db):
        print('Creando DB')
        self.crearDB()

    def crearDB(self):
        # Especifica la ruta de la carpeta que deseas crear
        nombre_carpeta = self.nombreTable
        #ruta_carpeta = "/home/jhony/ING/SEXTO/COMPI 2/VAQUERAS/python/src/databases/" + nombre_carpeta

        ruta_actual = os.getcwd()
        ruta_carpeta = os.path.abspath(os.path.join(ruta_actual, '..', '..')) + '/databases/'+ nombre_carpeta

        # Verifica si la carpeta ya existe
        if not os.path.exists(ruta_carpeta):
            # Crea la carpeta
            os.makedirs(ruta_carpeta)
            print(f"Se ha creado la carpeta: {ruta_carpeta}")
            os.makedirs(ruta_carpeta+'/Tables')
            os.makedirs(ruta_carpeta + '/Funciones')
            os.makedirs(ruta_carpeta + '/Procedimientos')
        else:
            self.errores += f"Error: La Base de datos {self.nombreTable} ya existe. linea: { self.linea} \n"



