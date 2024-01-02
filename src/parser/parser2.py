from src.parser.lexer2 import tokens
import ply.yacc as yacc

tablasimbolos = []
errores2 = []

def p_initial(p):
    '''
    initial : expression
            | condiciones
    '''
    p[0] = p[1]
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
    term : term TIMES factor2
         | term DIVIDE factor2
         | factor2
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]


def p_factor2(p):
    '''
    factor2 : LPAREN expression RPAREN
            | factor
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_factor(p):
    '''
    factor : NUMBER
           | DECIMAL1
           | CADENA
           | ARROBA ID
           | ID
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '.':
        p[0] = p[1] + p[2] + p[3]
    else:
        p[0] = buscarvalor(p[2])

def buscarvalor(variable):
    for tmp in tablasimbolos:
        if tmp.nombre == variable:
            if tmp.valor != None:
                if isinstance(tmp.valor, float) or isinstance(tmp.valor, int):
                    return float (tmp.valor)
                else:
                    return tmp.valor
    return False
    pass

##para las condiciones

def p_condiciones(p):
    '''
    condiciones : condiciones OR x
                | x
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] or p[3]
def p_x(p):
    '''
        x   : x AND y
            | x NOT y
            | y
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == '&&':
            p[0] = p[1] and p[3]
        elif p[2] == '!':
            p[0] = p[1] or p[3]
def p_y(p):
    '''
        y   : LPAREN condiciones RPAREN
            | condicion
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]
def p_condicion(p):
    '''
    condicion : expression toperador expression
    '''
    p[1] = float(p[1])
    p[3] = float(p[3])
    if p[2] == '=':
        p[0] = p[1] == p[3]
    elif p[2] == '!=':
        p[0] = p[1] != p[3]
    elif p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]


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

def getTablaSimbolos():
    return tablasimbolos
def t_error(t):
    print("Carácter no válido '%s'" % t.value[0])
    t.lexer.skip(1)


def p_error(t):
    errores = f'Error sintáctico en línea {t.lineno} con: {t.value}'
    print(errores)

parser2 = yacc.yacc()
errores2 = errores2
tablaparser = getTablaSimbolos()