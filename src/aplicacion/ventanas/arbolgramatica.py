import ply.lex as lex
import ply.yacc as yacc
from graphviz import Digraph
from src.parser.lexer import tokens, lexer


# ... (definiciones de tokens y otras reglas de la gramática) ...

# Clase para representar nodos del AST
class Node:
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.children = children if children else []
        self.value = value

    def __repr__(self):
        return f"{self.type}({self.value})" if self.value else f"{self.type}"

# Reglas semánticas yacc para construir nodos del AST
def p_initial(p):
    '''
    initial : produccion initial
            | produccion
    '''
    if len(p) == 3:
        p[0] = Node("initial", [p[1], p[2]])
    else:
        p[0] = Node("initial", [p[1]])

def p_seleccionardb(p):
    '''
    seleccionardb : USAR ID
    '''
    p[0] = Node("seleccionardb", [Node("USAR"), Node("ID", value=p[2])])

def p_produccion(p):
    '''
    produccion  : create PCOMA
                | createdb PCOMA
                | compartidas PCOMA
                | seleccionardb PCOMA
                | funcion
                | procedure PCOMA
                | llamado PCOMA

    '''
    p[0] = Node("produccion", [p[1], Node('PUNTO COMA')])
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
    p[0] = Node("compartidas", [p[1]])

def p_createdb(p):
    '''
    createdb : CREATE DATA BASE ID
    '''
    p[0] = Node("createdb", [Node("CREATE"), Node("DATA"), Node("BASE"), Node(p[4])])

def p_create(p):
    '''
    create      : CREATE TABLE ID LPAREN  defcreate_list RPAREN
    '''
    p[0] = Node("create", [Node("CREATE"), Node("TABLE"), Node(p[3]), Node("LPAREN"), p[5], Node("RPAREN")])
def p_defcreate_list(p):
    '''
    defcreate_list : defcreate_list COMA defcreate
                  | defcreate
    '''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
        p[1] = Node("defcreate", [p[1],Node('COMA'), p[3]])
    else:
        p[0] = [p[1]]
        p[0]=Node("defcreate", [p[1]])


def p_defcreate(p):
    '''
    defcreate   : campo COMA defcreate
                | campo
    '''
    if len(p) == 4:
        p[0] = Node("defcreate", [p[1], Node("COMA"), Node("def",[p[3]])])
    else:
        p[0] = Node("defcreate", [p[1]])

def p_campo(p):
    '''
        campo   : ID tipodato restriccion
                | ID tipodato
    '''
    if len(p) == 4:

        p[0] = Node("campo", [p[1],Node(p[2]), p[3]])
    else:
        p[0] = Node("campo", [Node(p[1]),p[2]])
def p_restriccion(p):
    '''
    restriccion   : NOT NULL
            | PRIMARY KEY foranea
            | PRIMARY KEY
            | foranea
    '''
    if len(p) == 4:
        p[0] = Node("restriccion", [Node("PRIMARY"),Node("KEY"), Node(p[3])])
    elif len(p)==2:
        p[0] = Node("restriccion", [Node(p[1])])
    elif p[1]=='NOT':
        p[0] = Node("restriccion", [Node("NOT"),Node("NULL")])
    else:
        p[0] = Node("restriccion", [Node("PRIMARY"), Node("KEY")])

def p_foranea(p):
    '''
    foranea : REFERENCES ID LPAREN ID RPAREN
    '''
    p[0] = Node("foranea", [Node("REFERENCES"), Node(p[2]), Node("LPAREN"), Node(p[4]), Node("RPAREN")])
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
        p[0] = Node("tipodato", [Node("INT")])
    elif p[1] == 'decimal':
        p[0] = Node("tipodato", [Node("DECIMAL")])
    elif p[1] == 'nvarchar':
        p[0] = Node("tipodato", [Node("NVARCHAR"), Node("LPAREN"), Node(p[3]), Node("RPAREN")])
    elif p[1] == 'nchar':
        p[0] = Node("tipodato", [Node("NCHAR"), Node("LPAREN"), Node(p[3]), Node("RPAREN")])
    elif p[1] == 'date':
        p[0] = Node("tipodato", [Node("DATE")])
    elif p[1] == 'datetime':
        p[0] = Node("tipodato", [Node("DATETIMEL")])

def p_select(p):
    '''
    select  : SELECT funcionesdefinidas
            | SELECT selectmultiple
    '''
    p[0] = Node("select", [Node(p[2])])

def p_selectmultiple(p):
    '''
    selectmultiple  : listacolumn FROM valores WHERE condiciones
                    | listacolumn FROM valores
    '''
    if len(p) == 6:
        p[0] = Node("selectmultiple", [p[1], Node("FROM"), p[3], Node("WHERE"), p[5]])
    elif len(p) == 4:
        p[0] = Node("selectmultiple", [p[1], Node("FROM"), p[3]])
def p_listacolumn(p):
    '''
    listacolumn : valorescolumna COMA listacolumn
                | valorescolumna
                | TIMES
    '''
    if len(p) == 4:
        p[0] = Node("listacolumn", [p[1], Node("COMA"), p[3]])
    elif len(p) == 2:
        p[0] = Node("listacolumn", [p[1]])
    elif p[1] == '*':
        p[0] = Node("listacolumn", [Node("TIMES")])
def p_valorescolumna(p):
    '''
    valorescolumna  : ID PUNTO ID
                    | ID
                    | funcionesdefinidas
                    | llamado
    '''
    if len(p) == 4:
        p[0] = Node("valorescolumna", [Node("ID", [p[1]]), Node("PUNTO"), Node("ID", [p[3]])])
    elif len(p) == 2:
        if isinstance(p[1], Node):
            p[0] = Node("valorescolumna", [p[1]])
        else:
            p[0] = Node("valorescolumna", [Node("ID", [p[1]])])
def p_funcionesefinidas(p):
    '''
    funcionesdefinidas :  CONCATENA LPAREN factor COMA factor RPAREN
                    |  SUBSTRAER LPAREN CADENA COMA NUMBER COMA NUMBER
                    |  HOY LPAREN RPAREN
                    |  CONTAR LPAREN TIMES RPAREN FROM ID
                    |  SUMA LPAREN ID RPAREN FROM ID
                    |  CAST
    '''
    if p[1] == 'CONCATENA':
        p[0] = Node("CONCATENA", [Node("factor", [p[3]]), Node("factor", [p[5]])])
    elif p[1] == 'SUBSTRAER':
        p[0] = Node("SUBSTRAER", [Node("CADENA", [p[3]]), Node("NUMBER", [p[5]]), Node("NUMBER", [p[7]])])
    elif p[1] == 'HOY':
        p[0] = Node("HOY")
    elif p[1] == 'CONTAR':
        p[0] = Node("CONTAR", [Node("TIMES")])
    elif p[1] == 'SUMA':
        p[0] = Node("SUMA", [Node("ID", [p[3]]), Node("ID", [p[7]])])
    elif p[1] == 'CAST':
        p[0] = Node("CAST")
def p_alter(p):
    '''
    alter   : ALTER TABLE ID ADD COLUMN ID tipodato
            | ALTER TABLE ID DROP COLUMN ID
    '''
    if p[4] == 'ADD':
        p[0] = Node("ALTER",
                    [Node("ADD_COLUMN", [Node("TABLE", [p[3]]), Node("COLUMN", [p[6]]), Node("TYPE", [p[7]])])])
    elif p[4] == 'DROP':
        p[0] = Node("ALTER", [Node("DROP_COLUMN", [Node("TABLE", [p[3]]), Node("COLUMN", [p[6]])])])
def p_truncate(p):
    '''
    truncate    : TRUNCATE TABLE ID
    '''
    p[0] = Node("TRUNCATE", [Node("TRUNCATE"), Node("TABLE", [p[3]]) ])
def p_drop(p):
    '''
    drop : DROP TABLE ID
         | DROP COLUMN ID
    '''
    if p[2] == 'TABLE':
        p[0] = Node("DROP", [Node("TABLE", [p[3]])])
    elif p[2] == 'COLUMN':
        p[0] = Node("DROP", [Node("COLUMN", [p[3]])])
def p_insert(p):
    '''
    insert      : INSERT INTO ID parametrosi VALUES entradas
    '''
    p[0] = Node("INSERT", [Node("INTO"), p[3], p[4], p[6]])
def p_parametrosi(p):
    '''
    parametrosi  : LPAREN valores RPAREN
    '''
    p[0] = Node("PARAMETROS_INSERT", [p[2]])
def p_entradas(p):
    '''
    entradas  : LPAREN valentradas RPAREN
    '''
    p[0] = Node("ENTRADAS_INSERT", [p[2]])
def p_valentradas(p):
    '''
    valentradas  : expression COMA valentradas
                 | expression
    '''
    if len(p) == 4:
        p[0] = Node("VALORES_ENTRADA", [p[1], p[3]])
    else:
        p[0] = Node("VALORES_ENTRADA", [p[1]])
def p_valores(p):
    '''
    valores : ID COMA valores
            | ID
    '''
    if len(p) == 4:
        p[0] = Node("VALORES", [Node(p[1]), p[3]])
    else:
        p[0] = Node("VALORES", [Node(p[1])])
def p_update(p):
    '''
    update  : UPDATE ID SET cambios WHERE ID EQUALS expression
            | UPDATE ID SET cambios WHERE condiciones
    '''
    if len(p) == 9:
        p[0] = Node("UPDATE", [Node(p[2]), Node("CAMBIOS", [p[4]]), Node("WHERE"),p[6],Node("EQUAL"), p[8]])
    else:
        p[0] = Node("UPDATE", [Node(p[2]), Node("CAMBIOS", [p[4]]), Node("WHERE"), p[6]])

def p_cambios(p):
    '''
    cambios : campocambios COMA cambios
            | campocambios
    '''
    if len(p) == 4:
        p[0] = Node("CAMBIOS", [p[1], p[3]])
    else:
        p[0] = Node("CAMBIOS", [p[1]])

def p_campocambios(p):
    '''
    campocambios : ID EQUALS expression
    '''

    p[0] = Node("CAMPO_CAMBIOS", [Node(p[1]), Node("=", [Node(p[3])])])
# DELETE
def p_delete(p):
    '''
    delete  : DELETE FROM ID WHERE ID EQUALS expression
    '''
    p[0] = Node("DELETE", [Node("FROM", [Node(p[3])]), Node("WHERE", [p[5]])])

# DECLARACION------VARIABLES

def p_variable(p):
    '''
        variable : DECLARE ARROBA ID tipodato
                | SET ARROBA ID EQUALS valorvar
    '''


def p_valorvar(p):
    '''
    valorvar : expression
            | funcionesdefinidas
    '''


# ****************FUNCIONES y PROCEDURE *************

def p_initial2(p):
    '''
    initial2 : opespeciales initial2
            | opespeciales
    '''


def p_opespeciales(p):
    '''
    opespeciales : if PCOMA
                | variable PCOMA
                | compartidas PCOMA
    '''


def p_funcion(p):
    '''
    funcion  : CREATE FUNCTION ID LPAREN parametros RPAREN RETURN tipodato AS BEGIN initial2 RETURN expression PCOMA END
    '''
def p_parametros(p):
    '''
    parametros  : ARROBA ID tipodato COMA parametros
                | ARROBA ID tipodato
    '''

def p_procedure(p):
    '''
    procedure  : CREATE PROCEDURE ID LPAREN parametros RPAREN  AS BEGIN initial2 END
    '''

def p_llamado(p):
    '''
    llamado : EXEC ID entradas
            | ID entradas
            | ID LPAREN RPAREN
    '''
#****************BUCLES IF WHILE************************

#IF
def p_if(p):
    '''
    if  : IF LPAREN condiciones RPAREN BEGIN initial2 END
        | IF LPAREN condiciones RPAREN BEGIN initial2 END ELSE BEGIN initial2 END
    '''


def p_condiciones(p):
    '''
    condiciones : condicion
                | condicion explogicas condiciones
    '''

def p_condicion(p):
    '''
    condicion : expression toperador expression
    '''


def p_toperador(p):
    '''
    toperador    : EQUALS
                | DIFERENTE
                | MAYORQ
                | MENORQ
                | MAYORIQ
                | MENORIQ
    '''
def p_explogicas(p):
    '''
    explogicas  : AND
                | OR
                | NOT1
    '''

#**************CASE
def p_case(p):
    '''
    case : expression toperador
    '''

def p_expression(p):
    '''
    expression : expression PLUS term
               | expression MINUS term
               | term
    '''
    if len(p) == 4:
        p[0] = Node(p[2], [p[1], p[3]])
    else:
        p[0] = p[1]

def p_term(p):
    '''
    term : term TIMES factor2
         | term DIVIDE factor2
         | factor2
    '''
    if len(p) == 4:
        p[0] = Node(p[2], [p[1], p[3]])
    else:
        p[0] = p[1]
#podria no funcionar
def p_factor2(p):
    '''
    factor2 : LPAREN expression RPAREN
            | factor
    '''
    if len(p) == 4:
        p[0] = p[2]  # Si hay paréntesis, devolvemos la expresión dentro de los paréntesis
    else:
        p[0] = p[1]

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
        p[0] = Node(p[1])  # Crear un nodo para factores simples como NUMBER, DECIMAL1, CADENA, ID, etc.
    elif len(p) == 3:
        p[0] = Node(f"{p[1]} {p[2]}",
                    [Node(p[1]), Node(p[2])])  # Crear un nodo para factores compuestos como ID PUNTO ID
    elif len(p) == 3:
        p[0] = Node(f"{p[1]} {p[2]}",
                    [Node(p[1]), Node(p[2])])  # Crear un nodo para factores compuestos como ID PUNTO ID
    elif len(p) == 3:
        p[0] = Node(p[1], [Node(p[2])])
def create_ast(code):
    return parser.parse(code, lexer=lexer)

# Función para visualizar el AST con Graphviz
def visualize_ast(node, dot=None):
    if dot is None:
        dot = Digraph(comment='Abstract Syntax Tree')

    if isinstance(node, Node):
        dot.node(str(node), str(node))
        for child in node.children:
            child_dot = visualize_ast(child, dot)
            dot.edge(str(node), str(child))

    return dot
# Crea el parser
parser = yacc.yacc()

# Función para crear el AST

class Arbolgramatica():
    def __init__(self, code):
        self.code =code
# Ejemplo de código
#code = "UPDATE tbcompus set nombre_pc = 'gamers lap' where marca = 'Dell';"
   # code = 'CREATE TABLE ' #"UPDATE tbcompus "
    #code2= "tbestado (idestado int PRIMARY KEY, estado nvarchar(50) NOT NULL);"#"set nombre_pc = 'gamers lap' where marca = 'Dell';"

   # code3= code+code2
    def dibujar(self):
        ast = create_ast(self.code)

        # Visualizar el AST
        dot = visualize_ast(ast)
        dot.render('ast_example', format='png', cleanup=True)
