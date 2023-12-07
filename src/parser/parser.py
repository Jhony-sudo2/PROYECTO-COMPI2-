import ply.yacc as yacc
from lexer import tokens

def p_expression(p):
    '''
    expression : expression PLUS term
               | expression MINUS term
               | term
               | HOLA
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
    '''
    p[0] = p[1]

def t_error(t):
    print("Carácter no válido '%s'" % t.value[0])
    t.lexer.skip(1)
    
parser = yacc.yacc()
