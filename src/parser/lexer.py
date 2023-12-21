import ply.lex as lex

reservadas = {
    #BASE DE DATOS DDL
    'USAR':'USAR',
    'CREATE':'CREATE',
    'DATA':'DATA',
    'BASE':'BASE',
    'ALTER':'ALTER',
    'TABLE':'TABLE',
    'TRUNCATE':'TRUNCATE',
    'not':'NOT',
    'null':'NULL',
    'DELETE':'DELETE',
    'FROM':'FROM',
    'set':'SET',

    #DML
    'UPDATE':'UPDATE',
    'SELECT':'SELECT',
    'INSERT':'INSERT',
    'INTO':'INTO',
    'VALUES':'VALUES',
    'PRIMARY':'PRIMARY',
    'KEY':'KEY',
    'REFERENCE':'REFERENCES',
    'date':'DATE',
    'datetime':'DATETIME',
    'int':'INT',
    'decimal':'DECIMAL',
    'boolean':'BOOL',
    'nvarchar':'NVARCHAR',
    'nchar':'NCHAR',

    #FUNCIONES DEL SISTEMA:
    'CONTATENA':'CONCATENAR',
    'SUBSTRAER':'SUBSTRAER',
    'HOY':'HOY',
    'CONTAR':'CONTAR',
    'SUMA':'SUMA',
    'CAST':'CAST',

    #ALTER 
    'add':'ADD',
    'column':'COLUMN',
    'drop':'DROP',

    #TRUNCATE
    'TRUNCATE':'TRUNCATE',

    #SSL
    'IF':'IF',
    'ELSE':'ELSE',
    'AS':'AS',
    'PROCEDURE':'PROCEDURE',
    'WHERE':'WHERE',
    'WHILE':'WHILE',
    'exec':'EXEC',

    #FUNCIONES
    'FUNCTION':'FUNCTION',
    'return':'RETURN',
    'BEGIN':'BEGIN',
    'END':'END',
    'DECLARE':'DECLARE',

}


tokens = [
    'NUMBER',
    'DECIMAL1',
    'CADENA',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'IGUAL',
    'DIFERENTE',
    'MAYORQ',
    'MENORQ',
    'MAYORIQ',
    'MENORIQ',
    'AND',
    'OR',
    'NOT1',
    'ID',
    'PCOMA',
    'COMA',
    'PUNTO',
    'ARROBA',
    'LPAREN',
    'RPAREN',
    'EQUALS',

] + list(reservadas.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_PCOMA = r';'
t_COMA = r','
t_PUNTO = r'\.'
t_ARROBA = r'@'
t_IGUAL = r'=='
t_EQUALS = r'='
t_DIFERENTE = r'!='
t_MAYORQ = r'>'
t_MENORQ = r'<'
t_MAYORIQ = r'>='
t_MENORIQ = r'<='
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT1 = r'!'
t_LPAREN = r'\('
t_RPAREN = r'\)'




def t_DECIMAL1(t):
    r'-?\d+\.\d+'
    t.value = float(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CADENA(t):
    r"'[^']*'"
    t.value = str(t.value)
    return t



t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()