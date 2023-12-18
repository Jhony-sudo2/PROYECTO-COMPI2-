import os
import pandas as pd
import xml.etree.ElementTree as ET
class CreateTable:
    def __init__(self, nombre, atributos):
        self.nombre= nombre
        self.atributos= atributos
        self.errores = ''
        self.rutatablas = ''

    def ejecutar(self, db):
        if self.verificar():
            print('pase')
            self.crearXml(db)
        print(self.errores)

    def crearXml(self,db):
        ruta_actual = os.getcwd()
        self.rutatablas = os.path.abspath(os.path.join(ruta_actual, '..', '..')) + '/databases/'+str(db)+'/Tables/'
        ruta = self.rutatablas +self.nombre
        data = {atributo.nombre: [atributo.tipo] for atributo in self.atributos}

        data2 = {f'Primaria_{i}': [atributo.nombre ]for i, atributo in enumerate(self.atributos, start=1)
                 if atributo.condicion is not None and atributo.condicion == 2
                 }
        data5 = {f'NOTNULL_{i}': [atributo.nombre] for i, atributo in enumerate(self.atributos, start=1)
                 if atributo.condicion is not None and atributo.condicion == 1
                 }

        data3 = [{'nombre': atributo.nombre,'tipo':atributo.tipo, 'tabla': atributo.foranea[0], 'referencia': atributo.foranea[1]}

                 for atributo in self.atributos if atributo.foranea is not None]

        data4 = {f'Foranea_{i}': [valor] for valor in data3 for i, valor in enumerate(data3,start=1)}
        try:
            if  data2:
                data.update(data2)
            if  data4:
                if self.verificarforaneas(data4):
                    data.update(data4)
                else:
                    return False
            if data5:
                data.update(data5)
            df = pd.DataFrame(data)
            xml_cadena = df.to_xml(index=False, root_name='Tabla', row_name='Estructura')
            os.mkdir(ruta)
            with open(ruta + '/estructura.xml', 'w') as archivo:
                archivo.write(xml_cadena)
            with open(ruta + '/datos.xml', 'w') as archivo:
                archivo.write('<?xml version="1.0" encoding="utf-8"?>\n<datos>\n \n</datos>')
        except FileExistsError:
            self.errores += f'la tabla {self.nombre} ya existe\n'


    def verificar(self):
        atributos = []
        for atributo in self.atributos:
            tupla = (atributo.nombre, atributo.tipo)
            atributos.append(tupla)
        tmp = set()
        # Verificar si los primeros elementos se repiten
        for tupla in atributos:
            primer_elemento = tupla[0]
            if primer_elemento in tmp:
                self.errores += 'Elementos repetidos en la declaracion de la tabla\n'
                return False
                break
            else:
                tmp.add(primer_elemento)
        return True

    def verificarforaneas(self,datos):
        print('verificando')
        for clave,lista_valores in datos.items():
            for foranea_info in lista_valores:
                nombre = foranea_info.get('nombre')
                tipo = foranea_info.get('tipo')
                tabla = foranea_info.get('tabla')
                referencia = foranea_info.get('referencia')
                if not self.buscarTabla(tabla,referencia,tipo):
                    return False
        return True

    def buscarTabla(self,tabla,referencia,tipo):
        tupla = (referencia,f'{tipo}')
        rutatmp = self.rutatablas + tabla
        if os.path.exists(rutatmp) and os.path.isdir(rutatmp):
            primarias = self.getTipos(referencia,rutatmp+'/estructura.xml')
            if tupla in primarias:
                return True
            else:
                self.errores += f'el campo {referencia} no es llave primaria en {tabla} o el tipo es incorrecto\n'
                return False
        else:
            self.errores += f"La tabla {tabla} no existe."
            return False

    def getTipos(self,referencia,ruta):
        tree = ET.parse(ruta)
        root = tree.getroot()
        primarias = []
        for estructura in root.findall('.//Estructura'):
            for subetiqueta in estructura:
                nombre_subetiqueta = subetiqueta.tag
                valor_subetiqueta = subetiqueta.text
                nuevoatrb = (nombre_subetiqueta, valor_subetiqueta)
                if (nombre_subetiqueta.startswith('Primaria')):
                    primarias.append((valor_subetiqueta,self.getTipo(valor_subetiqueta,root)))
        return primarias
    def getTipo(self,nombre,root):
        for estructura in root.findall('.//Estructura'):
            for subetiqueta in estructura:
                nombre_subetiqueta = subetiqueta.tag
                valor_subetiqueta = subetiqueta.text
                if (nombre_subetiqueta.startswith(nombre)):
                    return valor_subetiqueta

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