from datetime import datetime


class Hoy:
    def __init__(self):
        self.errores = ''
        self.resultado = ''
    def ejecutar(self,db):
        fecha = datetime.now()
        fecha_hora_formateada = fecha.strftime("%Y-%m-%d %H:%M")
        self.resultado += fecha_hora_formateada + '\n'
        return  fecha_hora_formateada