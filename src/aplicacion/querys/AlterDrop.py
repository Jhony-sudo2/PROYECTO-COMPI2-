import os

from src.aplicacion.querys.Basicos import existetabla


class AlterDrop():
    def __init__(self, idtable, isTable, idDelete):
        self.idtable = idtable
        self.isTable = isTable
        self.idDelete = idDelete

    def ejecutar(self, db):
        if self.isTable:
            #introducimos el codigo para elimnar tablas
            #verificamos que la tabla exista y si estiste la eliminamos
            ruta_actual = os.getcwd()
            ruta_tabla = os.path.abspath(
                os.path.join(ruta_actual, '..', '..')) + '/databases/' + db + '/Tables/' + self.idTable
            existeTb = existetabla(ruta_tabla)
            if existeTb:
                pass

        else:
            pass
            #codigo para eliminar una columna
