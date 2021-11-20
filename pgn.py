from ply import lex, yacc

"""
Gramática

S -> (S)S | .
"""

tokens = ('LPAREN','RPAREN','LLLAVE','RLLAVE','DOT','DOTS','NUM','STRING','JUGADA','DESCRIPTOR','RESULTADO','SPACE')

# Tokens
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_LLLAVE        = r'\{'
t_RLLAVE        = r'\}'
t_DOT           = r'\.' 
t_DOTS          = r'\.\.\.'
t_NUM           = r'[1-9][0-9]*'
t_STRING        = r'[a-zA-ZñÑáéíóúÁÉÍÓÚ\-!,’´]+'
t_JUGADA        = r'([PNBRQK]?[a-h]?[1-8]?x?[a-h][1-8](\+|\+\+)?|O-O|O-O-O)(!|\?)?'
t_DESCRIPTOR    = r'\[[a-zA-Z0-9ñÑáéíóúÁÉÍÓÚ]+\ "[a-zA-Z0-9ñÑáéíóúÁÉÍÓÚ\.\?\ -]+"\]'
t_RESULTADO     = r'0-1|1-0|1\/2-1\/2'
t_SPACE         = r'\ '

# Ignored characters
t_ignore = "\n\t"

def t_error(t):
    raise Exception(f"Lexer: Illegal character {t.value[0]!r}")

# Build the lexer
lexer = lex.lex()

"""
Gramática

P: Partida, J: Jugadas, F: Final, C: Comentario, T: Texto

############################ Gramática extendida

S -> (DESCRIPTOR+ P)+
P -> J*F
J -> B (C NUM DOTS SPACE)? JUGADA C? SPACE
F -> B ((C NUM DOTS SPACE)? JUGADA SPACE)? C? RESULTADO
B -> NUM DOT SPACE JUGADA SPACE
C -> {T C?} | (T C?)
T -> (STRING | NUM | DOT | JUGADA | SPACE)*

# Segunda iteración

S -> (DESCRIPTOR+ P)+
P -> J+
J -> B (Ns | C RESULTADO | RESULTADO)
Ns -> N (Cs | RESULTADO | .)
Cs -> C (SPACE | RESULTADO)
N -> (C NUM DOTS SPACE)? JUGADA SPACE
B -> NUM DOT SPACE JUGADA SPACE
C -> {T C?} | (T C?)
T -> (STRING | NUM | DOT | JUGADA | SPACE)+

############################ Gramática derivada

# Segunda iteración

S  -> D P S1 .
S1 -> S | .
D  -> DESCRIPTOR D1 .
D1 -> D | .
P  -> J P1 .
P1 -> P | . 
J  -> B J1 .
B  -> NUM DOT SPACE JUGADA SPACE .
J1 -> Ns | C RESULTADO | RESULTADO .
Ns -> N N1 .
N1 -> Cs | RESULTADO | .
Cs -> C C2 .
C2 -> SPACE | RESULTADO .
N  -> N2 JUGADA SPACE .
N2 -> C NUM DOTS SPACE | .
C  -> { T C1 } | ( T C1 ) .
C1 -> C | .
T  -> T1 T | T1 .
T1 -> STRING | NUM | DOT | JUGADA | SPACE .

# Primera iteración

D: Descriptor, Js: Jugadas, I: Interrupción de jugada, N: Negras (jugada de las negras), Ts: Textos

S  -> D P S'
S' -> S | λ
D  -> DESCRIPTOR D'
D' -> D | λ
P  -> Js F
Js -> J Js | λ
J  -> B I JUGADA C' SPACE
B  -> NUM DOT SPACE JUGADA SPACE
I  -> C NUM DOTS SPACE | λ
F  -> B N C' RESULTADO
N  -> I JUGADA SPACE | λ
C  -> {T C'} | (T C')
C' -> C | λ
T  -> Ts T | λ
Ts -> STRING | NUM | DOT | JUGADA | SPACE

# ¿Anidados intercalados?

C  -> CP | CL
CP -> (T CL) | λ
CL -> {T CP} | λ
"""

def p_start_simple(p):
    'start : desc part'

def p_start_multiple(p):
    'start : desc part start'
    
    
def p_expression_lambda(p):
    'expr : '
    p[0] = 0

def p_error(p):
    raise Exception(f"Parser: Syntax error at {p.value!r}")

parser = yacc.yacc()

# Test it out
data = '''
[a "b"]
1. e4 d5 {defensa escandinava (es com´un 2. exd5 Da5 {no es com´un 2... c6})} 1/2-1/2
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(f'{tok.type}({tok.value})', end = ' ')
