class Si:
    def __init__(self,condicion,acciones1,acciones2=None):
        self.condicion = condicion
        self.acciones1 = acciones1
        self.acciones2 = acciones2

    def ejecutar(self,db):
        if self.verificar():
            for accion in self.acciones1:
                accion.ejecutar(db)
        else:
            if self.acciones2 is not None:
                for accion in self.acciones2:
                    accion.ejecutar(db)


    def verificar(self):
        print(self.condicion)
