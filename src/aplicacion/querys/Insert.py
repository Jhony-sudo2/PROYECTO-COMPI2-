import os
from xml.dom import minidom
import xml.etree.ElementTree as ET
import pandas as pd
from lxml import etree
class Insert:
    def __init__(self, titulos, valores,tabla,db):
        self.errores = ''
        self.titulos=titulos
        self.valores= valores
        self.tabla= tabla
        ruta_actual = os.getcwd()
        ruta = os.path.abspath(os.path.join(ruta_actual, '..', '..')) + '/databases/'+db+'/'+tabla+'.xml'
        self.ruta = ruta
    def ejecutar(self):
        if self.existe():
            if self.verificar():
                self.insertar()
            else:
                print('Los datos no coinciden con el tipo')
        else:
            self.errores += ' La tabla no existe'

    def existe(self):
        print('verificando que la tabla exista: ' + self.ruta)
        return os.path.exists(self.ruta)

    def insertar(self):
        archivo = open(self.ruta, "r")
        data = {titulo: valor for titulo, valor in zip(self.titulos, self.valores)}
        tree = etree.parse(archivo)
        root = tree.getroot()
        nuevo_elemento = etree.Element("elemento")
        for clave, valor in data.items():
            subelemento = etree.Element(clave)
            subelemento.text = str(valor)
            nuevo_elemento.append(subelemento)

        root.append(nuevo_elemento)
        xml_string = etree.tostring(root, encoding='utf-8', xml_declaration=True)
        formatted_xml = minidom.parseString(xml_string).toprettyxml(indent="    ")

        with open(self.ruta, 'wb') as f:
            f.write(formatted_xml.encode('utf-8'))


    def verificar(self):
            print('Verificando tipos de datos en el archivo')
            tree = ET.parse(self.ruta)
            root = tree.getroot()
            atributos = []
            # Iterar sobre los elementos 'Estructura'
            for estructura in root.findall('.//Estructura'):
                # Iterar sobre las subetiquetas dentro de 'Estructura'
                for subetiqueta in estructura:
                    nombre_subetiqueta = subetiqueta.tag
                    valor_subetiqueta = subetiqueta.text
                    nuevoatrb = (nombre_subetiqueta, valor_subetiqueta)
                    atributos.append(nuevoatrb)
            return False