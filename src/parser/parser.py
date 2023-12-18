import ply.yacc as yacc
from .lexer import tokens
from ..aplicacion.querys.CreateDB import CreateDB
from ..aplicacion.querys.CreateTable import CreateTable
from ..aplicacion.querys.Insert import Insert
from ..aplicacion.querys.Operacion import Operacion
from ..aplicacion.querys.Parametrostabla import Parametrostabla

lista = []

def getLista():
    return lista
def p_initial(p):
    '''
    initial : produccion initial
            | produccion      
    '''

def p_seleccionardb(p):
    '''
    seleccionardb : USAR ID
    '''
    p[0] = p[2]

def p_produccion(p):
    '''
    produccion  : create PCOMA
                | createdb PCOMA
                | insert PCOMA
                | update PCOMA
                | select PCOMA
                | alter PCOMA
                | seleccionardb PCOMA
    '''

#CREAR BASE DE DATOS

def p_createdb(p):
    '''
    createdb : CREATE DATA BASE ID      
    '''
    deb = CreateDB(str(p[4]))
    lista.append(deb)
    print(p[0])

#CREAR TABLA
def p_create(p):
    '''
    create      : CREATE TABLE ID LPAREN  defcreate RPAREN      
    '''
    nuevatabla = CreateTable(str(p[3]),p[5])
    p[0] = nuevatabla
    lista.append(nuevatabla)


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
        if type (p[3]) is tuple:
            parametro = Parametrostabla(p[1],p[2],foranea=p[3])
        else:
            parametro = Parametrostabla(p[1], p[2], condicion=p[3])
        p[0] = parametro
def p_restriccion(p):
    '''
    restriccion   : NOT NULL
            | PRIMARY KEY
            | foranea      
    '''

    if(p[1] == 'NOT'):
        p[0] = 1
    elif p[1] == 'PRIMARY':
        p[0] = 2
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
    if p[1] == 'INTEGER':
        p[0] = 1
    elif p[1] == 'DECIMAL':
        p[0] = 2
    elif p[1] == 'NVARCHAR':
        p[0] = 4
    elif p[1] == 'NCHAR':
        p[0] = 4
    elif p[1] == 'DATE':
        p[0] = 5
    elif p[1] == 'DATETIME':
        p[0] = 6

#SELECT
def p_select(p):
    '''
    select  : selectbasico 
            | selectdefinidos 
            | selectasignacion
    '''

def p_selectdefinidos(p):
    '''
    selectdefinidos : SELECT CONCATENAR LPAREN CADENA COMA CADENA RPAREN 
                    | SELECT SUBSTRAER LPAREN CADENA COMA NUMBER COMA NUMBER
                    | SELECT HOY LPAREN RPAREN
                    | SELECT CONTAR LPAREN TIMES RPAREN FROM ID WHERE campocambios 
                    | SELECT SUMA LPAREN ID RPAREN FROM ID WHERE campocambios
                    | SELECT CAST
    '''

def p_selectbasico(p):
    '''
    selectbasico  : SELECT TIMES FROM ID 
    '''
def p_selectasignacion(p):
    '''
    selectasignacion    : SELECT  
    '''

#ALTER TABLE
def p_alter(p):
    '''
    alter   : ALTER TABLE ID ADD ID tipodato
            | ALTER TABLE ID drop
    '''

#TRUNCATE
def p_truncate(p):
    '''
    truncate    : TRUNCATE TABLE ID 
    '''
#DROP TABLE
def p_drop(p):
    '''
    drop : DROP TABLE ID
         | DROP COLUMN ID  
    '''
        

#INSERT
def p_insert(p):
    '''
    insert      : INSERT INTO ID parametrosi VALUES entradas
    '''
    accion = Insert(p[4],p[6],p[3])
    listado.append(accion)
    print('produccion insert')

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
        valentrada = p[3]
        valentrada.append(p[1])
        p[0] = valentrada
    else:
        valentrada = []
        valentrada.append(p[1])
        p[0] = valentrada

def p_valores(p):
    '''
    valores : ID COMA valores
            | ID     
    '''

    if len(p) == 4:
        valores = p[3]
        valores.append(p[1])
        p[0] = valores
    else:
        valores = []
        valores.append(p[1])
        p[0] = valores

    
#UPDATE    
def p_update(p):
    '''
    update  : UPDATE ID SET cambios WHERE ID EQUALS expression   
    '''

def p_cambios(p):
    '''
    cambios : campocambios COMA cambios
            | campocambios    
    '''

def p_campocambios(p):
    '''
    campocambios : ID EQUALS expression   
    '''
    
    

#DELETE
def p_delete(p):
    '''
    delete  : DELETE FROM ID WHERE ID EQUALS expression
    '''


def p_acciones(p):
    '''
    acciones    : variable PCOMA
                | select PCOMA
                | if
    '''

#VARIABLES
def p_variables(p):
    '''
        variable : DECLARE ARROBA ID tipodato
    '''

#FUNCIONES
def p_funcion(p):
    '''
    funcion  : CREATE FUNCTION ID LPAREN parametros RPAREN RETURN tipodato AS BEGIN END
    '''
    
def p_parametros(p):
    '''
    parametros  : ARROBA ID tipodato COMA parametros
                | ARROBA ID tipodato
    '''

def p_accionesfuncion(p):
    '''
    accionesfuncion :
    '''

#BUCLES

#IF
def p_if(p):
    '''
    if  : IF LPAREN condicion RPAREN
    '''

def p_condicion(p):
    '''
    condicion : expression toperador expression
    '''

def p_toperador(p):
    '''
    toperador    : IGUAL
                | DIFERENTE
                | MAYORQ
                | MENORQ
                | MAYORIQ
                | MENORIQ
    '''

#WHILE

def p_while(p):
    '''
    while   : 
    '''


def p_expression(p):
    '''
    expression : expression PLUS term
               | expression MINUS term
               | term
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]

def p_term(p):
    '''
    term : term TIMES factor
         | term DIVIDE factor
         | factor
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]

def p_factor(p):
    '''
    factor : NUMBER
           | DECIMAL1
           | CADENA
    '''
    p[0] = p[1]

def p_start(p):
    '''
    start : initial
    '''

def t_error(t):
    print("Carácter no válido '%s'" % t.value[0])
    t.lexer.skip(1)
    
def p_error(t):
    print(f'Error sintáctico en línea {t.lineno}, columna {find_column(t.lexer.lexdata, t)} con: {t.value}')

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

parser = yacc.yacc()
listado = getLista()