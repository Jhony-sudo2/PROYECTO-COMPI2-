class Mientras:
    def __init__(self,acciones,condicion):
        self.acciones = acciones
        self.condicion = condicion

    def ejecutar(self):
        while self.verificarcondicion():
            for accion in self.acciones:
                accion.ejecutar()


    def verificarcondicion(self):
        print(self.condicion)

