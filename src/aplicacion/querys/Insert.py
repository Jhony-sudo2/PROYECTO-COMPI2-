import os
import re
from xml.dom import minidom
import xml.etree.ElementTree as ET
from datetime import datetime
import pandas as pd
from lxml import etree
import  json

from src.aplicacion.querys.Basicos import getvalores


class Insert:
    def __init__(self, titulos, valores,tabla,linea,tablasimbolos=None):
        self.errores = ''
        self.titulos=titulos
        self.valores= valores
        self.tabla= tabla
        self.ruta =''
        self.ruta2 = ''
        self.ruta3 = ''
        self.combinado = []
        self.tablasimbolos = tablasimbolos
        self.linea = linea
    def ejecutar(self,db):
        self.valorescambiados()
        ruta_actual = os.getcwd()
        self.ruta3 = os.path.abspath(os.path.join(ruta_actual, '..', '..')) + '/databases/' + db + '/Tables/'
        ruta = os.path.abspath(os.path.join(ruta_actual, '..', '..')) + '/databases/' + db + '/Tables/' + self.tabla + '/estructura.xml'
        self.ruta2 = os.path.abspath(os.path.join(ruta_actual, '..', '..')) + '/databases/' + db + '/Tables/' + self.tabla + '/datos.xml'
        self.ruta = ruta
        if self.existe():
            if len(self.valores) == len(self.titulos) and len(self.titulos) == len(set(self.titulos)):
                if self.verificar():
                    self.insertar()

            else:
                self.errores += f'error en envio de parametros en insert linea: {self.linea}\n'
        else:
            self.errores += f'ERROR La tabla {self.tabla} no existe  linea: {self.linea}\n'


    # METODO PARA CONVERTIR LAS CADENAS A VALORES.
    def valorescambiados(self):
        print(self.valores)
        for i in range(len(self.valores)):
            self.valores[i] = getvalores(self.valores[i], self.tablasimbolos)
    def existe(self):
        return os.path.exists(self.ruta)

    def insertar(self):
        archivo = open(self.ruta2, "r")
        data = {titulo: valor for titulo, valor in zip(self.titulos, self.valores)}
        tree = etree.parse(archivo)
        root = tree.getroot()
        nuevo_elemento = etree.Element("elemento")
        for clave, valor in data.items():
            subelemento = etree.Element(clave)
            if isinstance(valor,str) and valor[0] =="'" and valor[-1] =="'":
                valor = valor[1:-1]
            subelemento.text = str(valor)
            nuevo_elemento.append(subelemento)

        root.append(nuevo_elemento)
        xml_string = etree.tostring(root, encoding='utf-8', xml_declaration=True)
        formatted_xml = minidom.parseString(xml_string).toprettyxml(indent="\t")
        lines = formatted_xml.split('\n')
        final = '\n'.join(line for line in lines if line.strip())
        with open(self.ruta2, 'wb') as f:
            f.write(final.encode('utf-8'))


    def verificar(self):
            tree = ET.parse(self.ruta)
            root = tree.getroot()
            atributos = []
            primarias = []
            foraneas = {}
            nonulos = []
            for estructura in root.findall('.//Estructura'):
                for subetiqueta in estructura:
                    nombre_subetiqueta = subetiqueta.tag
                    valor_subetiqueta = subetiqueta.text
                    nuevoatrb = (nombre_subetiqueta, valor_subetiqueta)
                    if(nombre_subetiqueta.startswith('Primaria')):
                        primarias.append(valor_subetiqueta)
                    elif (nombre_subetiqueta.startswith('Foranea')):
                        tmp = valor_subetiqueta.replace("'","\"")
                        valor = json.loads(tmp)
                        foraneas[f'{nombre_subetiqueta}']=[valor]
                    elif (nombre_subetiqueta.startswith('NOTNULL')):
                        nonulos.append(valor_subetiqueta)
                    else:
                        atributos.append(nuevoatrb)

            if self.verificaratributos(atributos):
                return self.verificarprimarias(primarias) and self.verificarforaneas(foraneas) and self.verificarnulos(nonulos)
            else:
                return False

    def verificarprimarias(self,primarias):
        if primarias:
            resultado = all(elemento in self.titulos for elemento in primarias)
            if resultado:
                combinados = [(primaria,self.valores[self.titulos.index(primaria)]) for primaria in primarias if
                                        primaria in self.titulos]
                return self.yaexiste(combinados)
            else:
                self.errores += f'ERROR: no viene la llave primaria  linea: {self.linea}\n'
                return False
        else:
            return True

    def verificarforaneas(self,foraneastmp):
        if foraneastmp:
            foraneas = self.getForaneas(foraneastmp)
            nombres = [tupla[0] for tupla in foraneas]
            resultado = all(elemento in self.titulos for elemento in nombres)
            if resultado:
                for index,tupla in enumerate(self.combinado):
                    for index2,nombre in enumerate(nombres):
                        if tupla[0] == nombre:
                            tabla = foraneas[index2][1]
                            idt = foraneas[index2][2]
                            valor = tupla[1]
                            if not self.verificarexistenciaforanea(tabla,idt,valor):
                                self.errores += f'la llave foranea {idt} = {valor} no se encuentra en la tabla {tabla}\n  linea: {self.linea}'
                                return False
                return True
            else:
                self.errores += f'Error inserts: no vienen los campos de llave foranea linea:   {self.linea}\n'
                return False
        else:
            return True

    def verificarexistenciaforanea(self,tabla,id,valor):
        archivo = open(self.ruta3+tabla+'/datos.xml', "r")
        df = pd.read_xml(archivo)
        resultado = df.query(f"{id} == {valor}")
        if resultado.empty: return False
        else: return True
    def getForaneas(self, tmp):
        foraneas = []
        for clave, lista_valores in tmp.items():
            for foranea_info in lista_valores:
                nombre = foranea_info.get('nombre')
                tipo = foranea_info.get('tipo')
                tabla = foranea_info.get('tabla')
                referencia = foranea_info.get('referencia')
                tupla = (nombre,tabla,referencia)
                foraneas.append(tupla)
        return foraneas
    def verificarnulos(self,nonulos):
        if nonulos:
            resultado = all(elemento in self.titulos for elemento in nonulos)
            return bool(resultado)
        else:
            return True

    def verificaratributos(self,atributos):
        resultado = all(titulo in [tupla[0] for tupla in atributos] for titulo in self.titulos)
        if resultado:
            return self.verificartipos(atributos)
        else:
            self.errores += f'ERROR: no coninciden los nombre con los atributos de la tabla  linea: {self.linea}\n'
            return False
        pass

    def verificartipos(self,atributos):
        self.combinado  = list(zip(self.titulos,self.valores))
        combinado = self.combinado

        for tupla in combinado:
            tipo = self.getTipo(tupla[1])
            esperado = self.getTipoesperado(tupla[0],atributos)
            if esperado == 2 and tipo == 1:
                tipo=2
            if tipo != esperado:
                self.errores += f'ERRRO INSERT: tipo de dato incorrecto para {tupla[0]}, se esperaba un tipo de dato {esperado} y se mando {tipo} \n  linea: {self.linea}'
                return False
        return True
    def getTipoesperado(self,titulo,atributos):
        for tmp in atributos:
            if titulo in tmp:
                return int(tmp[1])

    def getTipo(self,valor):
        if isinstance(valor, int):
            return 1
        elif isinstance(valor, float):
            return 2
        elif isinstance(valor, str) and valor.startswith("'") and valor.endswith("'"):
            if len(valor) == 22 and valor[1:11].replace('-', '').isdigit() and valor[12:22].replace(':', '').isdigit():
                try:
                    datetime.strptime(valor[1:-1], '%Y-%m-%d %H:%M')
                    return 6
                except ValueError:
                    return 4
            elif len(valor) == 12 and valor[1:5].isdigit() and valor[6:8].isdigit() and valor[9:11].isdigit():
                try:
                    datetime.strptime(valor[1:-1], '%Y-%m-%d')
                    return 5
                except ValueError:
                    return 4
            else:
                return 4
        else:
            return 0

    def yaexiste(self,combinado):
        #VERIFICANDO QUE NO EXISTA UN ELEMENTO CON LA MISMA LLAVE FORANEA
        archivo = open(self.ruta2, "r")
        try:
            df = pd.read_xml(archivo)
            mensaje = ''
            tmpresultado = False
            for tmp in combinado:
                resultado = df.query(f"{tmp[0]} == {tmp[1]}")
                if not resultado.empty:
                    mensaje += f'ERROR: ya hay un elemento {tmp[0]} = {tmp[1]} \n linea: {self.linea}'
                else:
                    tmpresultado = True
            if not tmpresultado:
                self.errores += mensaje
            return tmpresultado
        except Exception as e:
            return True

    def obtenerxml(self):
        print('generando xml de la instruccion')
        insert = ET.Element('insert')
        tabla = ET.SubElement(insert,'tabla')
        tabla.text =self.tabla
        for tmp in self.titulos:
            titulo = ET.SubElement(insert,'Titulo')
            titulo.text = tmp
        for tmp in self.valores:
            valor = ET.SubElement(insert,'Valor')
            valor.text = str(tmp)

        return insert