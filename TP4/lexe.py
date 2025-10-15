import ply.lex as lex
import re, math


states = (
    ('dinheiro', 'exclusive'),
    ('selecao', 'exclusive')
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
    eur, centi = math.mod(t.lexer.euro)
    print(f"Saldo = {eur}e{centi}c")
    t.lexer.begin('INITIAL')
    return t

def t_SELECIONAR(t):
    r'SELECIONAR'
    t.lexer.begin('selecao')
    return t
#verificar se posso usar t.lexer.dados[product]["x"]
def t_selecao_PROD(t):
    r'[A-Z]\d{2}'
    if hasattr(t.lexer, 'dados') and t.lexer.dados:
        product= next((p for p in t.lexer.dados if p["cod"] == t.value), None)
        if product:
            if product["quant"] <= 0:
                print(f'Produto com o código {t.value} está esgotado.')
                t.lexer.begin('INITIAL')
                return t
            else:
                if t.lexer.euro < product["preco"]:
                    t.lexer.dados[product]["quant"] -= 1
                    t.lexer.euro -= product["preco"]
                    print(f"maq: Pode retirar o produto dispensado {product["nome"]}")
        else:
            print(f'Produto com o código {t.value} não existe em stock.')
        
    t.lexer.begin('INITIAL')
    return t
    

t_ignore = ' \t\n,'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer= lex.lex()
