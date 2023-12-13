import os
class CreateDB:
    pass
    def __init__(self, nombreTable):
        self.nombreTable= nombreTable


    def crearDB(self):
        # Especifica la ruta de la carpeta que deseas crear
        nombre_carpeta = self.nombreTable
        ruta_carpeta = "/home/estuardo/Documentos/Sexto y septimo semestre/Compi2EVD-2023/Curso/Proyecto/PROYECTO-COMPI2-/src/databases/" + nombre_carpeta

        # Verifica si la carpeta ya existe
        if not os.path.exists(ruta_carpeta):
            # Crea la carpeta
            os.makedirs(ruta_carpeta)
            print(f"Se ha creado la carpeta: {ruta_carpeta}")
        else:
            print(f"La carpeta {ruta_carpeta} ya existe.")
        '''Aqui debemos crear unA carpeta con el nombre de la tabla'''


