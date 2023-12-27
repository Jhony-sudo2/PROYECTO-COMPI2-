import os.path

from src.aplicacion.querys.Basicos import *
import pandas as pd
import xml.etree.ElementTree as ET

class Select:
    def __init__(self,tablas,columnas,condiciones=None):
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        self.tabla = tablas
        self.errores = ''
        self.resultado = ''
        self.ruta = ''
        self.columnas = columnas
        self.condiciones = condiciones
        self.tablasi = []
        self.columnasi = []
        self.datos = {}

    def ejecutar(self,db):
        if self.verificartablas(db,self.tabla):
            if self.verificarcolumnas(self.columnas):
                if self.columnas[0] == '*':
                    if self.condiciones == None:
                        self.selectbasico(db)
                    else:
                        self.concondiciones(db)
                else:
                    if self.condiciones == None:
                        self.columnaespecifica(db)
                    else:
                        self.combinado(db)



    def verificartablas(self,db,tablas):
        self.ruta = getrutatablas(db)
        for elemento in tablas:
            if not os.path.exists(self.ruta+'/'+elemento):
                self.errores += f' la tabla: {elemento} no existe en la base de datos {db}'
                return False
        return True

    def verificarcolumnas(self,columnas):
        self.tablasi.clear()
        self.columnasi.clear()
        if columnas[0] != '*':
            for elemento in columnas:
                tupla = elemento.split('.')
                try:
                    self.tablasi.append(tupla[0])
                    self.columnasi.append(tupla[1])
                except IndexError:
                    self.errores += f'el elemento {tupla}  no esta asociado con ninguna tabla  el formato es tabla.atributo para las tablas \n'
            verificacion = all(tabla in self.tabla for tabla in self.tablasi)
            if verificacion:
                for index,elemento in enumerate(self.columnasi):
                    if not self.verificarcolumna(self.tablasi[index],elemento):
                        return False
                return True
            else:
                self.errores += 'hay tablas no declaras en la seccion de las columnas \n'
                return False
        else:
            return True

    def verificarcolumna(self,tabla,atributo):
        ruta = self.ruta + tabla + '/estructura.xml'
        tree = ET.parse(ruta)
        root = tree.getroot()
        for estructura in root.findall('.//Estructura'):
            for subetiqueta in estructura:
                nombre_subetiqueta = subetiqueta.tag
                if nombre_subetiqueta == atributo:
                    return True
        self.errores += f'el atributo {atributo} no existe en la tabla {tabla}'
        return False


    ###GENERACION DE LOS RESULTADOS
    ##BASICO
    def selectbasico(self,db):
        self.ruta = getrutatablas(db)
        if len(self.tabla) == 1:
            self.obtenerdatos(self.tabla[0])
        else:
            for elemento in self.tabla:
                self.obtenerdatos(elemento)

    def concondiciones(self,db):
        if len(self.tabla) > 1:
            explogicas = self.condiciones[1::2]
            tmp = self.condiciones[0::2]
        else:
            self.datosconrestriccioens(db)


    def getcadenarestriccion(self):
        cadenatmp = ''
        for elemento in self.condiciones:
            if len(elemento) == 3:
                if elemento[1] == '=':
                    cadenatmp += str (elemento[0]) + '== ' + str(elemento[2])
                else:
                    cadenatmp += str(elemento[0]) + str(elemento[1]) + str(elemento[2])
            else:
                if elemento == '&&':
                    cadenatmp += ' ' + '& '
                elif elemento == '||':
                    cadenatmp += ' | '
        return cadenatmp

    def columnaespecifica(self,db):
        for index,elemento in enumerate(self.columnas):
            self.obtenerdatosespecificos(elemento,index)
        longitud_maxima = max(len(v) for v in self.datos.values())
        datos_actualizados = {k: v + [None] * (longitud_maxima - len(v)) for k, v in self.datos.items()}
        df = pd.DataFrame(datos_actualizados)
        self.resultado += f'****{self.tabla[0]}****\n' + str(df) + '\n'

    def obtenerdatosespecificos(self,campo,indice):
        tabla = self.tablasi[indice]
        columna = self.columnasi[indice]
        rutatmp = getrutadatos(self.ruta,tabla)
        archivo = open(rutatmp,"r")
        df = pd.read_xml(archivo)
        resultado = df[columna]
        datostmp = []
        for dato in resultado:
            datostmp.append(dato)
        newdiccionario = {campo:datostmp}
        self.datos.update(newdiccionario)

    ##SELECT CON VARIAS TABLAS Y CONDICIONES
    def combinado(self,db):
        tmp = self.obtenercondiciones()
        if self.verificarcolumnas(tmp):
            Frames = self.obtenerframes(self.tabla)
            Combinados = []
            for tmp in self.condiciones:
                if len(tmp) == 3:
                    tmp1 = tmp[0].split('.')
                    tmp2 = tmp[2].split('.')
                    tabla1 = tmp1[0]
                    atr1 = tmp1[1]
                    tabla2 = tmp2[0]
                    atr2 = tmp2[1]
                    Frametmp = self.obtenerFrames(tabla1,tabla2,Frames)
                    df_resultado = pd.merge(Frametmp[0],Frametmp[1],left_on=atr1,right_on=atr2)
                    if not df_resultado.empty:
                        Combinados.append(df_resultado)

            resultado = Combinados[0]

            # Itera sobre los DataFrames en Combinado para realizar la fusión
            for df in Combinados[1:]:
                # Encuentra las columnas comunes
                columnas_comunes = resultado.columns.intersection(df.columns).tolist()
                # Realiza la fusión basada en las columnas que tienen en común
                resultado = pd.merge(resultado, df, how='inner', on=columnas_comunes)
            self.verificarcolumnas(self.columnas)

            for tmp in self.columnasi:
                valores  = resultado[tmp]
                datostmp = []
                for dato in valores:
                    datostmp.append(dato)
                newdiccionario = {tmp: datostmp}
                self.datos.update(newdiccionario)
            resultado = pd.DataFrame(self.datos)
            print(resultado)

    def obtenerFrames(self,tabla1,tabla2,Frames):
        frm = []
        for tmp in Frames:
            if tabla1 == tmp[1]:
                frm.insert(0,tmp[0])
            if tabla2 == tmp[1]:
                frm.insert(1,tmp[0])

        return frm

    def obtenercondiciones(self):
        condiciones = []
        for elemento in self.condiciones:
            if isinstance(elemento, tuple):
                condiciones.append(elemento[0])
                condiciones.append(elemento[2])
        return condiciones
    def obtenerframes(self,tabla):
        Frames = []
        for elemento in tabla:
            ruta = getrutadatos(self.ruta,elemento)
            archivo = open(ruta,"r")
            df = pd.read_xml(archivo)
            Frames.append((df,elemento))
        return Frames

    #RESTRICCIONES UNA TABLA
    def datosconrestriccioens(self,db):
        self.ruta = getrutatablas(db)
        restriccion = self.getcadenarestriccion()
        rutatmp = getrutadatos(self.ruta, self.tabla[0])
        archivo = open(rutatmp, "r")
        df = pd.read_xml(archivo)
        try:
            resultado = df.query(restriccion)
            self.resultado += f'****{self.tabla[0]}****\n' + str(resultado) + '\n'
        except Exception as e:
            self.errores += ' campo no existe en la tabla'
    def obtenerdatos(self,tabla):
        rutatmp = getrutadatos(self.ruta,tabla)
        archivo = open(rutatmp, "r")
        df = pd.read_xml(archivo)
        self.resultado += f'****{tabla}****' + '\n' + str(df) + '\n'
        return df

    def getsalida(self):
        return self.resultado
