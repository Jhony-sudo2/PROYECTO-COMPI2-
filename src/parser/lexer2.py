import ply.lex as lex
tokens = [
    'NUMBER',
    'DECIMAL1',
    'CADENA',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'ID',
    'ARROBA',
    'LPAREN',
    'RPAREN',
    'DIFERENTE',
    'MAYORQ',
    'MENORQ',
    'MAYORIQ',
    'MENORIQ',
    'AND',
    'OR',
    'NOT',
    'EQUALS'

]

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ARROBA = r'@'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='
t_DIFERENTE = r'!='
t_MAYORQ = r'>'
t_MENORQ = r'<'
t_MAYORIQ = r'>='
t_MENORIQ = r'<='
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
def t_DECIMAL1(t):
    r'-?\d+\.\d+'
    t.value = float(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CADENA(t):
    r"'[^']*'"
    t.value = str(t.value)
    return t


t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer2 = lex.lex()