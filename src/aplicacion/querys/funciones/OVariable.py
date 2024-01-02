from src.aplicacion.querys.funciones.Variable import Variable
import xml.etree.ElementTree as ET

class OVariable:
    def __init__(self,variable:Variable,linea,tablasimbolos=None):
        self.variable = variable
        self.tablasimbolos = tablasimbolos
        self.errores = ''
        self.linea = linea

    def ejecutar(self,db):
        if self.buscar():
            self.tablasimbolos.append(self.variable)

    def buscar(self):
        for tmp in self.tablasimbolos:
            if tmp.nombre == self.variable.nombre:
                self.errores += f'ERROR SEMANTICO: la variable {self.variable} ya existe  linea {self.linea}'
                return False
        return True

    def obtenerxml(self):
        print('generando xml de una variable')
        variable = ET.Element('variable')
        nombre = ET.SubElement(variable,'nombre')
        nombre.text = self.nombre
        tipo = ET.SubElement(variable,'tipo')
        tipo.text = str(self.tipo)
        return variable