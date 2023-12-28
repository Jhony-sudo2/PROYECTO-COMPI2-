import  os
from datetime import datetime


def getrutatablas(db):
    ruta_actual = os.getcwd()
    ruta3 = os.path.abspath(os.path.join(ruta_actual, '..', '..')) + '/databases/' + db + '/Tables/'
    return ruta3

def getrutabase(db):
    ruta_actual = os.getcwd()
    ruta3 = os.path.abspath(os.path.join(ruta_actual, '..', '..')) + '/databases/' + db
    return ruta3

def existetabla(ruta):
    return os.path.exists(ruta)

def getrutadatos(ruta,nombre):
    rutatmp = ruta + nombre+'/datos.xml'
    return rutatmp

def getrutafunciones(db):
    ruta_actual = os.getcwd()
    ruta3 = os.path.abspath(os.path.join(ruta_actual, '..', '..')) + '/databases/' + db + '/Funciones/'
    return ruta3

def getTipoDato(valor):
    if isinstance(valor, int):
        return 1
    elif isinstance(valor, float):
        return 2
    elif isinstance(valor, str) and valor.startswith("'") and valor.endswith("'"):
        if len(valor) == 22 and valor[1:11].replace('-', '').isdigit() and valor[12:22].replace(':', '').isdigit():
            try:
                datetime.strptime(valor[1:-1], '%Y-%m-%d %H:%M')
                return 6
            except ValueError:
                return 4
        elif len(valor) == 12 and valor[1:5].isdigit() and valor[6:8].isdigit() and valor[9:11].isdigit():
            try:
                datetime.strptime(valor[1:-1], '%Y-%m-%d')
                return 5
            except ValueError:
                return 4
        else:
            return 4
    else:
        return 0