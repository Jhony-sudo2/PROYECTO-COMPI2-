class Condicion:
    def __init__(self, id, signo, val2):
        self.id = id
        self.signo = signo
        self.val2 = val2

    def validar(self):
        if self.signo == '==':
            if self.val1 == self.val2:
                return True
        if self.signo == '=Z':
            pass

    def obtenerValor(self):
        pass
