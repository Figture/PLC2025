import ply.lex as lex
import re


states = (
    ('dinheiro', 'exclusive'),
    # num estado exclusivo, apenas aplicamos os tokens e regras para esse estado
    # por outro lado, num estado inclusivo, as regras e tokens desse estado juntam-se às outras regras e tokens
    # o estado inicial chama-se 'INITIAL' e não é preciso defini-lo
)

tokens = (
    'LISTAR',
    'MOEDA',
    'CENT',
    'EURO',
    'TERMINATOR',
    'PROD',
    'SELECIONAR',
    # 'SAIR',
    # 'SALDO',
    # 'SAIR'
)



def t_LISTAR(t):
    r'LISTAR'
    
    if hasattr(t.lexer, 'dados') and t.lexer.dados:
        # Cabeçalho
        print(f"{'COD':<5} | {'NOME':<15} | {'QUANTIDADE':<10} | {'PREÇO':<5}")
        print("-"*45)
        # Dados
        for p in t.lexer.dados:
            print(f"{p['cod']:<5} | {p['nome']:<15} | {p['quant']:<10} | {p['preco']:<5}")
    else:
        print("Stock Vazio")
    return t

def t_MOEDA(t):
    r'MOEDA'
    t.lexer.begin('dinheiro')
    return t

def t_dinheiro_EURO(t):
    r'(?:1|2|5|10|20|50)e'
    # Obter o valor do grupo
    valor = int(t.value[:-1])  # remove o 'e' no final
    t.lexer.euro += valor
    return t

def t_dinheiro_CENT(t):
    r'(?:1|2|5|10|20|50)c'
    valor = int(t.value[:-1]) /100.0  # remove o 'c' no final
    t.lexer.euro += valor
    return t

def t_dinheiro_TERMINATOR(t):
    r'\.'
    print(f"Saldo = {t.lexer.euro}e{t.lexer.cent}c")
    t.lexer.begin('INITIAL')
    return t

def t_SELECIONAR(t):
    r'SELECIONAR'
    t.lexer.begin('dinheiro')
    return t
#ACABAR ISTO
def t_dinheiro_PROD(t):
    r'[A-B]\d{2}'
    if hasattr(t.lexer, 'dados') and t.lexer.dados:
        print("ola")

t_ignore = ' \t\n,'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer= lex.lex()
