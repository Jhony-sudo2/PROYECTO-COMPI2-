from xml.dom import minidom

import pandas as pd
import xml.dom.minidom
from src.aplicacion.querys.Basicos import *
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse


class Alter():
    def __init__(self, idTable, agregar, idColumna, tipoColumna, esTabla=None):
        self.idTable = idTable
        self.agregar = agregar
        self.idColumna = idColumna
        self.tipoColumna = tipoColumna
        self.esTabla = esTabla

    def ejecutar(self, db):
        if self.agregar is True:
            # Agregamos codigo para agregar columna
            ruta_actual = os.getcwd()
            ruta_tabla = os.path.abspath(
                os.path.join(ruta_actual, '..', '..')) + '/databases/' + db + '/Tables/' + self.idTable
            existeTb = existetabla(ruta_tabla)
            if existeTb:
                if self.verificarColumna(ruta_tabla, '/estructura.xml') is False:
                    print('Se ingreso un nueo atributo a la tabla ')

        else:
            # agresgamos codigo para eliminar columna
            pass

    def buscarTabla(db, idTabla):
        pass

    # verificamos que la columna no exista en la estructura<
    def verificarColumna(self, ruta, select):
        existenAtributos = False
        archivo = open(ruta + select, "r")
        df = pd.read_xml(archivo)
        tree = parse(ruta + select)
        root = tree.getroot()
        for fila in root.findall('Estructura'):
            row = {}
            for child in fila:

                print(f'Columna {child.tag} == "{self.idColumna}"')
                if child.tag == self.idColumna:

                    existenAtributos = True
                    break
                else:
                    print('no existe el atributo')

                    existenAtributos = False
            if existenAtributos is True:
                self.errores = f'El la columna {self.idColumna} ya existe en la tabla'
                return False
            else:
                nuevo_elemento = ET.Element(self.idColumna)
                nuevo_elemento.text = str(self.tipoColumna)
                fila.append(nuevo_elemento)
                #fila.insert(0, nuevo_elemento)
                #fila.find('hijos').append(nuevo_elemento)
        archivo.close()

        tree.write(ruta + select)

    # agregamos la nueva columna a la tabla
    def agregarNuevacColumna(self, ruta, select):
        pass


