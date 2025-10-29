from lexpa import lexer
import re

#gramatica
#PAR --> (PAR) PAR | PASS

prox_simb = ('Erro', '', 0, 0)

def rec_Par():
    global prox_simb
    if prox_simb and (prox_simb.type == 'PA'):
        print(f"Reconheci Pa {prox_simb.value}")
        prox_simb = lexer.token()
        rec_Par()
        if prox_simb and prox_simb.type=='PF':
            print(f"Reconheci Pf {prox_simb.value}")
            prox_simb = lexer.token()
            rec_Par()
        else:
            print("Erro: esperava 'PF' ")
    else: 
        pass


def rec_Parser(linha):
 
    global prox_simb
    lexer.input(linha)
    prox_simb = lexer.token()
    rec_Par()
    print("That's all folks!")

linha = input("Introduza uma expressão: ")
rec_Parser(linha)