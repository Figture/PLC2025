import ply.lex as lex
import re

tokens = (
    'PA',
    'PF'
)

t_PA = r'\('
t_PF= r'\)'
t_ignore = ' \t\n,'

def t_error(t):
    print(f"Caracter Inválido '{t.value[0]}'")
    t.lexer.skip(1)

lexer=lex.lex()