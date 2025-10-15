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
    'SAIR',
)



def t_LISTAR(t):
    r'\bLISTAR\b'
    
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
    r'\bMOEDA\b'
    t.lexer.begin('dinheiro')
    return t

def t_dinheiro_EURO(t):
    r'\b(?:50|20|10|5|2|1)e\b'
    # Obter o valor do grupo
    valor = int(t.value[:-1])  # remove o 'e' no final
    t.lexer.euro += valor
    return t

def t_dinheiro_CENT(t):
    r'\b(?:50|20|10|5|2|1)e\b'
    valor = int(t.value[:-1]) /100.0  # remove o 'c' no final
    t.lexer.euro += valor
    return t

def t_dinheiro_TERMINATOR(t):
    r'\.'
    valor = t.lexer.euro   
    total_cent = round(valor * 100)   
    eur, centi = divmod(total_cent, 100)
    print(f"Saldo = {eur}e{centi}c")
    t.lexer.begin('INITIAL')
    return t

def t_SELECIONAR(t):
    r'SELECIONAR'
    t.lexer.begin('selecao')
    return t

def t_selecao_PROD(t):
    r'\b[A-Z]\d{2}\b'
    if hasattr(t.lexer, 'dados') and t.lexer.dados:
        product= next((p for p in t.lexer.dados if p["cod"] == t.value), None)
        if product:
            if product["quant"] <= 0:
                print(f'Produto com o código {t.value} está esgotado.')
                t.lexer.begin('INITIAL')
                return t
            else:
                if t.lexer.euro >= product["preco"]:
                    product["quant"] -= 1
                    t.lexer.euro -= product["preco"]
                    prod= product["nome"]
                    valor = t.lexer.euro   
                    total_cent = round(valor * 100)   
                    eur, centi = divmod(total_cent, 100)
                    print(f"maq: Pode retirar o produto dispensado {prod}")
                    print(f"maq: Saldo = {eur}e{centi}c")
                else:
                    valor = t.lexer.euro   
                    total_cent = round(valor * 100)   
                    eur, centi = divmod(total_cent, 100)
                    prod = product["preco"]
                    total_prod=round(prod * 100)
                    eu, ct=divmod(total_prod, 100)    
                    print("maq: Saldo insufuciente para satisfazer o seu pedido")
                    print(f"maq: Saldo = {eur}e{centi}c; Pedido = {eu}e{ct}c")
        else:
            print(f'Produto com o código {t.value} não existe em stock.')
        
    t.lexer.begin('INITIAL')
    return t
def t_SAIR(t):
    r'\bSAIR\b'
    total_cent = round(t.lexer.euro * 100)
    moedas = [200, 100, 50, 20, 10, 5, 2, 1]  # em cêntimos
    troco = []

    for m in moedas:
        qtd, total_cent = divmod(total_cent, m)
        if qtd > 0:
            if m >= 100:
                troco.append(f"{qtd}x {m//100}e")
            else:
                troco.append(f"{qtd}x {m}c")

    if troco:
        print(f"maq: Pode retirar o troco: {', '.join(troco)}.")
    else:
        print("maq: Sem troco a devolver.")
    
    return None



t_ignore = ' \t\n,'
t_selecao_ignore = ' \t\n,'
t_dinheiro_ignore= ' \t\n,'

def t_error(t):
    print(f"Opção Inválida '{t.value[0]}'")
    t.lexer.skip(1)

def t_selecao_error(t):
    print(f"Código  incorreto: '{t.value[0]}'")
    t.lexer.skip(1)

def t_dinheiro_error(t):
    print(f"Erro a colocar moedas: '{t.value[0]}'")
    t.lexer.skip(1)

lexer= lex.lex()
