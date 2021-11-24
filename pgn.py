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
        
def condition(expression):
    if not expression:
        raise Exception()
    
# S  -> D P S .
def p_start_conc(p):
    'start : desc part start'
    condition(p[2].number == 1)
    p[0] = max(p[2].nesting, p[3])

# S  -> D P .
def p_start(p):
    'start : desc part '
    condition(p[2].number == 1)
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
    condition(p[1].number == (p[2].number - 1))
    p[0] = PGN(max(p[1].nesting, p[2].nesting), p[1].number)
    
# P  -> J .
def p_partida_jugada(p):
    'part : jug'
    p[0] = p[1]

# J  -> B Ns .
def p_jugada_negras(p):
    'jug : blanca negras'
    if p[2].number != -1:
        condition(p[1].number == p[2].number)
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
    condition(p[1].isnumeric())
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
    condition(p[3].isnumeric())
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

[a "b"]

1. e4 d5 {defensa escandinava (es com´un 2. exd5 Da5 {no es com´un 2... c6})} 1/2-1/2

[Event "Mannheim"]
[Site "Mannheim GER"]
[Date "1914.08.01"]
[EventDate "1914.07.20"]
[Round "11"]
[Result "1-0"]
[White "Alexander Alekhine"]
[Black "Hans Fahrni"]
[ECO "C13"]
[WhiteElo "?"]
[BlackElo "?"]
[PlyCount "45"]

1. e4 {Notes by Richard Reti} 1... e6 2. d4 d5 3. Nc3 Nf6 4. Bg5 Be7 5. e5 Nfd7 6. h4 {This ingenious method of play which has subsequently been adopted by all modern masters is characteristic of Alekhine’s style.} 6... Bxg5 7. hxg5 Qxg5 8. Nh3 {! The short-stepping knight is always brought as near as possible to the actual battle field. Therefore White does not make the plausible move 8 Nf3 but 8 Nh3 so as to get the knight to f4.} 8... Qe7 9. Nf4 Nf8 10. Qg4 f5 {The only move. Not only was 11 Qxg7 threatened but also Nxd5.} 11. exf6 gxf6 12. O-O-O {He again threatens Nxd5.} 12... c6 13. Re1 Kd8 14. Rh6 e5 15. Qh4 Nbd7 16. Bd3 e4 17. Qg3 Qf7 {Forced - the sacrifice of the knight at d5 was threatened and after 17...Qd6 18 Bxe4 dxe4 19 Rxe4 and 20 Qg7 wins.} 18. Bxe4 dxe4 19. Nxe4 Rg8 20. Qa3 {Here, as so often happens, a surprising move and one difficult to have foreseen, forms the kernel of an apparently simple Alekhine combination.} 20... Qg7 {After 20.Qe7 21.Qa5+ b6 22.Qc3 would follow.} 21. Nd6 Nb6 22. Ne8 Qf7 {White mates in three moves.} 23. Qd6+ 1-0
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
