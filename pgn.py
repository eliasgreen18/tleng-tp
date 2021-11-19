from ply import lex, yacc

"""
Gramática

S -> (S)S | .
"""

tokens = (
    'LPAREN','RPAREN','LLLAVE','RLLAVE','LCORCH','RCORCH','COMILL','DOT','CHAR','PLUS','QMARK','EMARK','GUION','SLASH','DOTS','PLUSES','JUGADA','COSO','RESULTADO'
)

# Tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LLLAVE = r'\{'
t_RLLAVE = r'\}'
t_LCORCH = r'\['
t_RCORCH = r'\]'
t_COMILL = r'\"'
t_DOT    = r'\.' 
t_PLUS   = r'\+' 
t_QMARK  = r'\?'
t_EMARK  = r'\!'
t_GUION  = r'-'
t_SLASH  = r'/'
t_DOTS   = r'\.\.\.'
t_PLUSES = r'\+\+'
t_CHAR   = r'[a-zA-Z0-9ñÑáéíóúÁÉÍÓÚ ]'
t_JUGADA = r'([PNBRQK]?[a-h]?[1-8]?x?[a-h][1-8](+|++)?|O-O(-O)?)(!|\?)?'
t_COSO = r'\[[a-zA-Z0-9ñÑáéíóúÁÉÍÓÚ ]+ \"[a-zA-Z0-9ñÑáéíóúÁÉÍÓÚ ]+\"\]'
t_RESULTADO = r'0-1|1-0|1\/2-1\/2'

# Ignored characters
t_ignore = "\n\t"

def t_error(t):
    raise Exception(f"Lexer: Illegal character {t.value[0]!r}")

# Build the lexer
lexer = lex.lex()

def p_expression_concat(p):
    'expr : LPAREN expr RPAREN expr'
    p[0] = max(p[2] + 1, p[4])
    
def p_expression_lambda(p):
    'expr : '
    p[0] = 0

def p_error(p):
    raise Exception(f"Parser: Syntax error at {p.value!r}")

parser = yacc.yacc()

# Para probar el lexer tenés que poner lo siguiente:

# Test it out
data = '''
.. .
. . ...
++ + ++ + + ++++
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)