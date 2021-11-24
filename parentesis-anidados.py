from ply import lex, yacc

"""
Gramática

S -> (S)S | .
"""

tokens = (
    'LPAREN','RPAREN',
)

# Tokens
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

# Ignored characters
t_ignore = "\n\t "

def t_error(t):
    raise Exception(f"Lexer: Illegal character {t.value[0]!r}")

# Build the lexer
lexer = lex.lex()
class Parentesis():
    def __init__(self, pepe, panoli):
        self.pepe   = pepe
        self.panoli = panoli

def p_start(p):
    'start : expr'
    p[0] = p[1].pepe

def p_expression_concat(p):
    'expr : LPAREN expr RPAREN expr'
    p[0] = Parentesis(max(p[2].pepe + 1, p[4].pepe), 0)
    
def p_expression_lambda(p):
    'expr : '
    p[0] = Parentesis(0, 0)
    

def p_error(p):
    raise Exception(f"Parser: Syntax error at {p.value!r}")

parser = yacc.yacc()

# Para probar el parser se utiliza el código que dejamos a continuación con entrada estándar. En este caso, cuenta la mayor cantidad de paréntesis anidados.

while True:
  try:
      s = input('input > ')
  except EOFError:
      break
  if not s: continue
  result = parser.parse(s)
  print(result)

# Para probar el lexer tenés que poner lo siguiente:
#
# # Test it out
# data = '''
# ()()((()()))
# '''
# 
# # Give the lexer some input
# lexer.input(data)
# 
# # Tokenize
# while True:
#     tok = lexer.token()
#     if not tok: 
#         break      # No more input
#     print(tok)
