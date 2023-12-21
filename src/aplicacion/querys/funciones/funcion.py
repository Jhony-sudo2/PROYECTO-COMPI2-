from src.aplicacion.querys.Basicos import *
import xml.etree.ElementTree as ET
import os
class funcion:
    def __init__(self,nombre,parametros,acciones,tiporetorno):
        self.nombre = nombre
        self.parametros = parametros
        self.acciones = acciones
        self.errores = ''
        self.tiporetorno = tiporetorno

    def ejecutar(self,db):
        print(f'creando funcion {self.nombre} EN LA BASE: {db}')
        if not self.verificar(db):
            print('generando xml')
            self.generarxml()
        else:
            self.errores += f' la funcion: {self.nombre} ya existe en la base de datos: {db}'

    def verificar(self,db):
        ruta = getrutafunciones(db)
        ruta2 = ruta + self.nombre + '.xml'
        return os.path.exists(ruta2)

    def generarxml(self):
        print('generando xml de la funcion')
        funcion = ET.Element('funcion')
        nombre = ET.SubElement(funcion,'nombre')
        nombre.text = self.nombre
        for op in self.acciones:
            funcion.append(op.obtenerxml())

        tree = ET.ElementTree(funcion)
        root = tree.getroot()  # Accede al elemento raíz
        xml_string = ET.tostring(root, encoding='utf-8')  # Especifica el encoding
        print(xml_string)





