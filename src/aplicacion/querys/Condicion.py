import pandas as pd
import xml.dom.minidom
from src.aplicacion.querys.Basicos import *
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse

class Condicion:
    def __init__(self, id, signo, val2,tablasimbolos=None):
        self.id = id
        self.signo = signo
        self.val2 = val2
        self.val1 = ''
        self.tablasimbolos = tablasimbolos

    def validar(self, val1):
        if isinstance(self.val2, str) and (
                self.val2.startswith("'") and self.val2.endswith("'") or self.val2.startswith('"') and self.val2.endswith('"')):
            self.val2 = self.val2.strip('\'"')
        print(f'comparando {val1} - {self.signo} - { self.val2}')
        self.val1= val1
        if self.signo == '=':
            if self.val1 == self.val2:
                print('true')
                return True
        if self.signo == '=!':
            if self.val1 == self.val2:
                print('true')
                return True
        if self.signo == '<':
            if self.val1 < self.val2:
                print('true')
                return True
        if self.signo == '>':
            if self.val1 < self.val2:
                print('true')
                return True
        if self.signo == '>=':
            if self.val1 >= self.val2:
                print('true')
                return True
        if self.signo == '<=':
            if self.val1 <= self.val2:
                print('true')
                return True

    def getId(self):
        return self.id
    def getVa2(self):
        return getvalores(self.val2, self.tablasimbolos)
    def obtenerColumna(self, ruta, select):
        # Abrir el archivo XML
        tree = parse(ruta + select)
        root = tree.getroot()
        existeColumna = False

        # Buscar la columna y eliminarla
        for fila in root.findall('datos'):
            for child in fila:
                if child.tag == self.id:
                    valor= child.text
                    return valor
                    break

                else:
                    return False
        if existeColumna is False:
            self.error= f'Error la columna {self.idColumna} no exite en la tabla, por loo tanto no se puede eliminar'

        # Guardar los cambios en el archivo XML
        tree.write(ruta + select)

        return True

    def convertirCadenas(self, cadenas):
        for etiqueta, valor in cadenas.items():
            valor= getvalores(valor, self.tablasimbolos)
        return  cadenas;