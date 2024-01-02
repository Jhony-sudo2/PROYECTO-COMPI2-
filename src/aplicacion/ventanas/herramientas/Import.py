import os
import xml.etree.ElementTree as ET
from src.aplicacion.querys.Basicos import existetabla


class Import():
    def __init__(self, table, db):
        self.table = table
        self.db = db

    def import_data(self):
        ruta_actual = os.getcwd()
        ruta_tabla = os.path.abspath(
            os.path.join(ruta_actual, '..', '..')) + '/databases/' + self.db + '/Tables/' + self.tabla
        existeTb = existetabla(ruta_tabla)
        tree = ET.parse(ruta_tabla+'/datos.xml')
        root = tree.getroot()

        columnas = [child.tag for child in root.find('elemento')]

        # Iterar sobre los elementos y construir las consultas SQL
        for elemento in root.findall('elemento'):
            valores = [elemento.find(columna).text for columna in columnas]

            # Construir la consulta SQL
            sql_query = f"INSERT INTO {self.table} ({','.join(columnas)}) VALUES ({','.join(valores)});"

            # Imprimir la consulta SQL
            print(sql_query)