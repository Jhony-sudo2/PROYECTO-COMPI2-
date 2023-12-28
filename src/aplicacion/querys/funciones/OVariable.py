from src.aplicacion.querys.funciones.Variable import Variable
import xml.etree.ElementTree as ET

class OVariable:
    def __init__(self,variable:Variable,tablasimbolos=None):
        self.variable = variable
        self.tablasimbolos = tablasimbolos


    def ejecutar(self,db):
        print(f'nombre variable: {self.variable.nombre}')
        print(f'valor: {self.variable.valor}')
        pass

    def ingresarvariable(self):
        pass

    def asignarvalor(self):
        pass
    def obtenerxml(self):
        print('generando xml de una variable')
        variable = ET.Element('variable')
        nombre = ET.SubElement(variable,'nombre')
        nombre.text = self.nombre
        tipo = ET.SubElement(variable,'tipo')
        tipo.text = str(self.tipo)
        return variable