import ply.lex as lex
import re



#token names
tokens = (
    'SELECT',
    'WHERE',
    'VAR',
    'ID',
    'TERMINATOR',
    'PA',
    'PF',
)

t_SELECT = r'SELECT'
t_WHERE = r'WHERE'
t_VAR= r'\?\w+'
t_ID= r'\w*:\w+'
t_TERMINATOR=r'\.'
t_PA=r'\{'
t_PF=r'\}'
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

test= """SELECT ?a ?b ?c WHERE
{
  ?a rdf:type :Pessoa .
  ?a :temIdade ?b .
  ?a :eIrmaosDe ?c .
}
"""

lexer.input(test)


while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)