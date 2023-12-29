import ply.lex as lex
import ply.yacc as yacc
from graphviz import Digraph

# Lista de tokens
# Lista de tokens
tokens = ['NUMBER', 'PLUS', 'MINUS', 'TIMES', 'LPAREN', 'RPAREN']

# Reglas de expresiones regulares para los tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NUMBER = r'\d+'


# Ignorar caracteres en blanco
t_ignore = ' \t\n'

# Definir la gramática
def p_expression(p):
    '''
    expression : expression PLUS term
               | expression MINUS term
               | term
    '''
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_term(p):
    '''
    term : term PLUS factor
         | term MINUS factor
         | factor
    '''
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_factor(p):
    '''
    factor : NUMBER
           | LPAREN expression RPAREN
    '''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = int(p[1])



# Construir el lexer y parser
lexer = lex.lex()
parser = yacc.yacc()

# Crear el AST
def create_ast(code):
    return parser.parse(code, lexer=lexer)

# Visualizar el AST con Graphviz
def visualize_ast(node, dot=None):
    if dot is None:
        dot = Digraph(comment='Abstract Syntax Tree')

    if isinstance(node, tuple):
        label, *children = node
        dot.node(str(node), label)
        for child in children:
            child_dot = visualize_ast(child, dot)
            dot.edge(str(node), str(child))
    else:
        dot.node(str(node), str(node))

    return dot

# Ejemplo de código
code = "(2 + 3) + 4"
ast = create_ast(code)

# Visualizar el AST
dot = visualize_ast(ast)
dot.render('ast_example', format='png', cleanup=True)