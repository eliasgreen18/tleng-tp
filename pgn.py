import lex
import yacc

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
t_STRING        = r'[a-zA-ZñÑáéíóúÁÉÍÓÚ\-!,’´~]+'
t_JUGADA        = r'([PNBRQK]?[a-h]?[1-8]?x?[a-h][1-8]\+?\+?|O-O(-O)?)(!|\?)?'
t_DESCRIPTOR    = r'\[[a-zA-Z0-9ñÑáéíóúÁÉÍÓÚ~]+\ "[a-zA-Z0-9ñÑáéíóúÁÉÍÓÚ\.\?\ -~]+"\]'
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
N -> (C SPACE NUM DOTS SPACE)? JUGADA SPACE
B -> NUM DOT SPACE JUGADA SPACE
C -> {T (C T)?} | (T (C T)?)
T -> (STRING | NUM | DOT | JUGADA | SPACE )+

# Tercera iteración

S  -> (DESCRIPTOR+ P)+
P  -> J+
J  -> B (Ns | C SPACE RESULTADO | RESULTADO)
Ns -> N (Cs | RESULTADO | .)
Cs -> C SPACE RESULTADO?
N  -> (C SPACE NUM DOTS SPACE)? JUGADA SPACE
B  -> NUM DOT SPACE JUGADA SPACE
C  -> CT | { C T } | CP | ( C T ) .
CL -> { T [C4 | }] .
CP -> ( T [C5 | )] .
C4 -> C [} | T }] .
C5 -> C [) | T )] .
T  -> (STRING | NUM | DOT | JUGADA | SPACE | DOTS)+

# Cuarta iteración

S  -> (DESCRIPTOR+ P)+
P  -> J+
J  -> B (Ns | C SPACE RESULTADO | RESULTADO)
Ns -> N (Cs | RESULTADO | .)
Cs -> C SPACE RESULTADO?
N  -> (C SPACE NUM DOTS SPACE)? JUGADA SPACE
B  -> NUM DOT SPACE JUGADA SPACE
C  -> { C1 } | ( C1 ) .
C1 -> T (C | .) | C (T | .) .
T  -> (STRING | NUM | DOT | JUGADA | SPACE | DOTS)+

############################ Gramática derivada

# Cuarta iteración

P -> J P | J .
J -> NUM .... NUM... .....

S  -> D P S | D P .                 {  }
D  -> DESCRIPTOR D | DESCRIPTOR .
P  -> J P | J .
J  -> B Ns | B C SPACE RESULTADO | B RESULTADO .
B  -> NUM DOT SPACE JUGADA SPACE .
- Ns -> N Cs | N RESULTADO | N .
- Cs -> C SPACE RESULTADO | C SPACE .                        
.N  -> C SPACE NUM DOTS SPACE JUGADA SPACE | JUGADA SPACE .
.C  -> { Cu } | ( Cu ) . 
.Cu -> CT | CC .
.CT -> T CC | T . 
.CC -> C T | C .
.T  -> T1 T | T1 .
.T1 -> STRING | NUM | DOT | JUGADA | SPACE | DOTS .

| atrib | tipo | sintetizado o heredado?
| J.
|
|
|
|
|
|
|

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
N2 -> C SPACE NUM DOTS SPACE | .
C  -> CL | { C T } | CP | ( C T ) .  
CL -> { T C6 .
C6 -> C4 | } .
CP -> ( T C7 .
C7 -> C5 | ) .
C4 -> C C8.
C8 -> } | T } .
C5 -> C C9 .
C9 -> ) | T ) .
T  -> T1 T | T1 .
T1 -> STRING | NUM | DOT | JUGADA | SPACE | DOTS .

- Recordar chequear los números 

 - {T} -> jugada_captura(T) then 0 else 1
 - (T) -> jugada_captura(T) then 0 else 1
 - {C T} -> if C.nivel_anidamiento > 0 then C.nivel_anidamiento + 1 else jugada_captura(T)
( {} ... {} )

   r - - > 0, 1, 2, 3 ...
   |
   | r - > C.value + 1 or ¿captura en T?
   | |
   v v
 { C T }

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
C  -> {T C' T} | (T C' T)
C' -> C | λ
T  -> Ts T | λ
Ts -> STRING | NUM | DOT | JUGADA | SPACE

# ¿Anidados intercalados?

C  -> CP | CL
CP -> (T CL) | λ
CL -> {T CP} | λ
"""

class PGN():
    def __init__(self, nesting, number):
        self.nesting = nesting
        self.number  = number

class Comentario():
    def __init__(self, nesting, capture):
        self.nesting = nesting
        self.capture = capture
        
def condition(expression, message):
    if not expression:
        raise Exception(message)
    
# S  -> D P S .
def p_start_conc(p):
    'start : desc part start'
    condition(p[2].number == 1, "la numeración no comienza en 1")
    p[0] = max(p[2].nesting, p[3])

# S  -> D P .
def p_start(p):
    'start : desc part '
    condition(p[2].number == 1, "la numeración no comienza en 1")
    p[0] = p[2].nesting

# D  -> DESCRIPTOR D .
def p_descriptor_conc(p):
    'desc : DESCRIPTOR desc'

# D  -> DESCRIPTOR  .
def p_descriptor(p):
    'desc : DESCRIPTOR '

# P  -> J P . 
def p_partida_conc(p):
    'part : jug part'
    condition(p[1].number == (p[2].number - 1), "numeración no consecutiva")
    p[0] = PGN(max(p[1].nesting, p[2].nesting), p[1].number)
    
# P  -> J .
def p_partida_jugada(p):
    'part : jug'
    p[0] = p[1]

# J  -> B Ns .
def p_jugada_negras(p):
    'jug : blanca negras'
    if p[2].number != -1:
        condition(p[1].number == p[2].number, "no mantiene numeración entre jugada de negras y blancas")
    p[0] = PGN(max(p[1].nesting, p[2].nesting), p[1].number)

# J  -> B C SPACE RESULTADO .
def p_jugada_comentario(p):
    'jug : blanca comentario SPACE RESULTADO'
    p[0] = PGN(max(p[1].nesting, p[2].nesting), p[1].number)

# J  -> B RESULTADO .
def p_jugada_fin(p):
    'jug : blanca RESULTADO'
    p[0] = p[1]

# B  -> NUM DOT SPACE JUGADA SPACE .
def p_blancas(p):
    'blanca : NUM DOT SPACE JUGADA SPACE'
    p[0] = PGN(0, int(p[1]))

# Ns -> N Cs .
def p_negras_comentarios(p):
    'negras : negra comentarios'
    p[0] = PGN(max(p[1].nesting, p[2].nesting), p[1].number)

# Ns -> N RESULTADO .
def p_negras_resultado(p):
    'negras : negra RESULTADO'
    p[0] = p[1]

# Ns -> N .
def p_negras(p):
    'negras : negra'
    p[0] = p[1]

# Cs -> C SPACE RESULTADO .
def p_comentarios_resultado(p):
    'comentarios : comentario SPACE RESULTADO'
    p[0] = PGN(p[1],-1)

# Cs -> C SPACE .
def p_comentarios(p):
    'comentarios : comentario SPACE'
    p[0] = PGN(p[1],-1)

# N  -> C SPACE NUM DOTS SPACE JUGADA SPACE .
def p_negra_comentario(p):
    'negra : comentario SPACE NUM DOTS SPACE JUGADA SPACE'
    p[0] = PGN(p[1], int(p[3]))

# N  -> JUGADA SPACE .
def p_negra(p):
    'negra : JUGADA SPACE'
    p[0] = PGN(0,-1)

# C  -> { Cu } .
def p_comentario_llave_cuerpo(p):
    'comentario : LLLAVE cuerpo RLLAVE'
    p[0] = p[2].nesting + 1 if p[2].nesting > 0 else (0 if p[2].capture else 1)

# C  -> ( Cu ) .
def p_comentario_paren_cuerpo(p):
    'comentario : LPAREN cuerpo RPAREN'
    p[0] = p[2].nesting + 1 if p[2].nesting > 0 else (0 if p[2].capture else 1)

# Cu -> CT .
def p_cuerpo_text(p):
    'cuerpo : comentario_texto'
    p[0] = p[1]

# Cu  -> CC .
def p_cuerpo_comentario(p):
    'cuerpo : comentario_comentario'
    p[0] = p[1] 

# CT -> T CC . 
def p_comentario_texto_comentario(p):
    'comentario_texto : texto comentario_comentario'
    p[0] = Comentario(p[2].nesting, p[1] or p[2].capture)

# CT -> T . 
def p_comentario_texto_texto(p):
    'comentario_texto : texto'
    p[0] = Comentario(0, p[1])

# CC -> C T .
def p_comentario_comentario_texto(p):
    'comentario_comentario : comentario texto'
    p[0] = Comentario(p[1], p[2])

# CC -> C .
def p_comentario_comentario(p):
    'comentario_comentario : comentario'
    p[0] = Comentario(p[1], False)

# T  -> T1 T
def p_texto_cont(p):
    'texto : texto1 texto'
    p[0] = p[1] or p[2]

# T  -> T1 .
def p_texto_termina(p):
    'texto : texto1'
    p[0] = p[1]

# T1 -> STRING
def p_texto1_string(p):
    'texto1 : STRING'
    p[0] = False

# T1 -> NUM
def p_texto1_numerico(p):
    'texto1 : NUM'
    p[0] = False

# T1 -> DOT .
def p_texto1_punto(p):
    'texto1 : DOT'
    p[0] = False

# T1 -> DOTS .
def p_texto1_puntos(p):
    'texto1 : DOTS'
    p[0] = False
    
# T1 -> JUGADA .
def p_texto1_jugada(p):
    'texto1 : JUGADA'
    p[0] = "x" in p[1]
    
# T1 -> SPACE .
def p_texto1_espacio(p):
    'texto1 : SPACE'
    p[0] = False
    
def p_error(p):
    raise Exception(f"Parser: Syntax error at {p.value!r}")

parser = yacc.yacc()

# Test it out
data = ""

with open('entrada.txt') as f:
    data = f.read()

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input

resultado = parser.parse(data)
print("Máximo nivel de anidamiento:", resultado)
