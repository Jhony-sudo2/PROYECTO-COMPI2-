from src.aplicacion.querys.funciones.Variable import Variable
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
        self.retorno:Variable

    def ejecutar(self,db):
        print(f'linea {self.linea}')
        if self.buscar(db):
            if len(self.funcion.parametros) == len(self.parametros):
                self.IniciarTabla()
                print('ejecutando funcion '+self.funcion.nombre)
                for accion in self.funcion.acciones:
                    accion.tablasimbolos = self.tablasimbolos
                    accion.ejecutar(db)
                    if len(accion.errores) != 0:
                        self.errores += accion.errores
                if self.funcion.tipo == 1:
                    self.buscarretorno()
                    print('devolviendo: ',self.retorno.nombre , ' con valor: ',self.retorno.valor)
                    self.funcion.tablasimbolos.clear();
                    return  self.retorno.valor

            else:
                self.errores += f' ERROR en envio de parametros en la funcion {self.funcion.nombre}  linea : {self.linea}'


    def IniciarTabla(self):

        for index,tmp in enumerate(self.parametros):
            nombre = self.funcion.parametros[index][0]
            tipo   = self.funcion.parametros[index][1]
            variable = Variable(nombre,tipo,tmp)
            self.tablasimbolos.append(variable)


    def buscarretorno(self):
        nombrevar = self.funcion.retorno.lstrip('@')
        for variable in self.tablasimbolos:
            if variable.nombre == nombrevar:
                self.retorno = variable


    def buscar(self,db):
        for funcion in self.tablafunciones:
            if funcion.nombre == self.nombre and db == funcion.db:
                self.funcion = funcion
                return True
        self.errores += f'ERROR: La funcion  {self.nombre} no existe en la base de datos {db}  liena: {self.linea} \n'
        return False