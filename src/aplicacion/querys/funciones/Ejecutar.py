from src.aplicacion.querys.funciones.funcion import funcion


class Ejecutar:
    def __init__(self,nombre,linea,parametros = None,tablafunciones = None):
        self.nombre = nombre
        self.parametros = parametros
        self.tablasimbolos = []
        self.errores = ''
        self.resultado = ''
        self.tablafunciones = tablafunciones
        self.funcion:funcion
        self.linea = linea

    def ejecutar(self,db):
        print(f'linea {self.linea}')
        if self.buscar(db):
            if len(self.funcion.parametros) == len(self.parametros):
                self.IniciarTabla()
                print('ejecutando funcion '+self.funcion.nombre)
                for accion in self.funcion.acciones:
                    accion.tablasimbolos = self.tablasimbolos
                    accion.ejecutar(db)
            else:
                self.errores += f' Error en envio de parametros en la funcion {self.funcion.nombre}  linea : {self.linea}'


    def IniciarTabla(self):
        print('parametros recibidos')
        print(self.funcion.parametros)
        print('parametros ENVIADOS')
        print(self.parametros)

    def buscar(self,db):
        print('buscando funcion '+self.nombre)
        for funcion in self.tablafunciones:
            if funcion.nombre == self.nombre and db == funcion.db:
                self.funcion = funcion
                return True
        return False