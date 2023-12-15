import os

from src.aplicacion.querys.Operacion import Operacion


class CreateDB(Operacion):
    pass
    def __init__(self, nombreTable):
        self.nombreTable= nombreTable



    def ejecutar(self):
        print('Creando DB')
        self.crearDB()

    def crearDB(self):
        # Especifica la ruta de la carpeta que deseas crear
        nombre_carpeta = self.nombreTable
        ruta_carpeta = "/home/jhony/ING/SEXTO/COMPI 2/VAQUERAS/python/src/databases/" + nombre_carpeta

        # Verifica si la carpeta ya existe
        if not os.path.exists(ruta_carpeta):
            # Crea la carpeta
            os.makedirs(ruta_carpeta)
            print(f"Se ha creado la carpeta: {ruta_carpeta}")
        else:
            print(f"La carpeta {ruta_carpeta} ya existe.")
        '''Aqui debemos crear unA carpeta con el nombre de la tabla'''


