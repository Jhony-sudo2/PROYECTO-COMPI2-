from xml.dom import minidom

from src.aplicacion.querys.Basicos import *
import xml.etree.ElementTree as ET
import os
class funcion:
    def __init__(self,nombre,parametros,acciones,tiporetorno,retorno,tipo,tablafunciones=None,db = None):
        self.nombre = nombre
        self.parametros = parametros
        self.acciones = acciones
        self.errores = ''
        self.tiporetorno = tiporetorno
        self.tablasimbolos = []
        self.tablafunciones = tablafunciones
        self.db = db
        self.retorno = retorno
        self.tipo = tipo
    def ejecutar(self,db):
        if self.buscar(db):
            print(f'Guardando funcion  {self.nombre} EN LA BASE: {db}')
            fn = funcion(self.nombre,self.parametros,self.acciones,self.tiporetorno,self.retorno,self.tipo,db=db)
            self.tablafunciones.append(fn)


    def buscar(self,db):
        for tmp in self.tablafunciones:
            if tmp.nombre == self.nombre and tmp.db == db and tmp.tipo == self.tipo:
                if self.tipo == 1:
                    self.errores += f' ERROR: la funcion: {self.nombre} ya existe en la base de datos: {db}'
                else:
                    self.errores += f' ERROR: El procedimiento: {self.nombre} ya existe en la base de datos: {db}'
                return False
        return True

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
        formatted_xml = minidom.parseString(xml_string).toprettyxml(indent="\t")
        lines = formatted_xml.split('\n')
        final = '\n'.join(line for line in lines if line.strip())
        print(final)





