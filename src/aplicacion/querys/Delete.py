import os
from xml.etree.ElementTree import parse


import pandas as pd

from src.aplicacion.querys.Basicos import existetabla, getvalores


class Delete():
    def __init__(self, idTabla, condiciones, tablasimbolos=None, errores=None):
        self.idTabla = idTabla
        self.condiciones = condiciones
        self.tablasimbolos = tablasimbolos
        self.errores = errores

    def ejecutar(self, db):
        ruta_actual = os.getcwd()
        ruta_tabla = os.path.abspath(
        os.path.join(ruta_actual, '..', '..')) + '/databases/' + db + '/Tables/' + self.idTabla
        existeTb = existetabla(ruta_tabla)
        if existeTb:
            self.obtnerBorarFila(ruta_tabla,"/datos.xml")
        else:
            self.errores= f'NO existe la tabla "{self.idTabla}" en la base de datos '


    def obtnerBorarFila(self, ruta, select):
        archivo = open(ruta + select, "r")
        df = pd.read_xml(archivo)
        # Cargar el archivo XML
        tree = parse(ruta + select)
        root = tree.getroot()
        seEncontroVal = False
        for persona in root.findall('elemento'):
            coincidencia = False

            for condicion in self.condiciones:
                print(condicion.id)

                valor_en_persona = persona.find(str(condicion.id)).text if persona.find(str(condicion.id)) is not None else  None
                val2=condicion.getVa2()
                if valor_en_persona is None:
                    self.errores=f'Error la columna {condicion.id} no existe en la tabla   '
                    return False
                if isinstance(val2, str) and (
                        val2.startswith("'") and val2.endswith("'") or val2.startswith('"') and val2.endswith('"')):
                    val2 =val2.strip('\'"')

                print(f'val {valor_en_persona} == {val2}')
                #if str(valor_en_persona) == str(val2):
                if condicion.validar(valor_en_persona):
                    coincidencia = True
                else:
                    coincidencia = False
                    break  # Si un val2 no coincide, podemos salir del bucle

            if coincidencia:
                root.remove(persona)
                elementos_a_eliminar = []  # Lista para almacenar elementos a eliminar
                seEncontroVal = True
                self.resultado = 'Se ha eliminado la tabla'

            else:
                break
        if seEncontroVal is False:
            self.errores = f'Error no se encontro el valor "{val2}" en la columna  "{condicion.id}"'

        archivo.close()

        # Escribir el árbol modificado de vuelta al archivo
        tree.write(ruta + select)

        return 0

