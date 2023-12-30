import pandas as pd

from src.aplicacion.querys.Basicos import *
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse

class Update:
    #recibinos los val de cambiios queson los nuevos valores
    def __init__(self, tabla, cambios, actuales, signo=None, tablasimbolos=None):
        self.errores = ''
        self.tabla= tabla
        self.cambios= cambios
        self.actualees=actuales
        self.signo= signo
        self.tablasimbolos=tablasimbolos
        self.resultado = ''
    def ejecutar(self, db):
        ruta_actual = os.getcwd()
        ruta_tabla = os.path.abspath( os.path.join(ruta_actual, '..', '..')) + '/databases/' + db + '/Tables/' + self.tabla
        existeTb=existetabla(ruta_tabla)
        #self.actualees=self.convertirCadenas(self.actualees)
        self.cambios=self.convertirCadenas(self.cambios)
        if existeTb :
            #Debemos verificar si existen los campos que se quieren actualizar
            estructura=self.getEstructura(ruta_tabla, '/estructura.xml')
            validarActuales=self.verficarAtributos(ruta_tabla, '/estructura.xml')
            if estructura and validarActuales:
                #verificar que los datos que la condicion se cumpla
                self.obtnerDatosmodificar(ruta_tabla, '/datos.xml')
        else:
            self.errores= "ErrOR la tabla no exiate en  la base de datos"


    #Verifica que los atributos que  se quieran actualizar esten en la estructura de la tabla
    def getEstructura(self, ruta, select):
        existenAtributos= False
        tipoIgual=False
        archivo = open(ruta + select, "r")
        df = pd.read_xml(archivo)
        # Cargar el archivo XML
        tree = parse(ruta+select)
        root = tree.getroot()
        for persona in root.findall('Estructura'):
            row = {}
            for etiqueta,valor in self.cambios.items():
                print(f'Etiqueta: {etiqueta}  Valor: {type(valor)}')
                for child in persona:
                    row[child.tag] = child.text
                    print(f'Etiqueta: {etiqueta}  tag: {child.tag}')
                    valor=(valor)
                    if child.tag ==etiqueta:
                        '''print(f'{self.getTipo(valor[0])} : {child.text}')
                        if self.getTipo(valor[0])== child.text:
                            tipoIgual=True
                        else:
                            tipoIgual=False
                            self.errores=f'Tipo de dato no coincide'
                            return False'''
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

    #verfica que los atributos que estan de condicion existan enla tabla
    def verficarAtributos(self, ruta, select):
        existenAtributos = False
        archivo = open(ruta + select, "r")
        df = pd.read_xml(archivo)
        tree = parse(ruta + select)
        root = tree.getroot()
        print(type(self.actualees))
        for persona in root.findall('Estructura'):
            row = {}
            for condicion in self.actualees:
                id= str(condicion.getId())
                for child in persona:
                    row[child.tag] = child.text
                    if child.tag == id:

                        existenAtributos = True
                        break
                    else:
                        print('no existe el atributo')
                        existenAtributos = False
                if existenAtributos is False:
                    self.errores = f'El atributo {id} no existe'
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

            for condicion in self.actualees:
                etiqueta=str(condicion.getId())
                valor=condicion.getVa2()
                valor_en_persona = persona.find(etiqueta).text if persona.find(etiqueta) is not None else None
                if isinstance(valor, str) and (
                        valor.startswith("'") and valor.endswith("'") or valor.startswith('"') and valor.endswith('"')):
                    valor = valor.strip('\'"')

                print(f'val {valor_en_persona} == {valor}')
                #if str(valor_en_persona) == str(valor):
                if condicion.validar(valor_en_persona):
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
                self.resultado = 'Se ha actualizado la tabla'
            else:
                break
                print(f"eroror el valor {valor} no se encontro")

        if seEncontroVal is False:
            self.errores = f'Error no se encontro el valor {valor}  en la columnas especificadas'

        archivo.close()

        # Escribir el árbol modificado de vuelta al archivo
        tree.write(ruta + select)

        return 0


    def convertirCadenas(self, cadenas):
        for etiqueta, valor in cadenas.items():
            valor= getvalores(valor, self.tablasimbolos)
        return  cadenas;


    def valorescambiados(self, valores):
        print(valores)
        for i in range(len(valores)):
            valores[i] = getvalores(valores[i], self.tablasimbolos)
        print('valores cambiados')
        print(valores)
        return valores

    def getTipo(self, valor):
        print(f"Valor recibido en getTipo: {valor}")

        if isinstance(valor, int):
            print("Tipo 1: int")
            return 1
        elif isinstance(valor, float):
            print("Tipo 2: float")
            return 2
        elif isinstance(valor, str) and valor.startswith("'") and valor.endswith("'"):
            if len(valor) == 22 and valor[1:11].replace('-', '').isdigit() and valor[12:22].replace(':', '').isdigit():
                try:
                    datetime.strptime(valor[1:-1], '%Y-%m-%d %H:%M')
                    print("Tipo 6: datetime")
                    return 6
                except ValueError:
                    print("Tipo 4: formato incorrecto para datetime")
                    return 4
            elif len(valor) == 12 and valor[1:5].isdigit() and valor[6:8].isdigit() and valor[9:11].isdigit():
                try:
                    datetime.strptime(valor[1:-1], '%Y-%m-%d')
                    print("Tipo 5: fecha")
                    return 5
                except ValueError:
                    print("Tipo 4: formato incorrecto para fecha")
                    return 4
            else:
                print("Tipo 4: formato incorrecto para cadena")
                return 4
        else:
            print("Tipo 0: no reconocido")
            return 0

