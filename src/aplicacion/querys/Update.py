import pandas as pd

from src.aplicacion.querys.Basicos import *
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse

class Update:
    #recibinos los val de cambiios queson los nuevos valores
    def __init__(self, tabla, cambios, actuales):
        self.errores = ''
        self.tabla= tabla
        self.cambios= cambios
        self.actualees=actuales
    def ejecutar(self, db):
        ruta_actual = os.getcwd()
        ruta_tabla = os.path.abspath( os.path.join(ruta_actual, '..', '..')) + '/databases/' + db + '/Tables/' + self.tabla
        existeTb=existetabla(ruta_tabla)
        if existeTb :
            #Debemos verificar si existen los campos que se quieren actualizar
            estructura=self.getEstructura(ruta_tabla, '/estructura.xml')
            validarActuales=self.verficarAtributos(ruta_tabla, '/estructura.xml')
            if estructura and validarActuales:
                #verificar que los datos que la condicion se cumpla
                self.obtnerDatosmodificar(ruta_tabla, '/datos.xml')
        else:
            self.errores= "ErrOR la tabla no exiate en  la base de datos"


    def getEstructura(self, ruta, select):
        existenAtributos= False
        archivo = open(ruta + select, "r")
        df = pd.read_xml(archivo)
        # Cargar el archivo XML
        tree = parse(ruta+select)
        root = tree.getroot()
        for persona in root.findall('Estructura'):
            row = {}
            for etiqueta in self.cambios.keys():
                for child in persona:
                    row[child.tag] = child.text
                    if child.tag ==etiqueta:
                        existenAtributos=True
                        break
                    else:
                        existenAtributos=False
                if existenAtributos is False:
                    self.errores = f'El atributo {etiqueta} no existe'
                    return False

            for child in persona:
                row[child.tag] = child.text

        #data.append(row)
        #df_from_xml = pd.DataFrame(data)
        return  existenAtributos

    def verficarAtributos(self, ruta, select):
        existenAtributos = False
        archivo = open(ruta + select, "r")
        df = pd.read_xml(archivo)
        tree = parse(ruta + select)
        root = tree.getroot()
        for persona in root.findall('Estructura'):
            row = {}
            for etiqueta in self.actualees.keys():
                for child in persona:
                    row[child.tag] = child.text
                    if child.tag == etiqueta:
                        existenAtributos = True
                        break
                    else:
                        print('no existe el atributo')
                        existenAtributos = False
                if existenAtributos is False:
                    self.errores = f'El atributo {etiqueta} no existe'
                    return False

        return existenAtributos

    def obtenerdatos(self):
        rutatmp = getrutadatos(self.ruta, self.tabla)
        archivo = open(rutatmp, "r")
        df = pd.read_xml(archivo)
        self.resultado = df

    def obtnerDatosmodificar(self, ruta, select):
        archivo = open(ruta + select, "r")
        df = pd.read_xml(archivo)
        # Cargar el archivo XML
        tree = parse(ruta + select)
        root = tree.getroot()
        seEncontroVal = False
        for persona in root.findall('elemento'):
            coincidencia = False

            for etiqueta, valor in self.actualees.items():
                valor_en_persona = persona.find(etiqueta).text if persona.find(etiqueta) is not None else None
                valor = valor.strip('\'"') if valor is not None else valor

                if valor_en_persona == valor:
                    coincidencia = True
                else:
                    coincidencia = False
                    print(f'El valor {valor} no se encontro')
                    break  # Si un valor no coincide, podemos salir del bucle

            if coincidencia:
                for etiqueta, nuevo_valor in self.cambios.items():
                    elemento = persona.find(etiqueta)
                    if elemento is not None:
                        nuevo_valor = str(nuevo_valor).strip('\'"')
                        elemento.text = nuevo_valor
                    persona = elemento
                seEncontroVal=True
            else:
                print(f"eroror el valor no se encontro")

        if seEncontroVal is False:
            self.errores = f'Error no se encontro el valor en la columnas especificadas'

        archivo.close()

        # Escribir el árbol modificado de vuelta al archivo
        tree.write(ruta + select)

        return 0

    def obtnervalorCambio(self, id):
        dic = {}
        dic= self.cambios
        return  dic[id]
