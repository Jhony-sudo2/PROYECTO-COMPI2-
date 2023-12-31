
import ply.yacc as yacc

from ..aplicacion.querys.Alter import Alter
from ..aplicacion.querys.Condicion import Condicion
from ..aplicacion.querys.CreateDB import CreateDB
from ..aplicacion.querys.CreateTable import CreateTable
from ..aplicacion.querys.Delete import Delete
from ..aplicacion.querys.Insert import Insert
from ..aplicacion.querys.Parametrostabla import Parametrostabla
from ..aplicacion.querys.Select import Select
from src.aplicacion.querys.bucles.Si import Si
from src.parser.lexer import tokens
from ..aplicacion.querys.Trucate import Trucate
from ..aplicacion.querys.Update import Update
from ..aplicacion.querys.Usar import Usar
from ..aplicacion.querys.bucles.Caso import Caso
from ..aplicacion.querys.bucles.Casos import Casos
from ..aplicacion.querys.definidas.Concatena import Concatena
from ..aplicacion.querys.definidas.Contar import Contar
from ..aplicacion.querys.definidas.Hoy import Hoy
from ..aplicacion.querys.definidas.Substraer import Substraer
from ..aplicacion.querys.definidas.Suma import Suma
from ..aplicacion.querys.funciones.Ejecutar import Ejecutar
from ..aplicacion.querys.funciones.OVariable import OVariable
from ..aplicacion.querys.funciones.Variable import Variable
from ..aplicacion.querys.funciones.funcion import funcion
from ..aplicacion.querys.funciones.setVariable import SetVariable

listaerrores = []
def p_initial(p):
    '''
    initial : produccion initial
            | produccion
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]
def p_seleccionardb(p):
    '''
    seleccionardb : USAR ID
    '''
    linea = p.lineno(1)
    fn = Usar(p[2],linea)
    p[0] = fn

def p_produccion(p):
    '''
    produccion  : create PCOMA
                | createdb PCOMA
                | compartidas PCOMA
                | seleccionardb PCOMA
                | funcion
                | procedure
                | llamado PCOMA
    '''
    p[0] = p[1]

def p_compartidas(p):
    '''
    compartidas : insert
                | select
                | update
                | truncate
                | drop
                | alter
                | delete
    '''
    p[0] = p[1]

#CREAR BASE DE DATOS

def p_createdb(p):
    '''
    createdb : CREATE DATA BASE ID      
    '''
    linea = p.lineno(1)
    deb = CreateDB(str(p[4]),linea)
    p[0] = deb

#CREAR TABLA
def p_create(p):
    '''
    create      : CREATE TABLE ID LPAREN  defcreate RPAREN      
    '''

    new = p[5][::-1]
    nuevatabla = CreateTable(str(p[3]),new)
    p[0] = nuevatabla


def p_defcreate(p):
    '''
    defcreate   : campo COMA defcreate
                | campo
    '''
    if len(p) == 4:
        parametros = p[3]
        parametros.append(p[1])
        p[0] = parametros
    elif len(p) == 2:
        parametros = []
        parametros.append(p[1])
        p[0] = parametros

def p_campo(p):
    '''
        campo   : ID tipodato restriccion
                | ID tipodato
    '''
    if len(p) == 3:
        parametro = Parametrostabla(p[1],p[2])
        p[0] = parametro
    else:
        if type (p[3]) is tuple and not type(p[3][1]) is tuple:
            parametro = Parametrostabla(p[1],p[2],foranea=p[3])
        elif type (p[3]) is tuple and type(p[3][1]) is tuple:
            parametro = Parametrostabla(p[1],p[2],foranea=p[3][1],condicion=p[3][0])
        else:
            parametro = Parametrostabla(p[1], p[2], condicion=p[3])
        p[0] = parametro
def p_restriccion(p):
    '''
    restriccion   : NOT NULL
            | PRIMARY KEY foranea
            | PRIMARY KEY
            | foranea      
    '''

    if(p[1] == 'not'):
        p[0] = 1
    elif len(p) == 3:
        p[0] = 2
    elif len(p) == 4:
        p[0] = (2,p[3])
    else:
        p[0] = p[1]


def p_foranea(p):
    '''
    foranea : REFERENCES ID LPAREN ID RPAREN
    '''
    tmp = (p[2],p[4])
    p[0] = tmp

def p_tipodato(p):
    '''
    tipodato  : INT
                | DECIMAL
                | BOOL
                | NVARCHAR LPAREN NUMBER RPAREN
                | NCHAR LPAREN NUMBER RPAREN
                | DATE
                | DATETIME
    '''
    if p[1] == 'int':
        p[0] = 1
    elif p[1] == 'decimal':
        p[0] = 2
    elif p[1] == 'nvarchar':
        p[0] = 4
    elif p[1] == 'nchar':
        p[0] = 4
    elif p[1] == 'date':
        p[0] = 5
    elif p[1] == 'datetime':
        p[0] = 6

#****SELECT*********************************************************************
def p_select(p):
    '''
    select  : SELECT funcionesdefinidas
            | SELECT selectmultiple
    '''
    p[0] = p[2]


def p_selectmultiple(p):
    '''
    selectmultiple  : listacolumn FROM valores WHERE condiciones
                    | listacolumn FROM valores
    '''
    linea = p.lineno(2)

    if len(p) == 4:
        fn = Select(p[3],p[1],linea)
        p[0] = fn
    else:
        fn = Select(p[3],p[1],linea,condiciones=p[5])
        p[0] = fn
def p_listacolumn(p):
    '''
    listacolumn : valorescolumna COMA listacolumn
                | valorescolumna
                | TIMES
    '''
    if len(p) == 2 and p[0] != '*':
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif p[0] =='*':
        p[0] = '*'

def p_valorescolumna(p):
    '''
    valorescolumna  : ID PUNTO ID
                    | ID
                    | funcionesdefinidas
                    | llamado
    '''
    if len(p) == 4:
        valor = p[1] + p[2] + p[3]
        p[0] = valor
    else:
        p[0] = p[1]


def p_funcionesefinidas(p):
    '''
    funcionesdefinidas :  CONCATENA LPAREN factor COMA factor RPAREN
                    |  SUBSTRAER LPAREN CADENA COMA NUMBER COMA NUMBER RPAREN
                    |  HOY LPAREN RPAREN
                    |  CONTAR LPAREN TIMES RPAREN FROM ID
                    |  SUMA LPAREN ID RPAREN FROM ID
                    |  CAST
    '''
    linea = p.lineno
    if p[1] == 'CONCATENA' or p[1] == 'concatena':
        valor = Concatena((p[3]),(p[5]))
        p[0] = valor
    elif len(p) == 4:
        fn = Hoy()
        p[0] = fn
    elif p[3] == '*':
        fn = Contar(p[6],columna=None)
        p[0] = fn
    elif p[1] == 'SUMA' or p[1] == 'suma':
        fn = Suma(p[6],p[3])
        p[0] = fn
    elif p[1] == 'SUBSTRAER' or p[1] == 'substraer':
        fn = Substraer(p[3],p[5],p[7],linea)
        p[0] = fn

#****************ALTER TABLE
def p_alter(p):
    '''
    alter   : ALTER TABLE ID ADD COLUMN ID tipodato
            | ALTER TABLE ID DROP COLUMN ID
    '''
    if p[4] == "add":
        alter = Alter(p[3], True, p[6],  p[7] )
        p[0]= alter
    else:
        alter = Alter(p[3], False, p[6],  p[6] )
        p[0] = alter
#**************TRUNCATE
def p_truncate(p):
    '''
    truncate    : TRUNCATE TABLE ID 
    '''
    fn = Trucate(p[3])
    p[0]= fn
#****************DROP TABLE

def p_drop(p):
    '''
    drop : DROP TABLE ID
         | DROP COLUMN ID  
    '''
    p[0]= {p[2]: p[3]}

#INSERT
def p_insert(p):
    '''
    insert      : INSERT INTO ID parametrosi VALUES entradas
    '''
    linea = p.lineno(1)
    accion = Insert(p[4],p[6],p[3],linea)
    p[0] = accion

def p_parametrosi(p):
    '''
    parametrosi  : LPAREN valores RPAREN
    '''
    p[0] = p[2]

def p_entradas(p):
    '''
    entradas  : LPAREN valentradas RPAREN
    '''
    p[0] = p[2]

def p_valentradas(p):
    '''
    valentradas  : expression COMA valentradas
                 | expression
    '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_valores(p):
    '''
    valores : ID COMA valores
            | ID     
    '''

    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

    
#UPDATE    
def p_update(p):
    '''
    update  :  UPDATE ID SET cambios WHERE condi
    '''

    update = Update(p[2], p[4],  p[6] )
    p[0] = update



def p_cambios(p):
    '''
    cambios : campocambios COMA cambios
            | campocambios    
    '''
    if len(p) == 4:
        cambios = p[3]
        cambios.update(p[1])  # Utiliza update para agregar al diccionario existente
        p[0] = cambios
    else:
        p[0] = {**p[1]}

def p_campocambios(p):
    '''
    campocambios : ID EQUALS expression   
    '''
    dic = {p[1]: p[3]}
    p[0] = dic
    

#DELETE
def p_delete(p):
    '''
    delete  : DELETE FROM ID WHERE condi
    '''
    delet = Delete(p[3], p[5])
    p[0]= delet

def p_condi(p):
     '''
     condi : ID toperador expression AND condi
            | ID toperador expression
     '''
     if len(p) == 6:
         condi= Condicion(p[1], p[2], p[3])
         p[0]=[condi] + p[5]
     else:
         condi= Condicion(p[1], p[2], p[3])
         p[0]=[condi]


#DECLARACION------VARIABLES

def p_variable(p):
    '''
        variable : DECLARE ARROBA ID tipodato
                | SET ARROBA ID EQUALS valorvar
    '''
    linea = p.lineno(1)
    if len(p) == 5:
        var = Variable(p[3],p[4])
        fn = OVariable(var,linea)
        p[0] = fn
    else:
        fn = SetVariable(p[3],p[5],linea)
        p[0] = fn
def p_valorvar(p):
    '''
    valorvar : expression
            | funcionesdefinidas
    '''
    p[0] = p[1]

#****************FUNCIONES y PROCEDURE *************

def p_initial2(p):
    '''
    initial2 : opespeciales initial2
            | opespeciales
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]
def p_opespeciales(p):
    '''
    opespeciales : if PCOMA
                | variable PCOMA
                | compartidas PCOMA
                | case PCOMA
    '''
    p[0]=p[1]


def p_funcion(p):
    '''
    funcion  : CREATE FUNCTION ID LPAREN parametros RPAREN RETURN tipodato AS BEGIN initial2 RETURN expression PCOMA END
    '''
    fn = funcion(p[3],p[5],p[11],p[8],p[13],1)
    p[0] = fn
    
def p_parametros(p):
    '''
    parametros  : ARROBA ID tipodato COMA parametros
                | ARROBA ID tipodato
    '''
    if len(p) == 6:
        p[0] = [(p[2],p[3])] + p[5]
    else:
        p[0] = [(p[2],p[3])]

def p_procedure(p):
    '''
    procedure  : CREATE PROCEDURE ID LPAREN parametros RPAREN  AS BEGIN initial2 END
    '''
    fn = funcion(p[3],p[5],p[9],None,None,2)
    p[0] = fn

def p_llamado(p):
    '''
    llamado : EXEC ID entradas
            | ID entradas
            | ID LPAREN RPAREN
    '''
    linea = p.lineno(1)
    if len(p) == 3:
        fn = Ejecutar(p[1],linea,parametros=p[2])
        p[0] = fn
    elif len(p) == 4:
        fn = Ejecutar(p[1],linea)
        p[0] = fn
#****************BUCLES IF WHILE************************

#IF
def p_if(p):
    '''
    if  : IF LPAREN condiciones RPAREN BEGIN initial2 END
        | IF LPAREN condiciones RPAREN BEGIN initial2 END ELSE BEGIN initial2 END
    '''
    if len(p) ==  8:
        accion = Si(p[3],p[6])
        p[0] = accion
    else:
        accion = Si(p[3], p[6],acciones2=p[10])
        p[0] = accion


def p_condiciones(p):
    '''
    condiciones : condicion
                | condicion explogicas condiciones
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = [p[1]] + [p[2]] + p[3]

def p_condicion(p):
    '''
    condicion : expression toperador expression
    '''
    p[0] = (p[1],p[2],p[3])


def p_toperador(p):
    '''
    toperador    : EQUALS
                | DIFERENTE
                | MAYORQ
                | MENORQ
                | MAYORIQ
                | MENORIQ
    '''
    p[0] = p[1]

def p_explogicas(p):
    '''
    explogicas  : AND
                | OR
                | NOT1
    '''

    p[0] = p[1]

#**************CASE
def p_case(p):
    '''
    case : CASE casos END
         | CASE casos ELSE THEN initial2 END
    '''
    if len(p) == 4:
        fn = Casos(p[2])
        p[0]= fn
    else:
        fn = Casos(p[2],extra=p[5])
        p[0] = fn

def p_casos(p):
    '''
    casos  : WHEN condiciones THEN initial2 casos
           | WHEN condiciones THEN initial2
    '''
    if len(p)== 6:
        caso= Caso(p[2],p[4])
        p[0] = [caso] + p[5]
    else:
        caso = Caso(p[2],p[4])
        p[0] = [caso]

def p_expression(p):
    '''
    expression : expression PLUS term
               | expression MINUS term
               | term
    '''
    if len(p) == 2:
        p[0] = str(p[1])
    else:
        if p[2] == '+':
            p[0] = f'{p[1]} + {p[3]}'
        elif p[2] == '-':
            p[0] = f'{p[1]} - {p[3]}'


def p_term(p):
    '''
    term : term TIMES factor2
         | term DIVIDE factor2
         | factor2
    '''
    if len(p) == 2:
        p[0] = str(p[1])
    else:
        if p[2] == '*':
            p[0] = f'{str(p[1])} * {str(p[3])}'
        elif p[2] == '/':
            p[0] = f'{str(p[1])} / {str(p[3])}'


def p_factor2(p):
    '''
    factor2 : LPAREN expression RPAREN
            | factor
    '''
    if len(p) == 2:
        p[0] = str(p[1])
    else:
        p[0] = f'(  {str(p[2])}  )'

def p_factor(p):
    '''
    factor : NUMBER
           | DECIMAL1
           | CADENA
           | ARROBA ID
           | ID PUNTO ID
           | ID
    '''
    if len(p) == 2:
        p[0] = str(p[1])
    elif p[2] == '.':
        p[0] = p[1] + p[2] + p[3]
    else:
        p[0] = p[1] + p[2]

def t_error(t):
    print("Carácter no válido '%s'" % t.value[0])
    t.lexer.skip(1)

def p_error(t):
    if t:
        errores = f'Error sintáctico en línea {t.lineno}, columna {find_column(t.lexer.lexdata, t)} con: {t.value}'
    else:
        errores = f'Error sintactico en EOF fin de caden'
    listaerrores.append(errores)
def getErrores():
    return listaerrores


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

parser = yacc.yacc()
parsererror = getErrores()