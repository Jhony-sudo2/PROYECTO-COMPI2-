import ply.lex as lex

reservadas = {
    #BASE DE DATOS DDL
    'DECLARE':'DECLARE'|'declare',
    'CREATE':'create'|'CREARTE',
    'ALTER':'alter'|'ALTER',
    'DROP':'drop'|'DROP',
    'TABLE':'TABLE'|'table',
    'TRUNCATE':'TRUNCATE'|'truncate',


    #DML
    'UPDATE':'UPDATE'|'update',
    'SELECT':'SELECT'|'select',
    'INSERT':'INSERT'|'insert',
    'INTO':'INTO'|'into',
    'VALUES':'VALUES'|'values',
    'PRIMARY':'PRIMARY KEY',
    'FOREING':'FIREIGN KEY',
    'DATE':'DATE',
    'DATETIME':'DATETIME',
    'BIT':'BIT',
    'INT':'INTEGER',
    'DECIMAL':'DECIMAL',
    'BOOL':'BOOLEAN',
    'NVARCHAR':'NVARCHAR',
    'NCHAR':'NCHAR',

    #FUNCIONES DEL SISTEMA:
    'CONTATENA':'CONCATENA',
    'SUBSTRAER':'SUBSTRAER',
    'HOY':'HOY',
    'CONTAR':'CONTAR',
    'SUMA':'SUMA',
    'CAST':'CAST',


    #SSL
    'IF':'IF'|'if',


}


tokens = [
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'EQUALS',
    'ID',
    'PCOMA',
    'PUNTO',
    'ARROBA',
] + list(reservadas.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_PCOMA = r';'
t_PUNTO = r'\.'
t_ARROBA = r'@'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # Verificar si es una palabra reservada
    t.type = reservadas.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()