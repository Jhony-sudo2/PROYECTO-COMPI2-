import xml.etree.ElementTree as ET
class Variable:
    def __init__(self,nombre,tipo):
        self.nombre = nombre
        self.tipo = tipo

    def ejecutar(self,deb):
        print('Ejecutando variable')

    def obtenerxml(self):
        print('generando xml de una variable')
        variable = ET.Element('variable')
        nombre = ET.SubElement(variable,'nombre')
        nombre.text = self.nombre
        tipo = ET.SubElement(variable,'tipo')
        tipo.text = str(self.tipo)
        return variable