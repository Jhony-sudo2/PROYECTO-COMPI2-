from src.parser.lexer2 import tokens
import ply.yacc as yacc

tablasimbolos = []
errores2 = []
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
        p[0] = buscarvalor(p[1])

def buscarvalor(variable):
    for tmp in tablasimbolos:
        if tmp.nombre == variable:
            if tmp.valor != None:
                return tmp.valor
    return False
    pass
def t_error(t):
    print("Carácter no válido '%s'" % t.value[0])
    t.lexer.skip(1)


def p_error(t):
    errores = f'Error sintáctico en línea {t.lineno} con: {t.value}'
    print(errores)

parser2 = yacc.yacc()
tablaparser = tablasimbolos
errores2 = errores2