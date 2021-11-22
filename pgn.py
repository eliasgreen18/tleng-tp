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
t_RESULTADO     = r'0\-1|1\-0|1\/2\-1\/2'
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
J -> B (Ns | C SPACE RESULTADO | RESULTADO)
Ns -> N (Cs | RESULTADO | .)
Cs -> C SPACE RESULTADO?
N -> (C NUM DOTS SPACE)? JUGADA SPACE
B -> NUM DOT SPACE JUGADA SPACE
C -> {T C?} | (T C?)
T -> (STRING | NUM | DOT | JUGADA | SPACE | DOTS)+

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
J1 -> Ns | C SPACE RESULTADO | RESULTADO .
Ns -> N N1 .
N1 -> Cs | RESULTADO | .
Cs -> C SPACE C2 .                
C2 -> RESULTADO | .               
N  -> N2 JUGADA SPACE .
N2 -> C NUM DOTS SPACE | .
C  -> { T C1 } | ( T C1 ) .
C1 -> C | .
T  -> T1 T | T1 .
T1 -> STRING | NUM | DOT | JUGADA | SPACE | DOTS .

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

# S  -> D P S1 .
def p_start(p):
    'start : desc part start1'

# S1 -> S 
def p_start1_cont(p):
    'start1 : start'

# S1 -> .
def p_start1_lambda(p):
    'start1 : '

# D  -> DESCRIPTOR D1 .
def p_descriptor(p):
    'desc : DESCRIPTOR desc1'

# D1 -> D 
def p_descriptor1_cont(p):
    'desc1 : desc'

# D1 -> .
def p_descriptor1_lambda(p):
    'desc1 : '

# P  -> J P1 .    
def p_partida(p):
    'part : jug part1'

# P1 -> P
def p_partida1_cont(p):
    'part1 : part'

# P1 -> . 
def p_partida1_lambda(p):
    'part1 : '

# J  -> B J1 .
def p_jugada(p):
    'jug : blanca jug1'

# B  -> NUM DOT SPACE JUGADA SPACE .
def p_blancas(p):
    'blanca : NUM DOT SPACE JUGADA SPACE'

# J1 -> Ns .
def p_jugada1_empieza_negras(p):
    'jug1 : negras'

# J1 -> C SPACE RESULTADO 
def p_jugada1_empieza_comentario(p):
    'jug1 : comentario SPACE RESULTADO'

# J1 -> RESULTADO 
def p_jugada1_termina(p):
    'jug1 : RESULTADO'

# Ns -> N N1 .
def p_negras(p):
    'negras : negra negra1'

# N1 -> Cs
def p_negra1_empieza_comentario(p):
    'negra1 : comentarios'

# N1 -> RESULTADO
def p_negra1_termina(p):
    'negra1 : RESULTADO'

# N1 -> .
def p_negra1_lambda(p):
    'negra1 : '

# Cs -> C SPACE C2 .
def p_comentarios(p):
    'comentarios : comentario SPACE comentario2'

# C2 -> RESULTADO .
def p_comentario2_termina(p):
    'comentario2 : RESULTADO'

# C2 -> .
def p_comentario2_termina(p):
    'comentario2 : '

# N  -> N2 JUGADA SPACE .
def p_negra(p):
    'negra : negra2 JUGADA SPACE'

# N2 -> C NUM DOTS SPACE
def p_negra2_ocurre(p):
    'negra2 : comentario NUM DOTS SPACE'

# N2 -> .
def p_negra2_lambda(p):
    'negra2 : '

# C  -> { T C1 }
def p_comentario_llaves(p):
    'comentario : LLLAVE texto comentario1 RLLAVE'

# C  -> ( T C1 ) .
def p_comentario_parentesis(p):
    'comentario : LPAREN texto comentario1 RPAREN'

# C1 -> C | .
def p_comentario1_comentario(p):
    'comentario1 : comentario'

# C1 -> C | .
def p_comentario1_lambda(p):
    'comentario1 : '

# T  -> T1 T
def p_texto_cont(p):
    'texto : texto1 texto'

# T  -> T1 .
def p_texto_termina(p):
    'texto : texto1'

# T1 -> STRING
def p_texto1_string(p):
    'texto1 : STRING'

# T1 -> NUM
def p_texto1_numerico(p):
    'texto1 : NUM'

# T1 -> DOT .
def p_texto1_punto(p):
    'texto1 : DOT'

# T1 -> DOTS .
def p_texto1_puntos(p):
    'texto1 : DOTS'

# T1 -> JUGADA .
def p_texto1_jugada(p):
    'texto1 : JUGADA'

# T1 -> SPACE .
def p_texto1_espacio(p):
    'texto1 : SPACE'

def p_error(p):
    raise Exception(f"Parser: Syntax error at {p.value!r}")

parser = yacc.yacc()

# Test it out
data = '''
[a "b"]
1. e4 d5 {defensa escandinava (es com´un 2. exd5 Da5 {no es com´un 2... c6})} 1/2-1/2'''

# Give the lexer some input
lexer.input(data)

print("LEXER", end="\n\n")

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(f'{tok.type}({tok.value})', end = ' ')

print("\n\nPARSER", end="\n\n")

print(parser.parse(data))
