import os
import pandas as pd
import xml.etree.ElementTree as ET
class CreateTable:
    def __init__(self, nombre, atributos):
        self.nombre= nombre
        self.atributos= atributos


    def ejecutar(self, db):
        print('ingresando nueva tabla')
        self.crearXml(db)
    def crearTable(self):
        pass
        '''Aqui debemos crear un archivo con el nombre de la tabla'''


    def crearXml(self,db):
        ruta_actual = os.getcwd()
        ruta = os.path.abspath(os.path.join(ruta_actual, '..', '..')) + '/databases/'+str(db)+'/Tables/'
        print('creando archivo XML en: ' + ruta)
        data = {atributo.nombre: [atributo.tipo] for atributo in self.atributos}

        data2 = {f'Primaria_{i}': [atributo.nombre ]for i, atributo in enumerate(self.atributos, start=1)
                 if atributo.condicion is not None and atributo.condicion == 2
                 }
        data5 = {f'NOTNULL_{i}': [atributo.nombre] for i, atributo in enumerate(self.atributos, start=1)
                 if atributo.condicion is not None and atributo.condicion == 1
                 }

        data3 = [{'nombre': atributo.nombre, 'tabla': atributo.foranea[0], 'referencia': atributo.foranea[1]}

                 for atributo in self.atributos if atributo.foranea is not None]

        data4 = {f'Foranea_{i}': [valor] for valor in data3 for i, valor in enumerate(data3,start=1)}

        if  data2:
            data.update(data2)
        if  data4:
            data.update(data4)
        if data5:
            data.update(data5)
        df = pd.DataFrame(data)

        xml_cadena = df.to_xml(index=False, root_name='Tabla', row_name='Estructura')

        with open(ruta + self.nombre+'.xml', 'w') as archivo:
            archivo.write(xml_cadena)


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