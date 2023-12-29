import ast
import os

from src.aplicacion.querys.Basicos import getrutatablas, existetabla
import xml.etree.ElementTree as ET

class Trucate():
    def __init__(self, idTable, errores=None):
        self.idTable=idTable
        self.errores=errores
        self.tablaRef=''
        self.resultado = ''


    def ejecutar(self, db):
        #buscarTable
        ruta=getrutatablas(db)+self.idTable
        if existetabla(ruta):
            #verificamos que sus valores no sean llavees foraneas de otras tablas
            noesForanea=self.verificarForaneas(getrutatablas(db))
            if noesForanea is False:
                ruta2= ruta+'/datos.xml'
                #eliminamos los datos de la tabla
                seelimino=self.borrar_elementos(ruta2)
                if seelimino:
                    print('Se borro el contenido de la tabla')
                    self.resultado = f'Se vacio el contenido de la tabla {self.idTable}'
                else:
                    print('No se borro el contenido de la tabla')
            else:
                print('No se pude borrar ya que tiene referencias de otras tablas')
                self.errores='No se pude borrar ya que tiene referencias en la tabla '+self.tablaRef

    def verificarForaneas(self, ruta):
        if not os.path.exists(ruta) or not os.path.isdir(ruta):
            print(f"La ruta {ruta} no es válida o no es un directorio.")
            return False

        tablas = [nombre for nombre in os.listdir(ruta) if os.path.isdir(os.path.join(ruta, nombre))]
        print('------verificando')
        print(f"La ruta {ruta} no es válida o no es un directorio.")

        for nombre in tablas:
            print('------verificando2')
            ruta2 = os.path.join(ruta, nombre)
            print(ruta2)
            ruta3=os.path.join(ruta2, 'estructura.xml')
            print(ruta3)
            root = self.leer_estructura_xml(ruta3)
            noSeborra = self.comparar_foranea_con_atributo(root, self.idTable)

            # Si encontramos alguna coincidencia, retornamos True
            if noSeborra:
                self.tablaRef=nombre
                return True

        # Si llegamos aquí, no se encontró ninguna coincidencia
        return False

    def leer_estructura_xml(self, ruta):
        try:
            with open(ruta, 'r') as file:
                tree = ET.parse(file)
                root = tree.getroot()
                return root
        except FileNotFoundError:
            print(f"El archivo no se encuentra: {ruta}")
            return None
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None

    def comparar_foranea_con_atributo(self, estructura_xml, id_tabla):
        print('comparando con atributo', estructura_xml.text)
        for foranea_elem in estructura_xml.findall(".//*"):
            if foranea_elem.tag.startswith("Foranea_"):
                foranea_info = eval(foranea_elem.text)  # Convertir la cadena a un diccionario
                print(f"Encontrado una Foranea que coincide con la tabla {id_tabla}: {foranea_info}")
                if foranea_info.get('tabla') == id_tabla:
                    print(f"Encontrado una Foranea que coincide con la tabla {id_tabla}: {foranea_info}")

                    return True
        return False

    def limpiar_contenido_archivo(self,ruta_archivo):
        try:
            with open(ruta_archivo, 'w') as archivo:
                archivo.write('')
            print(f"Contenido del archivo '{ruta_archivo}' limpiado correctamente.")
            return True
        except Exception as e:
            print(f"Error al intentar limpiar el archivo '{ruta_archivo}': {str(e)}")
            return False

    def borrar_elementos(self, ruta_archivo_xml):
        try:
            # Leer el archivo XML
            tree = ET.parse(ruta_archivo_xml)
            root = tree.getroot()

            # Eliminar todos los elementos hijos del elemento raíz
            root[:] = []

            # Guardar los cambios en el archivo
            tree.write(ruta_archivo_xml, encoding='utf-8', xml_declaration=True)
            print(f"Se han borrado todos los elementos en {ruta_archivo_xml}")
        except Exception as e:
            print(f"Error al borrar elementos: {e}")