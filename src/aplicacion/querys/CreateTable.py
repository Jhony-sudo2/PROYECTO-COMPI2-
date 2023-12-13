import os
class CreateTable:
    def __init__(self, nombre, atributos):
        self.nombre= nombre
        self.atrbutos= atributos


    def crearTable(self):
        pass
        '''Aqui debemos crear un archivo con el nombre de la tabla'''

    def buscarDb(self):
        # Nombre de la carpeta que estás buscando
        nombre_carpeta_buscada = "mi_carpeta"

        # Ruta del directorio donde deseas buscar
        directorio_buscado = "/ruta/del/directorio/donde/buscar"

        # Construye la ruta completa
        ruta_completa = os.path.join(directorio_buscado, nombre_carpeta_buscada)

        # Verifica si la carpeta existe
        if os.path.exists(ruta_completa):
            print(f"La carpeta {nombre_carpeta_buscada} existe en {directorio_buscado}.")
        else:
            print(f"La carpeta {nombre_carpeta_buscada} no existe en {directorio_buscado}.")