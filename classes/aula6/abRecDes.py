from abLex import lexer
import re

#gramatica
#Arvore -> '(' ArvoreRamos
#
# ArvoreRamos -> Int  Arvore   Arvore ')'
#              | ')'        

prox_simb = ('Erro', '', 0, 0)
#soma=0
def rec_Arv():
    global prox_simb
    if prox_simb and (prox_simb.type == 'PA'):
        print(f"Reconheci Pa  --> {prox_simb.value}")
        prox_simb = lexer.token()
        val = rec_ArvR()
    else:
        print("Erro: esperava 'PF' --> '(' ")
        val =0
    return val
    
def rec_ArvR():
    global prox_simb
    #global soma
    if prox_simb and (prox_simb.type == 'INT'):
        print(f"Reconheci um INT --> {prox_simb.value}")
        val = int(prox_simb.value)
        prox_simb = lexer.token()
        vale =rec_Arv()
        vald =rec_Arv()
        if prox_simb and prox_simb.type=='PF':
            print(f"Reconheci Pf --> {prox_simb.value}")
            prox_simb = lexer.token()
        else:
            print("Erro: esperava 'PF' --> ')' ")
    elif prox_simb and (prox_simb.type == 'PF'):
        print(f"Reconheci Pf --> {prox_simb.value}")
        prox_simb = lexer.token()
        val=0
        vale = 0
        vald = 0
    else:
        print("Erro: esperava 'PF' --> ')' ou 'INT' --> '[0-9]' ")
    return val + vale + vald
def rec_Parser(linha):
    #global soma
    global prox_simb
    lexer.input(linha)
    prox_simb = lexer.token()
    val= rec_Arv()
    print(f"Soma total dos nodos da arvore é: {val}")
    print("That's all folks!")

linha = input("Introduza uma expressão: ")
rec_Parser(linha)