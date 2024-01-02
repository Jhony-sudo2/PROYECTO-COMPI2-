from src.aplicacion.querys.Basicos import getvalores


class Si:
    def __init__(self,condicion,acciones1,tablasimbolos=None,acciones2=None):
        self.condicion = condicion
        self.acciones1 = acciones1
        self.acciones2 = acciones2
        self.tablasimbolos = tablasimbolos
        self.errores = ''

    def ejecutar(self,db):
        if self.verificar():
            for accion in self.acciones1:
                accion.tablasimbolos = self.tablasimbolos
                accion.ejecutar(db)
                if len(accion.errores) != 0:
                    self.errores += accion.errores + '\n'
        else:
            if self.acciones2 is not None:
                for accion in self.acciones2:
                    accion.tablasimbolos = self.tablasimbolos
                    accion.ejecutar(db)
                    if len(accion.errores) != 0:
                        self.errores += accion.errores + '\n'


    def verificar(self):
        cadena = self.getCadenaCondiciones()
        valorcondicion = getvalores(cadena,self.tablasimbolos)
        return valorcondicion
    def getCadenaCondiciones(self):
        cadena = ''
        for c in self.condicion:
            if isinstance(c,tuple):
                cadena += c[0] + c[1] + c[2]
            else:
                cadena += f' {c} '
        return cadena