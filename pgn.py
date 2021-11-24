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
t_JUGADA        = r'([PNBRQK]?[a-h]?[1-8]?x?[a-h][1-8]\+?\+?|O-O|O-O-O)(!|\?)?'
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
T  -> (STRING | NUM | DOT | JUGADA | SPACE )+

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
T1 -> STRING | NUM | DOT | JUGADA | SPACE .

 - {T} -> if jugada_captura(T) then 1 else 0
 - (T) -> if jugada_captura then 1 else 0
 - {C T} -> if c.value > 0 then c.value + 1 else jugada_captura(T)

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

# S  -> D P S1 .
def p_start(p):
    'start : desc part start1'
    p[0] = "He concluido con el parseo de la entrada."

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
def p_comentario2_lambda(p):
    'comentario2 : '

# N  -> N2 JUGADA SPACE .
def p_negra(p):
    'negra : negra2 JUGADA SPACE'

# N2 -> C SPACE NUM DOTS SPACE
def p_negra2_ocurre(p):
    'negra2 : comentario SPACE NUM DOTS SPACE'

# N2 -> .
def p_negra2_lambda(p):
    'negra2 : '

# C  -> CL
def p_comentario_llave_apertura(p):
    'comentario : comentario_llave'

# C  -> { C T } .
def p_comentario_llave_coment_texto_llave(p):
    'comentario : LLLAVE comentario texto RLLAVE'

# C -> CP 
def p_comentario_parentesis_apertura(p):
    'comentario : comentario_paren'

# C  -> ( C T ) .
def p_comentario_paren_coment_texto_paren(p):
    'comentario : LPAREN comentario texto RPAREN'

# CL -> { T C6 .
def p_comentario_llave(p):
    'comentario_llave : LLLAVE texto comentario6'

# C6 -> } .
def p_comentario_llave_cierre(p):
    'comentario6 : RLLAVE'

# C6 -> C4 .
def p_comentario6(p):
    'comentario6 : comentario4'

# CP -> ( T C7 .
def p_comentario_paren_apertura(p):
    'comentario_paren : LPAREN texto comentario7'
    
# C7 -> C5 .
def p_comentario7(p):
    'comentario7 : comentario5'

# C7 -> ) .
def p_comentario7_paren_cierre(p):
    'comentario7 : RPAREN'
    
# C4 -> C C8.
def p_comentario4_empieza_comentario(p):
    'comentario4 : comentario comentario8'
    
# C8 -> } .
def p_comentario8_llave(p):
    'comentario8 : RLLAVE'

# C8 -> T } .
def p_comentario8_texto(p):
    'comentario8 : texto RLLAVE'

# C5 -> C C9 .
def p_comentario5(p):
    'comentario5 : comentario comentario9'
    
# C9 -> ) .
def p_comentario9_parentesis(p):
    'comentario9 : RPAREN'

# C9 -> T ) .
def p_comentario9_texto(p):
    'comentario9 : texto RPAREN'

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
[prueba "loca"]
[Nzscf5qWgtg~NVX "56B~n~nQIeAhy"]
[gvk7dXkliRpR "2LAkQJGhz81"]
[~NFS5lBHW4Mm~NmJsP "e4ZhVulzl"]
[yZ1PSI4r78KP "XwWzscEtUqkAu~nNt7Hq5"]
[GArzOdNa~nITcsbFO9ES "WUodxeqxI"]

1. 1d7 d7 2. Rf8 gg7 1-0

[2ujZrN6LTmOBGss5jzqw "pnAGk"]
[kRM "lihgftp5kLaiAvuNSub2"]
[vUPhgAiKx "a9C7isOkq0vyep7svNE"]
[Lbfh "j6htrD1wKNFryNGHdUcG"]

1. Pxe7 Pad3 2. Be6 b6 3. Bb2 h3 4. Qc1 Kh3 5. Pb1 Pb2 6. Ra1 a7! 7. Nce4 Qxa3 8. Kd4 Qh1 9. Kd8 fh6 10. Nc1 Pg1 11. Nh2 Bf4 12. ca6 Kd8 13. Nb4 d5 14. e1 Ra5 15. f8 K5xd3 16. b6 (Ka4 h5a2) 16... g7 17. e5 Bg2 18. f3 Re2 19. Qc6 Kb4 20. Rg4 Rg3 21. g3 N2c7 22. Pb7 Rh7 23. Qd3 {bf8 B b3 K Nxf5 wuFzW c1 Pbd2 T c8 ka Pg3 K Ke6+ n Kg5 Pb7 f8 e2 O 1c5 Rxe4 Pxc5} 23... e6 24. d5 Nh7 25. Qxc6 Bxc3 26. Bf5 Qfa3 27. f4 Ka7 28. Nxb6 d6 29. Bg1 Qf2 30. Pb3 d6 31. Ba3 e7 32. Bab4 Kda1 33. Ph1 e2 34. cf4 Nxd7 35. Nc7 (gr Pfg2 iONp utl Pcd2 t (Pd3 Rc2 Bxd6 Kxg8 Kxh2 h6 Bxc8 zAx g2 qX Nh2 N c3 ~n Bxb5 D Nd1 h8 a1 c7 PVAO Rg7 g5 Kb6 oGq) rt Pf8 Qp) 35... e2 36. Ra6 Bhb8 37. Q5a4 c5 38. Qg7 g1 39. g6 Pg7 40. Kd6 d1 41. h7+ Kcc5 42. Qd8 ce1 43. Qxh3 Pa6 44. Bxe2 e4 45. Bh7 d2+ 1/2-1/2

[BYsR4sFynE2R~n2 "lNykA4WPhvh2kKPTjfaD"]
[loCuhQ "WDOTwZIISKjDik~n6"]

1. Pb7 ec6 2. f4 Nxf7 3. Kxe5 d7 4. Kc7 Rd6 5. e7 Qc7 6. h1 {s Rxb7 iI d5 Nh7} 6... e4+ 7. 7d6 Nf7a3 8. Pa7 e2 9. h8 h4 10. g8 Kxf6 11. 2b3 Bxg3 12. Q5h1 Pb6 13. fd4 e5 14. 5c6 f3 15. cb6 {l Pb6} 15... Pb1 16. Nb3 h7 17. b2 Nb7 18. Ra1 N8h6 19. f2 c8 20. P5g1 e1 21. Pg3 c3 22. f5 Kh1 23. Pd7 Nf3 24. Nd1 Rd1 25. Kd5 Ng8 26. e3 Nxg6 27. Rh8 fc3 28. Kxf1 Ncc4 29. c1+ e3 30. cc6 (a Kdxa3 e7 JQ Qe2 VLzeFq c7 FU f4 N Qxb7 Nd8++ Tf Nd2 yN ba2 me 1b6 hu Kd7 R Pxe6 Nxg7 DaR Ba8 Kxd5 Nd7 ttxI fe7 GK a2 m f6 Skp) 30... h8 31. Qh1 a1 32. fb7 b7 0-1

[4e "ws20"]

1. Bxd1 Pa6 0-1
'''

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

resultado = parser.parse(data)
print(resultado)
