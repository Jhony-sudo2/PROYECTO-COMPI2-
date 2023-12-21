import  os
def getrutatablas(db):
    ruta_actual = os.getcwd()
    ruta3 = os.path.abspath(os.path.join(ruta_actual, '..', '..')) + '/databases/' + db + '/Tables/'
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

