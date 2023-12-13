import pandas as pd
class Insert:
    def __init__(self, titulos, valores):
        self.titulos=titulos
        self.valores= valores

    titulos1=["nombre", "apellido", "edad"]
    valores=["Estuardo", "Ramos", 24]

    df = pd.DataFrame([valores], columns=titulos1)